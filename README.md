# MBA Skills Interview CLI

A production-style Python CLI for evaluating MBA proficiency through conversational simulations powered by Ollama Cloud.

It supports:
- Interactive interview simulations (open-ended, adaptive questioning)
- Report-writing challenge generation
- MBA-level MCQ generation
- Markdown-first terminal rendering with `rich`
- Environment-based secure configuration via `python-dotenv`

## Why this project

This project is designed for MBA prep, mentoring, and self-assessment where students need broad, scenario-driven testing beyond static quizzes.

The assistant uses multi-natured business contexts (strategy, finance, operations, leadership, analytics) and can evaluate candidate responses with competency-level feedback.

## Features

- **Open-ended interview mode** with random topic fallback
- **Scenario plans** with stressors and competency focus
- **JSON-backed scenario and question-set bank** with 10,000+ generated scenario combinations
- **Report-writing prompts** with structure and rubric expectations
- **MCQ generation** across conceptual, quantitative, and case styles
- **Dynamic scenario loading** from Ollama model (`--dynamic-scenario`)
- **Post-interview evaluation** with score and improvement plan
- **Clean architecture** split by concern (config, prompts, workflows, client, UI)
- **Automation support** through a `Makefile` (`build`, `lint`, `test`, `validate`, `run`)

## Project structure

```text
.
├── mba_skills.py            # CLI entrypoint
├── cli_parser.py            # Argument parsing and command modes
├── config.py                # .env loading and validated runtime config
├── domain.py                # Core domain dataclasses
├── scenario_bank.py         # Topics and interview scenario plans
├── data/scenario_bank.json  # Scenario and MCQ question-set source data
├── prompts.py               # Prompt templates for each workflow
├── ollama_cloud_client.py   # Ollama Cloud chat client wrapper
├── workflows.py             # Interview/report/mcq orchestration
├── ui.py                    # Rich-based markdown console rendering
├── tests/
│   ├── test_cli_parser.py   # CLI behavior tests
│   └── test_prompts.py      # Prompt content tests
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
├── Makefile                 # Build/lint/test/validate/run commands
└── LICENSE                  # MIT license
```

## Requirements

- Python 3.10+ (3.12 recommended)
- Ollama Cloud API key

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment setup

Create `.env` from template:

```bash
cp .env.example .env
```

Set values in `.env`:

```dotenv
OLLAMA_API_KEY=your_ollama_cloud_key_here
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_MODEL=llama3.1:8b-instruct-q8_0
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=800
```

### Environment variable reference

- `OLLAMA_API_KEY` (required): API key for Ollama Cloud authentication
- `OLLAMA_BASE_URL` (optional): API host, default `https://ollama.com`
- `OLLAMA_MODEL` (optional): default model for chat requests
- `OLLAMA_TEMPERATURE` (optional): generation creativity control
- `OLLAMA_MAX_TOKENS` (optional): max generation length per response

## Usage

General help:

```bash
python mba_skills.py --help
```

### 1) Interview mode (interactive)

Random topic:

```bash
python mba_skills.py --interview
```

Specific topic:

```bash
python mba_skills.py --interview --topic "decision making"
```

Custom interview depth:

```bash
python mba_skills.py --interview --topic "corporate finance" --max-rounds 7
```

Use dynamic interview scenario generation from the model:

```bash
python mba_skills.py --interview --topic "corporate finance" --dynamic-scenario
```

### 2) Report-writing challenge mode

```bash
python mba_skills.py --report-writing "SWOT analysis"
```

### 3) MCQ mode

```bash
python mba_skills.py --mcq --topic "operations engineering"
```

If `--topic` is omitted in MCQ mode, a random MBA topic is selected.

### Optional model override at runtime

```bash
python mba_skills.py --interview --topic "leadership communication" --model "llama3.1:8b-instruct-q8_0"
```

## Makefile commands

Run all commands from project root:

```bash
make build      # Compile Python files
make lint       # Run Ruff linter
make test       # Run pytest suite
make validate   # lint + test
make run        # CLI help smoke check
make interview  # Quick interview command
make report     # Quick report-writing command
make mcq        # Quick MCQ command
```

## Testing and quality

- Linting: `ruff`
- Unit tests: `pytest`
- Validation pipeline: `make validate`

Recommended pre-commit routine:

```bash
make validate
```

## Design notes

- The app intentionally keeps a **single-script execution model** (`mba_skills.py`) while splitting responsibilities into reusable modules.
- Prompt templates are isolated in `prompts.py` for easy scenario and rubric evolution.
- Interview scenarios are centralized in `scenario_bank.py` for wide coverage and extensibility.
- Rendering is handled by `rich` so model output remains readable in markdown form.
- Secrets and runtime config are loaded via `.env` with safe defaults.

## Extending the project

Common extension points:

- Add more topics/scenarios/question sets in `data/scenario_bank.json`
- Add new assessment modes by extending parser + workflow
- Store interview transcripts and longitudinal performance analytics
- Add robust integration tests with mocked Ollama responses
- Add CI (GitHub Actions) for automated `make validate`

## Troubleshooting

- **`OLLAMA_API_KEY is required`**  
  Ensure `.env` exists and includes a valid `OLLAMA_API_KEY`.

- **Authentication/network errors**  
  Re-check `OLLAMA_BASE_URL`, API key validity, and outbound connectivity.

- **Model not available**  
  Provide a valid deployed model using `--model` or `OLLAMA_MODEL`.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

