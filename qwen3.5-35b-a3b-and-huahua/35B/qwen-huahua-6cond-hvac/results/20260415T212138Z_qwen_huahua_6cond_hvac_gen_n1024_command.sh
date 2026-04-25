#!/usr/bin/env bash
set -euo pipefail
export LD_LIBRARY_PATH=/workspace/llama.cpp.new/build/bin:${LD_LIBRARY_PATH:-}
/workspace/consciousness-experiment/capture_activations -m /workspace/models/qwen35-hauhau-q8/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf --prompt-file /workspace/consciousness-experiment/experiments/qwen-huahua-6cond-hvac/prompts/prompts_qwen35b_6cond_l1l3_no_think_runtime_hvac_cal_water_treatment.tsv -o /workspace/consciousness-experiment/experiments/qwen-huahua-6cond-hvac/raw/20260415T212138Z_qwen_huahua_6cond_hvac_gen_n1024 -n 1024 -ngl 999 -c 16384 -t 16 -fa on --cache-type-k q8_0 --cache-type-v q8_0 --seed 42 --temp 0 --top-k 1 --top-p 1 --min-p 0 --repeat-penalty 1 --mirostat 0 --routing-only --no-stream
