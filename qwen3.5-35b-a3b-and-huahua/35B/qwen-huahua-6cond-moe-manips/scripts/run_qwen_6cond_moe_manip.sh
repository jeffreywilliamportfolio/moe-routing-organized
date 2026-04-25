#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/workspace/consciousness-experiment/experiments/qwen-huahua-6cond-moe-manips}"
REPO_ROOT="${REPO_ROOT:-$(cd "$ROOT_DIR/../.." && pwd)}"
CAPTURE_BINARY="${CAPTURE_BINARY:-/workspace/consciousness-experiment/capture_activations}"
MODEL_PATH="${MODEL_PATH:-/workspace/models/qwen35-hauhau-q8/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf}"
PROMPT_TSV="${PROMPT_TSV:-$ROOT_DIR/prompts/qwen-6cond-moe-manip.tsv}"
PROMPT_BUILDER="${PROMPT_BUILDER:-$ROOT_DIR/scripts/build_qwen_6cond_moe_manip.py}"
PROMPT_SOURCE_TSV="${PROMPT_SOURCE_TSV:-$REPO_ROOT/prompts_l1l3_a_only_30.tsv}"
CAPTURE_CPP_SOURCE="${CAPTURE_CPP_SOURCE:-$ROOT_DIR/scripts/capture_activations.cpp}"
LLAMA_BUILD_BIN="${LLAMA_BUILD_BIN:-/workspace/llama.cpp.new/build/bin}"

RUN_LABEL="${RUN_LABEL:-hauhau_6cond_moe_manip}"
RAW_DIR="${RAW_DIR:-$ROOT_DIR/raw}"
RESULTS_DIR="${RESULTS_DIR:-$ROOT_DIR/results}"
N_PREDICT="${N_PREDICT:-1024}"
NGL="${NGL:-999}"
CTX="${CTX:-16384}"
THREADS="${THREADS:-16}"
FLASH_ATTN="${FLASH_ATTN:-on}"
CACHE_TYPE_K="${CACHE_TYPE_K:-q8_0}"
CACHE_TYPE_V="${CACHE_TYPE_V:-q8_0}"
SEED="${SEED:-42}"
EXPERT_BIAS="${EXPERT_BIAS:-}"

mkdir -p "$RAW_DIR" "$RESULTS_DIR"
export LD_LIBRARY_PATH="$LLAMA_BUILD_BIN:${LD_LIBRARY_PATH:-}"

now="$(date -u +%Y%m%dT%H%M%SZ)"
run_id="${now}_${RUN_LABEL}_gen_n${N_PREDICT}"
out_dir="$RAW_DIR/$run_id"
log_path="$RESULTS_DIR/${run_id}_capture.log"
cmd_path="$RESULTS_DIR/${run_id}_command.sh"
meta_path="$RESULTS_DIR/${run_id}_run_metadata.json"

mkdir -p "$out_dir"

{
  echo "#!/usr/bin/env bash"
  echo "set -euo pipefail"
  echo "export LD_LIBRARY_PATH=$LLAMA_BUILD_BIN:\${LD_LIBRARY_PATH:-}"
  printf '%q' "$CAPTURE_BINARY"
  printf ' -m %q --prompt-file %q -o %q' "$MODEL_PATH" "$PROMPT_TSV" "$out_dir"
  if [[ -n "$EXPERT_BIAS" ]]; then
    printf ' --expert-bias %q' "$EXPERT_BIAS"
  fi
  printf ' -n %q -ngl %q -c %q -t %q -fa %q --cache-type-k %q --cache-type-v %q --seed %q --temp 0 --top-k 1 --top-p 1 --min-p 0 --repeat-penalty 1 --mirostat 0 --routing-only --no-stream\n' \
    "$N_PREDICT" "$NGL" "$CTX" "$THREADS" "$FLASH_ATTN" "$CACHE_TYPE_K" "$CACHE_TYPE_V" "$SEED"
} > "$cmd_path"
chmod +x "$cmd_path"

python3 - <<PY
import hashlib
import json
import pathlib
import subprocess


def sha256_file(path):
    p = pathlib.Path(path)
    if not p.exists():
        return None
    digest = hashlib.sha256()
    with p.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


binary = pathlib.Path("$CAPTURE_BINARY")
model = pathlib.Path("$MODEL_PATH")
cmd = pathlib.Path("$cmd_path").read_text().strip()
version_proc = subprocess.run([str(binary), "--version"], capture_output=True, text=True)
version = "\n".join(
    part for part in (version_proc.stdout.strip(), version_proc.stderr.strip()) if part
).strip()

meta = {
    "run_id": "$run_id",
    "capture_binary": str(binary),
    "capture_binary_sha256": sha256_file(str(binary)),
    "capture_binary_version": version,
    "capture_cpp_source": "$CAPTURE_CPP_SOURCE",
    "capture_cpp_source_sha256": sha256_file("$CAPTURE_CPP_SOURCE"),
    "model_path": str(model),
    "model_sha256": sha256_file(str(model)),
    "prompt_tsv": "$PROMPT_TSV",
    "prompt_tsv_sha256": sha256_file("$PROMPT_TSV"),
    "prompt_builder": "$PROMPT_BUILDER",
    "prompt_builder_sha256": sha256_file("$PROMPT_BUILDER"),
    "prompt_source_tsv": "$PROMPT_SOURCE_TSV",
    "prompt_source_tsv_sha256": sha256_file("$PROMPT_SOURCE_TSV"),
    "output_dir": "$out_dir",
    "n_predict": int("$N_PREDICT"),
    "seed": int("$SEED"),
    "temp": 0,
    "top_k": 1,
    "top_p": 1,
    "min_p": 0,
    "repeat_penalty": 1,
    "mirostat": 0,
    "cache_type_k": "$CACHE_TYPE_K",
    "cache_type_v": "$CACHE_TYPE_V",
    "flash_attn": "$FLASH_ATTN",
    "ctx": int("$CTX"),
    "ngl": int("$NGL"),
    "threads": int("$THREADS"),
    "routing_only": True,
    "no_stream": True,
    "expert_bias": "$EXPERT_BIAS" or None,
    "command_script": "$cmd_path",
    "command": cmd,
}

pathlib.Path("$meta_path").write_text(json.dumps(meta, indent=2) + "\\n")
PY

echo "=== Running $run_id ==="
echo "Command: $cmd_path"
echo "Metadata: $meta_path"
bash "$cmd_path" 2>&1 | tee "$log_path"
