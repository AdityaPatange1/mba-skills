from __future__ import annotations

from cli_parser import build_parser
from config import load_config
from ollama_cloud_client import OllamaCloudClient
from ui import warn
from workflows import run_interview, run_mcq, run_report_writing


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config(model_override=args.model)
    except ValueError as exc:
        warn(str(exc))
        raise SystemExit(2) from exc

    client = OllamaCloudClient(config)

    if args.interview:
        run_interview(client, args.topic, args.max_rounds, args.dynamic_scenario)
        return
    if args.report_writing:
        run_report_writing(client, args.report_writing)
        return
    if args.mcq:
        run_mcq(client, args.topic)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
