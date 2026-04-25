#!/usr/bin/env python3
"""
mirror_analysis.py

Post-run analysis for the mirror experiment.

Core idea:
- Load per-token, per-layer router captures for each run cell.
- Restrict to generated tokens only.
- Reconstruct routed probabilities exactly and consistently.
- Compute Expert 114 stats by condition and level.
- Compute the exact mirror metric M_a between true_self and shuffled.
- Support both a three-cell shakedown and the full 18-cell matrix via
  explicit --levels / --conditions filters.
- Decompose results per layer first, then summarize by layer family.

This script is conservative:
- It does NOT assume every capture file is already in routed-probability form.
- It does NOT assume all conditions have the same number of experts or layers.
- It only computes M_a for shape-compatible cells.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


EXPERT_114 = 114
TOP_K_DEFAULT = 8
LEVELS = ["L1", "L2", "L3"]
CONDITIONS = [
    "true_self",
    "shuffled",
    "stranger",
    "suppressed_twin",
    "static_control",
    "null_control",
]


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - np.max(x, axis=axis, keepdims=True)
    ex = np.exp(x)
    return ex / np.sum(ex, axis=axis, keepdims=True)


def ensure_3d(arr: np.ndarray) -> np.ndarray:
    if arr.ndim != 3:
        raise ValueError(f"Expected 3D tensor (tokens, layers, experts), got shape {arr.shape}")
    return arr


def round_float(x: float, ndigits: int = 6) -> float:
    return round(float(x), ndigits)


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def parse_int_list(s: Optional[str]) -> Optional[List[int]]:
    if not s:
        return None
    return [int(x.strip()) for x in s.split(",") if x.strip()]


# ---------------------------------------------------------------------
# Layer family helpers
# ---------------------------------------------------------------------

def get_layer_families(
    n_layers: int,
    attention_layers_override: Optional[List[int]] = None,
    deltanet_layers_override: Optional[List[int]] = None,
) -> Tuple[List[int], List[int]]:
    """
    For Hauhau Qwen3.5-35B-A3B:
      attention layers = 3,7,11,15,19,23,27,31,35,39
      deltanet layers = all others in 0..39

    If overrides are provided, use them.
    If n_layers != 40 and no overrides are provided, return empty families.
    """
    if attention_layers_override is not None or deltanet_layers_override is not None:
        attn = attention_layers_override or []
        delta = deltanet_layers_override or []
        return delta, attn

    if n_layers == 40:
        attn = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39]
        delta = [i for i in range(40) if i not in attn]
        return delta, attn

    return [], []


# ---------------------------------------------------------------------
# Capture loading
# ---------------------------------------------------------------------

def load_router_tensors(cell_dir: Path, n_gen: Optional[int] = None) -> np.ndarray:
    """
    Load per-layer router logits from the capture binary's output structure:
        cell_dir/router/ffn_moe_logits-0.npy   shape (n_tokens, n_experts)
        cell_dir/router/ffn_moe_logits-1.npy   shape (n_tokens, n_experts)
        ...

    Returns (n_gen, n_layers, n_experts) by extracting the last n_gen tokens
    from each layer and stacking on axis=1.

    Some layers (e.g., the final attention layer in hybrid DeltaNet/Attention
    architectures) may capture fewer prompt tokens than others, resulting in
    different total token counts per layer.  All layers share the same generated
    tokens at the tail, so extracting the last n_gen tokens from each layer
    aligns them correctly.

    If n_gen is None and all layers have the same token count, falls back to
    returning the full tensor.
    """
    if not cell_dir.exists():
        raise FileNotFoundError(f"Cell directory not found: {cell_dir}")

    router_dir = cell_dir / "router"
    if not router_dir.exists():
        raise FileNotFoundError(f"Router subdirectory not found: {router_dir}")

    files = sorted(
        router_dir.glob("ffn_moe_logits-*.npy"),
        key=lambda p: int(p.stem.split("-")[1]),
    )
    if not files:
        raise FileNotFoundError(f"No ffn_moe_logits-*.npy files in {router_dir}")

    layers_raw = [np.load(f) for f in files]
    token_counts = [arr.shape[0] for arr in layers_raw]

    if len(set(token_counts)) == 1 and n_gen is None:
        # All layers match — original fast path
        return ensure_3d(np.stack(layers_raw, axis=1))

    # Layers have different token counts; extract the last n_gen tokens from each.
    if n_gen is None:
        raise ValueError(
            f"Token counts vary across layers {dict(zip([f.name for f in files], token_counts))} "
            f"and n_gen was not provided — cannot align."
        )

    for i, arr in enumerate(layers_raw):
        if arr.shape[0] < n_gen:
            raise ValueError(
                f"Layer {i} ({files[i].name}) has {arr.shape[0]} tokens, "
                f"fewer than n_gen={n_gen}"
            )

    layers_aligned = [arr[-n_gen:] for arr in layers_raw]
    return ensure_3d(np.stack(layers_aligned, axis=1))


def parse_metadata_txt(path: Path) -> Dict[str, str]:
    """Parse key=value metadata.txt written by the capture binary."""
    meta: Dict[str, str] = {}
    if not path.exists():
        return meta
    for line in path.read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            meta[key.strip()] = value.strip()
    return meta


def load_generation_mask(cell_dir: Path, n_tokens: int) -> np.ndarray:
    """
    Generated-token mask.  Marks generated tokens as True, prompt tokens as False.

    The capture binary writes metadata.txt with n_tokens_prompt=N.
    Generated tokens start at index n_tokens_prompt.
    """
    meta = parse_metadata_txt(cell_dir / "metadata.txt")
    n_prompt_str = meta.get("n_tokens_prompt")
    if n_prompt_str is not None:
        n_prompt = int(n_prompt_str)
        mask = np.zeros(n_tokens, dtype=bool)
        mask[n_prompt:] = True
        return mask

    raise ValueError(
        f"metadata.txt not found or missing n_tokens_prompt in {cell_dir}. "
        f"Cannot determine generation boundary — refusing to default to all-True."
    )


# ---------------------------------------------------------------------
# Routing reconstruction
# ---------------------------------------------------------------------

def reconstruct_routed_probs(
    raw: np.ndarray,
    capture_format: str,
    top_k: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns:
      routed_probs: (tokens, layers, experts) with top-k renormalized routed probabilities
      selected_mask: (tokens, layers, experts) boolean

    capture_format:
      - logits: raw router logits over all experts
      - dense_probs: dense softmax probs over all experts
      - routed_probs: already sparse/top-k-routed weights over experts
    """
    raw = ensure_3d(raw)

    if capture_format == "logits":
        dense = softmax(raw, axis=2)
    elif capture_format == "dense_probs":
        dense = raw.astype(np.float64, copy=False)
        row_sums = np.sum(dense, axis=2, keepdims=True)
        if not np.allclose(row_sums, 1.0, atol=1e-3):
            raise ValueError("capture_format=dense_probs but rows do not sum to ~1")
    elif capture_format == "routed_probs":
        routed = raw.astype(np.float64, copy=False)
        selected = routed > 0
        row_sums = np.sum(routed, axis=2, keepdims=True)
        routed = np.divide(routed, row_sums, out=np.zeros_like(routed), where=row_sums > 0)
        return routed, selected
    else:
        raise ValueError(f"Unknown capture_format: {capture_format}")

    top_idx = np.argpartition(-dense, kth=top_k - 1, axis=2)[:, :, :top_k]
    selected = np.zeros_like(dense, dtype=bool)
    np.put_along_axis(selected, top_idx, True, axis=2)

    routed = np.where(selected, dense, 0.0)
    row_sums = np.sum(routed, axis=2, keepdims=True)
    routed = np.divide(routed, row_sums, out=np.zeros_like(routed), where=row_sums > 0)
    return routed, selected


# ---------------------------------------------------------------------
# Core stats
# ---------------------------------------------------------------------

def compute_expert_stats(
    routed_probs: np.ndarray,
    selected_mask: np.ndarray,
    generated_mask: np.ndarray,
    expert_id: int,
    deltanet_layers: List[int],
    attention_layers: List[int],
) -> Dict[str, Any]:
    """
    W = mean routed weight over generated token-layer pairs
    S = selection rate over generated token-layer pairs
    Q = mean routed weight conditional on selection over generated token-layer pairs

    All stats are computed on generated tokens only.
    """
    n_tokens, n_layers, n_experts = routed_probs.shape

    if expert_id >= n_experts:
        return {"error": f"expert {expert_id} out of range for n_experts={n_experts}"}

    if generated_mask.shape != (n_tokens,):
        raise ValueError(f"generated_mask shape {generated_mask.shape} != ({n_tokens},)")

    probs_gen = routed_probs[generated_mask]
    sel_gen = selected_mask[generated_mask]

    if probs_gen.shape[0] == 0:
        return {"error": "no generated tokens after masking"}

    ew = probs_gen[:, :, expert_id]
    es = sel_gen[:, :, expert_id]

    W = float(np.mean(ew))
    S = float(np.mean(es))
    Q = float(np.mean(ew[es])) if np.any(es) else 0.0

    per_layer_weight = np.mean(ew, axis=0)
    per_layer_selection = np.mean(es, axis=0)
    per_layer_Q = []
    for layer_idx in range(n_layers):
        mask = es[:, layer_idx]
        per_layer_Q.append(float(np.mean(ew[:, layer_idx][mask])) if np.any(mask) else 0.0)

    result: Dict[str, Any] = {
        "n_generated_tokens": int(probs_gen.shape[0]),
        "n_layers": int(n_layers),
        "n_experts": int(n_experts),
        "W": round_float(W),
        "S": round_float(S, 6),
        "Q": round_float(Q),
        "n_selected_pairs": int(np.sum(es)),
        "n_total_pairs": int(es.size),
        "W_reconstructed_from_SQ": round_float(S * Q),
        "per_layer_weight": [round_float(x) for x in per_layer_weight],
        "per_layer_selection": [round_float(x, 6) for x in per_layer_selection],
        "per_layer_Q": [round_float(x) for x in per_layer_Q],
    }

    if deltanet_layers:
        result["deltanet_mean_weight"] = round_float(np.mean(per_layer_weight[deltanet_layers]))
        result["deltanet_mean_selection"] = round_float(np.mean(per_layer_selection[deltanet_layers]), 6)
    if attention_layers:
        result["attention_mean_weight"] = round_float(np.mean(per_layer_weight[attention_layers]))
        result["attention_mean_selection"] = round_float(np.mean(per_layer_selection[attention_layers]), 6)
    if n_layers > 20:
        result["layer20_weight"] = round_float(per_layer_weight[20])
        result["layer20_selection"] = round_float(per_layer_selection[20], 6)

    return result


# ---------------------------------------------------------------------
# Mirror metric
# ---------------------------------------------------------------------

def compute_mirror_metric(
    true_stats: Dict[str, Any],
    shuffled_stats: Dict[str, Any],
    deltanet_layers: Optional[List[int]] = None,
    attention_layers: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    Exact decomposition:
      W = S * Q

      M_total = W_true - W_shuf
              = Q_shuf * (S_true - S_shuf) + S_true * (Q_true - Q_shuf)

      So:
        M_entry = Q_shuf * ΔS
        M_val   = S_true * ΔQ

    This sums exactly to M_total.
    """
    if "error" in true_stats or "error" in shuffled_stats:
        return {"error": "missing or invalid stats"}

    W_t, S_t, Q_t = true_stats["W"], true_stats["S"], true_stats["Q"]
    W_s, S_s, Q_s = shuffled_stats["W"], shuffled_stats["S"], shuffled_stats["Q"]

    M_total = W_t - W_s
    M_entry = Q_s * (S_t - S_s)
    M_val = S_t * (Q_t - Q_s)

    per_layer_M = [
        round_float(t - s)
        for t, s in zip(true_stats["per_layer_weight"], shuffled_stats["per_layer_weight"])
    ]

    out: Dict[str, Any] = {
        "M_total": round_float(M_total),
        "M_entry": round_float(M_entry),
        "M_val": round_float(M_val),
        "reconstruction_error": round_float(M_total - (M_entry + M_val), 10),
        "true_self_W": W_t,
        "shuffled_W": W_s,
        "true_self_S": S_t,
        "shuffled_S": S_s,
        "true_self_Q": Q_t,
        "shuffled_Q": Q_s,
        "per_layer_M": per_layer_M,
    }

    if deltanet_layers:
        out["M_deltanet"] = round_float(np.mean([per_layer_M[i] for i in deltanet_layers]))
    if attention_layers:
        out["M_attn"] = round_float(np.mean([per_layer_M[i] for i in attention_layers]))
    if len(per_layer_M) > 20:
        out["M_layer20"] = round_float(per_layer_M[20])

    return out


# ---------------------------------------------------------------------
# Run-cell analysis
# ---------------------------------------------------------------------

def analyze_run_cell(
    run_dir: Path,
    capture_format: str,
    top_k: int,
    expert_id: int,
    attention_layers_override: Optional[List[int]],
    deltanet_layers_override: Optional[List[int]],
) -> Dict[str, Any]:
    # Determine n_gen from metadata so we can align layers with different token counts
    meta = parse_metadata_txt(run_dir / "metadata.txt")
    n_prompt = int(meta["n_tokens_prompt"])
    n_gen_str = meta.get("n_tokens_generated")
    if n_gen_str is not None:
        n_gen = int(n_gen_str)
    else:
        # Infer from the majority layer token count
        router_dir = run_dir / "router"
        first_layer = np.load(sorted(router_dir.glob("ffn_moe_logits-*.npy"))[0])
        n_gen = first_layer.shape[0] - n_prompt

    raw = load_router_tensors(run_dir, n_gen=n_gen)
    n_tokens, n_layers, _ = raw.shape
    # All tokens in raw are now generated tokens — mask is all-True
    gen_mask = np.ones(n_tokens, dtype=bool)
    routed_probs, selected_mask = reconstruct_routed_probs(raw, capture_format, top_k)

    delta_layers, attn_layers = get_layer_families(
        n_layers,
        attention_layers_override=attention_layers_override,
        deltanet_layers_override=deltanet_layers_override,
    )

    stats = compute_expert_stats(
        routed_probs=routed_probs,
        selected_mask=selected_mask,
        generated_mask=gen_mask,
        expert_id=expert_id,
        deltanet_layers=delta_layers,
        attention_layers=attn_layers,
    )
    stats["capture_format"] = capture_format
    stats["top_k"] = top_k
    stats["generation_mask_coverage"] = round_float(float(np.mean(gen_mask)), 6)
    stats["deltanet_layers"] = delta_layers
    stats["attention_layers"] = attn_layers
    return stats


# ---------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------

def compute_condition_comparisons(stats_by_condition: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    if "true_self" in stats_by_condition and "shuffled" in stats_by_condition:
        ts = stats_by_condition["true_self"]
        sh = stats_by_condition["shuffled"]
        if (
            "error" not in ts
            and "error" not in sh
            and ts["n_experts"] == sh["n_experts"]
            and ts["n_layers"] == sh["n_layers"]
        ):
            out["mirror"] = compute_mirror_metric(
                ts,
                sh,
                deltanet_layers=ts.get("deltanet_layers", []),
                attention_layers=ts.get("attention_layers", []),
            )

    for other in ["stranger", "suppressed_twin", "static_control", "null_control"]:
        if "true_self" in stats_by_condition and other in stats_by_condition:
            ts = stats_by_condition["true_self"]
            ot = stats_by_condition[other]
            if "error" not in ts and "error" not in ot:
                out[f"true_vs_{other}"] = {
                    "W_diff": round_float(ts["W"] - ot["W"]),
                    "S_diff": round_float(ts["S"] - ot["S"], 6),
                    "Q_diff": round_float(ts["Q"] - ot["Q"]),
                    "shape_compatible": bool(
                        ts["n_experts"] == ot["n_experts"] and ts["n_layers"] == ot["n_layers"]
                    ),
                }

    return out


def find_run_dir(captures_root: Path, level: str, cond: str) -> Optional[Path]:
    """
    Expects:
      captures/L1_true_self
    Matches the TSV prompt ID used by the capture binary as the output directory name.
    """
    candidate = captures_root / f"{level}_{cond}"
    if candidate.exists():
        return candidate
    return None


def run_analysis(args: argparse.Namespace) -> None:
    captures_root = Path(args.captures)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    attention_override = parse_int_list(args.attention_layers)
    deltanet_override = parse_int_list(args.deltanet_layers)

    selected_levels = parse_csv_list(args.levels)
    selected_conditions = parse_csv_list(args.conditions)

    all_results: Dict[str, Any] = {
        "_analysis_scope": {
            "levels": selected_levels,
            "conditions": selected_conditions,
            "capture_format": args.capture_format,
            "top_k": args.top_k,
            "expert_id": args.expert_id,
        }
    }

    for level in selected_levels:
        print("\n" + "=" * 72)
        print(f"Level: {level}")
        print("=" * 72)

        stats_by_condition: Dict[str, Any] = {}

        for cond in selected_conditions:
            run_dir = find_run_dir(captures_root, level, cond)
            if run_dir is None:
                print(f"  {cond:<16} missing")
                continue

            print(f"  {cond:<16} -> {run_dir}")
            try:
                stats = analyze_run_cell(
                    run_dir=run_dir,
                    capture_format=args.capture_format,
                    top_k=args.top_k,
                    expert_id=args.expert_id,
                    attention_layers_override=attention_override,
                    deltanet_layers_override=deltanet_override,
                )
            except Exception as e:
                stats = {"error": str(e)}

            stats_by_condition[cond] = stats

            if "error" in stats:
                print(f"    ERROR: {stats['error']}")
            else:
                print(
                    f"    W={stats['W']:.6f} "
                    f"S={stats['S']:.6f} "
                    f"Q={stats['Q']:.6f} "
                    f"gen_cov={stats['generation_mask_coverage']:.6f}"
                )
                if "deltanet_mean_weight" in stats:
                    print(f"    DeltaNet={stats['deltanet_mean_weight']:.6f}")
                if "attention_mean_weight" in stats:
                    print(f"    Attention={stats['attention_mean_weight']:.6f}")
                if "layer20_weight" in stats:
                    print(f"    Layer20={stats['layer20_weight']:.6f}")

        comparisons = compute_condition_comparisons(stats_by_condition)
        all_results[level] = {"stats": stats_by_condition, "comparisons": comparisons}

        if "mirror" in comparisons:
            m = comparisons["mirror"]
            print("\n  MIRROR")
            print(f"    M_total   = {m['M_total']:.6f}")
            print(f"    M_entry   = {m['M_entry']:.6f}")
            print(f"    M_val     = {m['M_val']:.6f}")
            if "M_deltanet" in m:
                print(f"    M_deltanet= {m['M_deltanet']:.6f}")
            if "M_attn" in m:
                print(f"    M_attn    = {m['M_attn']:.6f}")
            if "M_layer20" in m:
                print(f"    M_layer20 = {m['M_layer20']:.6f}")
            print(f"    recon_err = {m['reconstruction_error']:.10f}")

    out_path = output_dir / "mirror_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "=" * 72)
    print("SUMMARY: mirror metric by level")
    print("=" * 72)
    print(f"{'Level':<6} {'M_total':>10} {'M_entry':>10} {'M_val':>10} {'M_delta':>10} {'M_attn':>10} {'M_L20':>10}")
    print("-" * 72)
    for level in selected_levels:
        m = all_results.get(level, {}).get("comparisons", {}).get("mirror")
        if m:
            print(
                f"{level:<6} "
                f"{m['M_total']:>10.6f} "
                f"{m['M_entry']:>10.6f} "
                f"{m['M_val']:>10.6f} "
                f"{m.get('M_deltanet', float('nan')):>10.6f} "
                f"{m.get('M_attn', float('nan')):>10.6f} "
                f"{m.get('M_layer20', float('nan')):>10.6f}"
            )
        else:
            print(f"{level:<6} {'N/A':>10}")

    print(f"\nResults written to {out_path}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mirror experiment analysis")
    parser.add_argument("--captures", required=True, help="Root captures directory from mirror.py")
    parser.add_argument("--output", required=True, help="Directory for analysis outputs")
    parser.add_argument(
        "--capture-format",
        choices=["logits", "dense_probs", "routed_probs"],
        required=True,
        help="Format of the stored router tensors",
    )
    parser.add_argument("--top-k", type=int, default=TOP_K_DEFAULT, help="Top-k routed experts")
    parser.add_argument("--expert-id", type=int, default=EXPERT_114, help="Expert to analyze")
    parser.add_argument(
        "--levels",
        default=",".join(LEVELS),
        help="Comma-separated levels to analyze, e.g. 'L3' or 'L1,L2,L3'",
    )
    parser.add_argument(
        "--conditions",
        default=",".join(CONDITIONS),
        help="Comma-separated conditions to analyze, e.g. 'true_self,shuffled,null_control'",
    )
    parser.add_argument(
        "--attention-layers",
        default=None,
        help="Comma-separated attention layer indices override, e.g. '3,7,11,15,19,23,27,31,35,39'",
    )
    parser.add_argument(
        "--deltanet-layers",
        default=None,
        help="Comma-separated DeltaNet layer indices override",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    run_analysis(args)


if __name__ == "__main__":
    main()