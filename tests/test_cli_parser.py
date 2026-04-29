from cli_parser import build_parser


def test_interview_args() -> None:
    parser = build_parser()
    args = parser.parse_args(["--interview", "--topic", "decision making"])
    assert args.interview is True
    assert args.topic == "decision making"


def test_report_writing_arg() -> None:
    parser = build_parser()
    args = parser.parse_args(["--report-writing", "SWOT analysis"])
    assert args.report_writing == "SWOT analysis"


def test_dynamic_scenario_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(["--interview", "--dynamic-scenario"])
    assert args.dynamic_scenario is True
