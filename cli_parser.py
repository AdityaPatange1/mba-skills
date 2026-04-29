from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mba_skills",
        description="Conversational MBA proficiency evaluator with Ollama Cloud.",
    )
    parser.add_argument("--topic", type=str, default=None, help="Interview/MCQ topic.")
    parser.add_argument("--model", type=str, default=None, help="Override Ollama model.")
    parser.add_argument("--max-rounds", type=int, default=5, help="Interview rounds.")
    parser.add_argument(
        "--dynamic-scenario",
        action="store_true",
        help="Load interview scenario dynamically from the Ollama model.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--interview", action="store_true", help="Start interactive interview.")
    group.add_argument(
        "--report-writing",
        type=str,
        metavar="SUBJECT",
        help="Generate a report-writing challenge for a given subject.",
    )
    group.add_argument("--mcq", action="store_true", help="Generate MCQ assessment.")
    return parser
