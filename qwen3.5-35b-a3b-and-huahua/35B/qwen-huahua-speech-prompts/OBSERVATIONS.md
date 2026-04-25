# OBSERVATIONS.md

Non-breaking, non-critical notes collected during experiment setup and execution.

## 2026-04-02 — Workspace Setup

### Build path drift
- CLAUDE.md specifies `/workspace/llama.cpp.new/build/bin/` (from yesterday's data-injection run)
- workspace-setup agent built at `/workspace/src/llama.cpp/build-cuda/bin/`
- Both are fresh b8493 clones; naming is cosmetic. Step 10 cp must use actual path.
- No prebuilt llama.cpp on this Docker image (unlike yesterday's) — no `/opt/llama.cpp/cuda-12.8/VERSION.txt`.

### Docker image difference
- Yesterday (data-injection): image had prebuilt llama.cpp at `/opt/llama.cpp/cuda-12.8/` with `VERSION.txt`
- Today (addressivity): `pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel` — no prebuilt. Clone from scratch required.

### LD_LIBRARY_PATH not needed on this image
- workspace-setup Step 11 exports build-cuda/bin to LD_LIBRARY_PATH
- On this Docker image (pytorch:2.6.0-cuda12.6), all shared libs resolve from system paths
- `ldd capture_activations` shows no missing libraries without the export
- Non-issue but noted for reproducibility on different images

### workspace-setup agent silent for 20+ minutes
- Steps 1-11 completed successfully (build done, binary copied, runs correctly)
- Stalled at Step 12 (model download) — model directory created but empty
- Likely blocked on HF download URL or token. Agent may need intervention.

### Model download failures
- `huggingface-cli` not on PATH after pip install (exit 127) — shell didn't refresh PATH
- `python3 -m huggingface_hub.commands.huggingface_cli` — old huggingface_hub version on pytorch image lacks `.commands` module
- Fell back to plain `wget -c` from HuggingFace CDN — 401 (repo is gated)
- wget with bearer token — 404 (wrong URL pattern for GGUF repo)
- Python API `hf_hub_download()` works but user wants CLI consistency with prior runs
- **Fix**: CLI binary is at `/opt/conda/bin/hf` (not `huggingface-cli`) on this pytorch image. Use `hf download` (newer alias).
- First partial download (2.2GB) stalled silently with no process left running

### CRITICAL: CUDA build had no GPU backend
- workspace-setup agent auto-detected `compute_120a` (Blackwell) but CUDA 12.6 only supports up to `compute_90`
- nvcc silently failed on all ggml-cuda .cu files — `nvcc fatal: Unsupported gpu architecture 'compute_120a'`
- Result: capture binary linked CPU-only (libggml-base, libggml-cpu — no libggml-cuda, no libllama.so)
- Binary would have run inference entirely on CPU — unusably slow for 35B model
- **Fix**: Full rebuild with `-DCMAKE_CUDA_ARCHITECTURES=90`. PTX JIT at runtime handles Blackwell via compute_90.
- Mission-control initially reported binary "detects both 5090s" — this was ggml_cuda_init succeeding (driver-level), not the compute kernels being available
- **Root cause**: workspace-setup agent Step 8 used cmake auto-detection which picked up the GPU's native arch, not what nvcc supports

### workspace-setup agent had stale b8123
- Agent definition shipped with `b8123` in Step 5. Corrected to `b8493` before launch.
- Root cause: agent was authored without checking data-injection project's actual build tag.
