#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
QWEN_ROUTER = SCRIPT_DIR / "qwen_router.py"
TARGET_EXPERT = 114
TARGET_LAYERS = [14, 26]


def load_reconstruct_probs():
    spec = importlib.util.spec_from_file_location("qwen_router", QWEN_ROUTER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load qwen_router from {QWEN_ROUTER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reconstruct_probs


reconstruct_probs = load_reconstruct_probs()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export per-token E114 breakdown for a single-prompt Huahua run.")
    parser.add_argument("--capture-dir", required=True)
    parser.add_argument("--out-tsv", required=True)
    parser.add_argument("--out-json", required=True)
    return parser.parse_args()


def parse_metadata(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def load_generated_tokens(cell_dir: Path) -> list[dict[str, Any]]:
    return json.loads((cell_dir / "generated_tokens.json").read_text())


def phase_probs(arr: np.ndarray, n_prompt: int, n_gen: int) -> tuple[np.ndarray, np.ndarray]:
    prefill = reconstruct_probs(arr[:n_prompt])
    if arr.shape[0] == n_prompt + n_gen:
        generation_logits = arr[n_prompt : n_prompt + n_gen]
    elif arr.shape[0] == n_gen + 1:
        generation_logits = arr[1:]
    elif arr.shape[0] == n_gen:
        generation_logits = arr
    else:
        generation_logits = arr[n_prompt:]
    generation = reconstruct_probs(generation_logits)
    return prefill, generation


def token_row(phase: str, local_idx: int, global_idx: int, token_id: int | None, token_piece: str, stats: dict[int, dict[str, float]]) -> list[str]:
    row = [
        phase,
        str(local_idx),
        str(global_idx),
        "" if token_id is None else str(token_id),
        token_piece.replace("\t", "\\t").replace("\n", "\\n"),
    ]
    for layer in TARGET_LAYERS:
        layer_stats = stats[layer]
        row.extend(
            [
                f"{layer_stats['W']:.8f}",
                f"{layer_stats['S']:.8f}",
                "" if np.isnan(layer_stats["Q"]) else f"{layer_stats['Q']:.8f}",
            ]
        )
    return row


def main() -> None:
    args = parse_args()
    capture_dir = Path(args.capture_dir)
    cell_dirs = [p for p in capture_dir.iterdir() if p.is_dir()]
    if len(cell_dirs) != 1:
        raise RuntimeError(f"Expected exactly one prompt cell in {capture_dir}, found {len(cell_dirs)}")
    cell_dir = cell_dirs[0]
    metadata = parse_metadata(cell_dir / "metadata.txt")
    n_prompt = int(metadata["n_tokens_prompt"])
    n_gen = int(metadata["n_tokens_generated"])
    generated_tokens = load_generated_tokens(cell_dir)

    per_layer_prefill: dict[int, np.ndarray] = {}
    per_layer_generation: dict[int, np.ndarray] = {}
    for layer in TARGET_LAYERS:
        arr = np.load(cell_dir / "router" / f"ffn_moe_logits-{layer}.npy")
        prefill_probs, generation_probs = phase_probs(arr, n_prompt, n_gen)
        per_layer_prefill[layer] = prefill_probs[:, TARGET_EXPERT]
        per_layer_generation[layer] = generation_probs[:, TARGET_EXPERT]

    header = [
        "phase",
        "token_index_in_phase",
        "global_token_index",
        "token_id",
        "token_piece",
    ]
    for layer in TARGET_LAYERS:
        header.extend([f"E{TARGET_EXPERT}_W_L{layer}", f"E{TARGET_EXPERT}_S_L{layer}", f"E{TARGET_EXPERT}_Q_L{layer}"])
    lines = ["\t".join(header)]

    summary: dict[str, Any] = {
        "capture_dir": str(capture_dir),
        "prompt_id": metadata.get("prompt_id", cell_dir.name),
        "n_tokens_prompt": n_prompt,
        "n_tokens_generated": n_gen,
        "layers": TARGET_LAYERS,
        "phase_means": {"prefill": {}, "generation": {}},
    }

    for phase_name, n_tokens, token_meta, per_layer in (
        ("prefill", n_prompt, [(None, "") for _ in range(n_prompt)], per_layer_prefill),
        (
            "generation",
            min(n_gen, len(generated_tokens)),
            [(int(tok["token_id"]), str(tok.get("piece", ""))) for tok in generated_tokens[:n_gen]],
            per_layer_generation,
        ),
    ):
        for layer in TARGET_LAYERS:
            values = per_layer[layer][:n_tokens]
            selected = values > 0
            summary["phase_means"][phase_name][f"L{layer}"] = {
                "W_mean": float(values.mean()),
                "S_mean": float(selected.mean()),
                "Q_mean": float(values[selected].mean()) if np.any(selected) else None,
            }

        for idx in range(n_tokens):
            stats: dict[int, dict[str, float]] = {}
            for layer in TARGET_LAYERS:
                value = float(per_layer[layer][idx])
                selected = 1.0 if value > 0 else 0.0
                stats[layer] = {
                    "W": value,
                    "S": selected,
                    "Q": value if selected else float("nan"),
                }
            token_id, token_piece = token_meta[idx]
            global_idx = idx if phase_name == "prefill" else n_prompt + idx
            lines.append("\t".join(token_row(phase_name, idx, global_idx, token_id, token_piece, stats)))

    Path(args.out_tsv).write_text("\n".join(lines) + "\n")
    Path(args.out_json).write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
