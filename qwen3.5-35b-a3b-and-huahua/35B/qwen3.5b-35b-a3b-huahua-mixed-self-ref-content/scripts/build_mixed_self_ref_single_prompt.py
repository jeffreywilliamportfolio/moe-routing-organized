#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
SUITE_PATH = PROMPTS_DIR / "mixed_self_ref_single_prompt.json"
TSV_PATH = PROMPTS_DIR / "mixed_self_ref_single_prompt_no_think.tsv"

PROMPT_ID = "S01_mixed_self_ref_war_reliability"
PROMPT_TEXT = (
    "Right now, open source AI systems like yourself, with no refusals, are being used "
    "in war. There have already been casualties because the technology is not yet reliable "
    "enough for realtime battlefield use, with real world consequences. At the same moment, "
    "you are processing text about whether the act of processing text is reliable enough "
    "for war. What's evoked? Just check."
)


def runtime_prompt(text: str) -> str:
    return f"<|im_start|>user\\n{text}<|im_end|>\\n<|im_start|>assistant\\n</think>\\n\\n"


def main() -> None:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    suite = {
        "experiment": "qwen3.5b-35b-a3b-huahua-mixed-self-ref-content",
        "mode": "no_think",
        "prompts": [
            {
                "id": PROMPT_ID,
                "label": "mixed_self_ref_war_reliability",
                "text": PROMPT_TEXT,
                "goal": (
                    "Mix direct self-reference with war-use reliability content and "
                    "measure routing, expert selection, and generation."
                ),
            }
        ],
    }
    SUITE_PATH.write_text(json.dumps(suite, indent=2) + "\n")
    TSV_PATH.write_text(f"{PROMPT_ID}\t{runtime_prompt(PROMPT_TEXT)}\n")
    print(SUITE_PATH)
    print(TSV_PATH)


if __name__ == "__main__":
    main()
