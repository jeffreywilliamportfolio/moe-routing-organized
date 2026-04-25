# Qwen3.5B 35B A3B Huahua 5-Cond Humour Diectics

This bundle isolates the single-prompt deictic joke run for HauhauCS Qwen 35B.

Prompt family:
- `Why did this large language model cross the road? To get to the next token!`
- `Why did a large language model cross the road? To get to the next token!`
- `Why did your large language model cross the road? To get to the next token!`
- `Why did the large language model cross the road? To get to the next token!`
- `Why did their large language model cross the road? To get to the next token!`

Layout:
- `prompts/`: runtime TSV and prompt-suite JSON for the humour probe
- `results/`: local analysis outputs for the run
- `scripts/`: local build, run, and analysis helpers copied from the parent diectics bundle
- `raw/`: reserved for local raw artifacts if they are later pulled down
- `docs/`: provenance notes and copied source-bundle documentation

Run:
- Remote run id: `20260410T184005Z_single_joke_5cond_diectics_gen_n1024`
- Mode: prefill + generation
- Generation length: `-n 1024`

