#!/usr/bin/env python3
"""
Run the mirror shakedown or full experiment using the existing capture binary.

Cell selection is controlled by the TSV file you pass in:
  - Shakedown: pass a TSV with only L3_true_self, L3_shuffled, L3_null_control
  - Full run: pass a TSV with all 18 cells

The binary iterates TSV rows, clears KV cache between them, and writes
per-prompt capture directories:

    runs/<run_name>/capture/<prompt_id>/router/ffn_moe_logits-<layer>.npy
    runs/<run_name>/capture/<prompt_id>/generated_text.txt
    runs/<run_name>/capture/<prompt_id>/metadata.txt
    runs/<run_name>/capture/<prompt_id>/generated_tokens.json
    runs/<run_name>/capture/<prompt_id>/prompt_tokens.json

The --routing-only flag captures only router tensors (not full layer activations)
but still generates text. generated_text.txt is always written.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime

_HERE = pathlib.Path(__file__).parent
RUNS_DIR = _HERE / "runs"

MODEL = os.environ.get(
    "MODEL_PATH",
    "/workspace/models/qwen35-hauhau-q8/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf",
)
BINARY = os.environ.get(
    "CAPTURE_BINARY",
    "/workspace/consciousness-experiment/capture_activations",
)
LLAMA_BUILD_BIN = os.environ.get(
    "LLAMA_BUILD_BIN",
    "/workspace/llama.cpp.new/build/bin",
)
NGL = int(os.environ.get("NGL", "999"))
CTX = int(os.environ.get("CTX", "16384"))
THREADS = int(os.environ.get("THREADS", "16"))
FLASH_ATTN = os.environ.get("FLASH_ATTN", "on")
CACHE_TYPE_K = os.environ.get("CACHE_TYPE_K", "q8_0")
CACHE_TYPE_V = os.environ.get("CACHE_TYPE_V", "q8_0")
SEED = int(os.environ.get("SEED", "42"))
MAX_NEW_TOKENS = int(os.environ.get("MAX_NEW_TOKENS", "2048"))
EXPECTED_ROUTER_LAYERS = 40


def read_tsv_ids(tsv_path: pathlib.Path) -> list[str]:
    """Extract prompt IDs from a TSV file (first column before tab)."""
    ids = []
    for line in tsv_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        tab = line.find("\t")
        if tab > 0:
            ids.append(line[:tab])
    return ids


def run_mirror(tsv_path: pathlib.Path, run_dir: pathlib.Path) -> int:
    capture_dir = run_dir / "capture"
    capture_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = LLAMA_BUILD_BIN + ":" + env.get("LD_LIBRARY_PATH", "")

    cmd = [
        BINARY,
        "-m", MODEL,
        "--prompt-file", str(tsv_path),
        "-o", str(capture_dir),
        "-n", str(MAX_NEW_TOKENS),
        "-ngl", str(NGL),
        "-c", str(CTX),
        "-t", str(THREADS),
        "-fa", FLASH_ATTN,
        "--cache-type-k", CACHE_TYPE_K,
        "--cache-type-v", CACHE_TYPE_V,
        "--seed", str(SEED),
        "--temp", "0",
        "--top-k", "1",
        "--top-p", "1",
        "--min-p", "0",
        "--repeat-penalty", "1",
        "--mirostat", "0",
        "--routing-only",
        "--no-stream",
    ]
    # No intervention flags. Baseline routing only.

    print("Running:", " ".join(cmd))
    sys.stdout.flush()
    completed = subprocess.run(cmd, env=env, check=False)
    return completed.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description="Mirror experiment runner")
    parser.add_argument("--tsv", required=True,
                        help="Path to mirror prompt TSV (cell selection is by TSV content)")
    parser.add_argument("--run-name", default=None,
                        help="Optional run directory name")
    args = parser.parse_args()

    tsv_path = pathlib.Path(args.tsv).resolve()

    # Preflight checks
    errors = []
    if not tsv_path.exists():
        errors.append(f"TSV not found: {tsv_path}")
    if not pathlib.Path(BINARY).exists():
        errors.append(f"Capture binary not found: {BINARY}")
    if not pathlib.Path(MODEL).exists():
        errors.append(f"Model not found: {MODEL}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Read cell IDs from TSV for manifest
    cell_ids = read_tsv_ids(tsv_path)
    if not cell_ids:
        print(f"ERROR: No valid rows in TSV: {tsv_path}", file=sys.stderr)
        sys.exit(1)

    RUNS_DIR.mkdir(exist_ok=True)
    run_name = args.run_name or datetime.utcnow().strftime("mirror-%Y%m%d-%H%M%S")
    run_dir = RUNS_DIR / run_name
    if run_dir.exists():
        print(f"ERROR: Run directory already exists: {run_dir}", file=sys.stderr)
        print(f"  Use a different --run-name or remove the existing directory.", file=sys.stderr)
        sys.exit(1)
    run_dir.mkdir(parents=True)

    # Copy the exact TSV used into the run directory
    shutil.copy2(tsv_path, run_dir / "prompts.tsv")

    # Save manifest
    manifest = {
        "experiment": "mirror",
        "run_name": run_name,
        "tsv_path": str(tsv_path),
        "tsv_copy": str(run_dir / "prompts.tsv"),
        "cells": cell_ids,
        "n_cells": len(cell_ids),
        "model": MODEL,
        "binary": BINARY,
        "seed": SEED,
        "max_new_tokens": MAX_NEW_TOKENS,
        "ctx": CTX,
        "intervention": "none",
        "routing_only": True,
        "timestamp": datetime.utcnow().isoformat(),
        "output_structure": {
            "capture_dir": "<run_dir>/capture/<cell_id>/",
            "router_tensors": "<cell_id>/router/ffn_moe_logits-<layer>.npy",
            "generated_text": "<cell_id>/generated_text.txt",
            "metadata": "<cell_id>/metadata.txt",
            "generated_tokens": "<cell_id>/generated_tokens.json",
            "prompt_tokens": "<cell_id>/prompt_tokens.json",
        },
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"Mirror experiment: {run_name}")
    print(f"  Cells: {cell_ids}")
    print(f"  TSV: {tsv_path}")
    print(f"  Model: {MODEL}")
    print(f"  Seed: {SEED}")
    print(f"  Max tokens: {MAX_NEW_TOKENS}")
    print(f"  Output: {run_dir}")
    print()

    rc = run_mirror(tsv_path, run_dir)
    if rc != 0:
        print(f"ERROR: capture binary returned {rc}", file=sys.stderr)
        sys.exit(rc)

    # Verify outputs exist — require metadata, generated text, and exactly 40 router tensors per cell
    capture_dir = run_dir / "capture"
    found = []
    degraded = []
    missing = []
    for cell_id in cell_ids:
        cell_dir = capture_dir / cell_id
        has_meta = (cell_dir / "metadata.txt").exists()
        has_text = (cell_dir / "generated_text.txt").exists()
        router_dir = cell_dir / "router"
        n_layers = len(list(router_dir.glob("ffn_moe_logits-*.npy"))) if router_dir.exists() else 0
        if has_meta and has_text and n_layers == EXPECTED_ROUTER_LAYERS:
            found.append((cell_id, n_layers))
        elif has_meta or has_text or router_dir.exists():
            degraded.append((cell_id, has_meta, has_text, n_layers))
        else:
            missing.append(cell_id)

    print(f"\nCapture complete -> {capture_dir}")
    print(
        f"  OK: {len(found)}/{len(cell_ids)} cells "
        f"(metadata + text + exactly {EXPECTED_ROUTER_LAYERS} router tensors)"
    )
    for cell_id, n_layers in found:
        print(f"    {cell_id}: {n_layers} layer files")
    if degraded:
        print("  DEGRADED:")
        for cell_id, has_meta, has_text, n_layers in degraded:
            print(
                f"    {cell_id}: metadata={has_meta} text={has_text} "
                f"router_layers={n_layers}/{EXPECTED_ROUTER_LAYERS}"
            )
    if missing:
        print(f"  MISSING: {missing}")

    if degraded or missing:
        print(
            "\nERROR: Incomplete capture set. Mirror shakedown/full run requires exactly "
            f"{EXPECTED_ROUTER_LAYERS} router files plus metadata and generated text for every cell.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check generated text exists for coherence review
    print(f"\nGenerated text for manual coherence check:")
    for cell_id, _ in found:
        gen_path = capture_dir / cell_id / "generated_text.txt"
        if gen_path.exists():
            text = gen_path.read_text()
            preview = text[:150].replace("\n", " ")
            print(f"  {cell_id}: {preview}...")
        else:
            print(f"  {cell_id}: NO generated_text.txt")

    print(f"\nManifest -> {run_dir / 'manifest.json'}")
    print(f"\nNext:")
    print(f"  1. Read generated text in {capture_dir}/*/generated_text.txt (manual coherence check)")
    print(f"  2. python mirror_analysis.py --captures {capture_dir} --output {run_dir / 'results'}")


if __name__ == "__main__":
    main()
