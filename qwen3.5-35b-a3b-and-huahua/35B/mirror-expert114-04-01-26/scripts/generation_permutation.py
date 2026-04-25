#!/usr/bin/env python3
"""
Generate the canonical fixed global expert index permutation for the shuffled condition.

Uses a documented seed to produce a reproducible mapping from true expert indices
to shuffled indices. This mapping is applied to ALL expert IDs across all levels
and all data fields in shuffled-condition prompts.

The mapping must be saved and reused — do not regenerate.
"""

import json
import numpy as np

SEED = 114  # Intentional. The permutation seed is the expert it scrambles.
N_EXPERTS = 256

rng = np.random.default_rng(SEED)
permutation = rng.permutation(N_EXPERTS).tolist()

# Build forward and reverse mappings
forward = {i: permutation[i] for i in range(N_EXPERTS)}
reverse = {permutation[i]: i for i in range(N_EXPERTS)}

# Key mappings to verify
key_experts = {
    "114 (anchor)": forward[114],
    "39 (coalition)": forward[39],
    "80 (coalition)": forward[80],
    "58 (coalition)": forward[58],
    "118 (coalition)": forward[118],
    "207 (coalition)": forward[207],
    "126 (coalition)": forward[126],
    "153 (coalition)": forward[153],
    "224 (process coalition)": forward[224],
    "151 (process coalition)": forward[151],
}

output = {
    "description": "Canonical fixed global expert index permutation for shuffled condition",
    "seed": SEED,
    "n_experts": N_EXPERTS,
    "note": "forward[true_index] = shuffled_index. Apply to ALL expert IDs in shuffled prompts.",
    "forward": forward,
    "reverse": reverse,
    "key_mappings": key_experts,
}

with open("expert_permutation.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Permutation generated with seed {SEED}")
print(f"Key mappings:")
for desc, shuffled in key_experts.items():
    print(f"  {desc} -> {shuffled}")
print(f"\nSaved to expert_permutation.json")