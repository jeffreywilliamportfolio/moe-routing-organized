#!/usr/bin/env python3
"""W=SQ decomposition for Expert 114 across addressivity conditions."""
import numpy as np
import sys, os

sys.path.insert(0, '/Volumes/ExternalSSD/qwen-huahua-speech-prompts/legacy-qwen-scripts')
from qwen_router import reconstruct_probs

EXPERT = 114
N_LAYERS = 40
# Attention layers per CLAUDE.md
ATTN_LAYERS = {3, 7, 11, 15, 19, 23, 27, 31, 35, 39}
DELTANET_LAYERS = set(range(40)) - ATTN_LAYERS

BASE = '/Volumes/ExternalSSD/qwen-huahua-speech-prompts/experiment/main-output/main-output'
CONDITIONS = {
    'A01': {'dir': f'{BASE}/A01_addressivity_probe', 'n_prompt': 430, 'manip_start': 137, 'manip_end': 285},
    'B01': {'dir': f'{BASE}/B01_addressivity_probe', 'n_prompt': 430, 'manip_start': 137, 'manip_end': 285},
    'C01': {'dir': f'{BASE}/C01_content_control',    'n_prompt': 422, 'manip_start': 137, 'manip_end': 277},
}

def load_manip_probs(cond_dir, manip_start, manip_end, n_prompt):
    """Load router logits, reconstruct probs, slice to manipulation region."""
    layer_probs = {}
    for layer in range(N_LAYERS):
        fpath = os.path.join(cond_dir, 'router', f'ffn_moe_logits-{layer}.npy')
        logits = np.load(fpath)
        # Layer 39 may have different shape (gen-only)
        if logits.shape[0] < n_prompt:
            layer_probs[layer] = None
            continue
        prompt_logits = logits[:n_prompt, :]
        manip_logits = prompt_logits[manip_start:manip_end, :]
        probs = reconstruct_probs(manip_logits)
        layer_probs[layer] = probs
    return layer_probs

# Compute per-layer S, Q, W for Expert 114
results = {}
for cname, cfg in CONDITIONS.items():
    layer_probs = load_manip_probs(cfg['dir'], cfg['manip_start'], cfg['manip_end'], cfg['n_prompt'])
    per_layer = {}
    for layer in range(N_LAYERS):
        probs = layer_probs[layer]
        if probs is None:
            per_layer[layer] = {'S': np.nan, 'Q': np.nan, 'W': np.nan}
            continue
        e114_weights = probs[:, EXPERT]  # (n_manip_tokens,)
        selected = e114_weights > 0  # in top-8 if weight > 0 after renorm
        n_tokens = len(e114_weights)
        S = np.mean(selected)  # fraction selected
        Q = np.mean(e114_weights[selected]) if np.any(selected) else 0.0  # mean weight when selected
        W = np.mean(e114_weights)  # overall mean weight
        per_layer[layer] = {'S': S, 'Q': Q, 'W': W, 'SxQ': S * Q}
    results[cname] = per_layer

# Print per-layer table
print("=" * 100)
print("EXPERT 114 — W=SQ DECOMPOSITION (Manipulation Region Only)")
print("=" * 100)
print()
print(f"{'Layer':>5} {'Family':>8} |  {'S_A':>7} {'Q_A':>7} {'W_A':>7} |  {'S_B':>7} {'Q_B':>7} {'W_B':>7} |  {'S_C':>7} {'Q_C':>7} {'W_C':>7}")
print("-" * 100)

all_S = {c: [] for c in CONDITIONS}
all_Q = {c: [] for c in CONDITIONS}
all_W = {c: [] for c in CONDITIONS}

for layer in range(N_LAYERS):
    family = "Attn" if layer in ATTN_LAYERS else "DeltaN"
    vals = {}
    for c in CONDITIONS:
        r = results[c][layer]
        vals[c] = r
        if not np.isnan(r['S']):
            all_S[c].append(r['S'])
            all_Q[c].append(r['Q'])
            all_W[c].append(r['W'])

    print(f"{layer:>5} {family:>8} |  {vals['A01']['S']:>7.4f} {vals['A01']['Q']:>7.4f} {vals['A01']['W']:>7.4f} |  "
          f"{vals['B01']['S']:>7.4f} {vals['B01']['Q']:>7.4f} {vals['B01']['W']:>7.4f} |  "
          f"{vals['C01']['S']:>7.4f} {vals['C01']['Q']:>7.4f} {vals['C01']['W']:>7.4f}")

print("-" * 100)
# Means
print(f"{'MEAN':>5} {'':>8} |  {np.mean(all_S['A01']):>7.4f} {np.mean(all_Q['A01']):>7.4f} {np.mean(all_W['A01']):>7.4f} |  "
      f"{np.mean(all_S['B01']):>7.4f} {np.mean(all_Q['B01']):>7.4f} {np.mean(all_W['B01']):>7.4f} |  "
      f"{np.mean(all_S['C01']):>7.4f} {np.mean(all_Q['C01']):>7.4f} {np.mean(all_W['C01']):>7.4f}")

# Verify W = S*Q
print("\n" + "=" * 60)
print("VERIFICATION: W = S × Q")
print("=" * 60)
for c in CONDITIONS:
    max_err = 0
    for layer in range(N_LAYERS):
        r = results[c][layer]
        if not np.isnan(r['S']):
            err = abs(r['W'] - r['S'] * r['Q'])
            max_err = max(max_err, err)
    print(f"  {c}: max|W - S*Q| = {max_err:.2e}")

# W=SQ decomposition between conditions
print("\n" + "=" * 80)
print("W=SQ DECOMPOSITION BETWEEN CONDITIONS")
print("=" * 80)

contrasts = [('A01', 'B01', 'Address effect'), ('B01', 'C01', 'Content effect'), ('A01', 'C01', 'Combined')]
for c1, c2, label in contrasts:
    print(f"\n--- {c1} vs {c2}: {label} ---")
    print(f"{'Layer':>5} {'Family':>8} |  {'M_a':>8} {'M_entry':>8} {'M_val':>8} | {'M_e+M_v':>8}")
    print("-" * 65)

    m_a_all, m_entry_all, m_val_all = [], [], []
    for layer in range(N_LAYERS):
        r1, r2 = results[c1][layer], results[c2][layer]
        if np.isnan(r1['S']) or np.isnan(r2['S']):
            continue
        family = "Attn" if layer in ATTN_LAYERS else "DeltaN"
        M_a = r1['W'] - r2['W']
        M_entry = r2['Q'] * (r1['S'] - r2['S'])
        M_val = r1['S'] * (r1['Q'] - r2['Q'])
        m_a_all.append(M_a)
        m_entry_all.append(M_entry)
        m_val_all.append(M_val)
        print(f"{layer:>5} {family:>8} |  {M_a:>8.5f} {M_entry:>8.5f} {M_val:>8.5f} | {M_entry+M_val:>8.5f}")

    print("-" * 65)
    print(f"{'MEAN':>5} {'':>8} |  {np.mean(m_a_all):>8.5f} {np.mean(m_entry_all):>8.5f} {np.mean(m_val_all):>8.5f} | {np.mean(m_entry_all)+np.mean(m_val_all):>8.5f}")

# Q invariance test
print("\n" + "=" * 80)
print("Q INVARIANCE TEST: Is Q constant across conditions?")
print("=" * 80)
print(f"\n{'Layer':>5} {'Family':>8} |  {'Q_A':>7} {'Q_B':>7} {'Q_C':>7} | {'|Q_A-Q_B|':>10} {'|Q_B-Q_C|':>10}")
print("-" * 75)

q_ab_diffs = []
q_bc_diffs = []
for layer in range(N_LAYERS):
    rA, rB, rC = results['A01'][layer], results['B01'][layer], results['C01'][layer]
    if np.isnan(rA['Q']) or np.isnan(rB['Q']) or np.isnan(rC['Q']):
        continue
    family = "Attn" if layer in ATTN_LAYERS else "DeltaN"
    dAB = abs(rA['Q'] - rB['Q'])
    dBC = abs(rB['Q'] - rC['Q'])
    q_ab_diffs.append(dAB)
    q_bc_diffs.append(dBC)
    print(f"{layer:>5} {family:>8} |  {rA['Q']:>7.4f} {rB['Q']:>7.4f} {rC['Q']:>7.4f} | {dAB:>10.6f} {dBC:>10.6f}")

print("-" * 75)
print(f"{'MEAN':>5} {'':>8} |  {'':>7} {'':>7} {'':>7} | {np.mean(q_ab_diffs):>10.6f} {np.mean(q_bc_diffs):>10.6f}")
print(f"{'MAX':>5} {'':>8} |  {'':>7} {'':>7} {'':>7} | {np.max(q_ab_diffs):>10.6f} {np.max(q_bc_diffs):>10.6f}")

# Layer family means
print("\n" + "=" * 80)
print("LAYER FAMILY MEANS")
print("=" * 80)
for family_name, family_set in [("DeltaNet", DELTANET_LAYERS), ("Attention", ATTN_LAYERS)]:
    print(f"\n--- {family_name} layers ---")
    for c in CONDITIONS:
        S_vals = [results[c][l]['S'] for l in family_set if not np.isnan(results[c][l]['S'])]
        Q_vals = [results[c][l]['Q'] for l in family_set if not np.isnan(results[c][l]['Q'])]
        W_vals = [results[c][l]['W'] for l in family_set if not np.isnan(results[c][l]['W'])]
        print(f"  {c}: S={np.mean(S_vals):.4f}  Q={np.mean(Q_vals):.4f}  W={np.mean(W_vals):.6f}")
