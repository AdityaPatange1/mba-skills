from __future__ import annotations

import json
import random
from pathlib import Path
from typing import TYPE_CHECKING, Any

from domain import ScenarioPlan

if TYPE_CHECKING:
    from ollama_cloud_client import OllamaCloudClient

DATA_FILE = Path(__file__).resolve().parent / "data" / "scenario_bank.json"


def _load_bank() -> dict[str, Any]:
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


BANK = _load_bank()
MBA_TOPICS: list[str] = BANK["mba_topics"]

BASE_SCENARIO_PLANS: list[ScenarioPlan] = [
    ScenarioPlan(
        name=item["name"],
        context=item["context"],
        competencies=item["competencies"],
        stressor=item["stressor"],
        evaluation_focus=item.get("evaluation_focus", []),
    )
    for item in BANK["base_scenarios"]
]

SCENARIO_TEMPLATE_DIMENSIONS: dict[str, list[str]] = BANK["scenario_template_dimensions"]
MCQ_QUESTION_SETS: list[dict[str, Any]] = BANK["mcq_question_sets"]


def _template_count() -> int:
    dims = SCENARIO_TEMPLATE_DIMENSIONS
    return (
        len(dims["industries"])
        * len(dims["business_challenges"])
        * len(dims["geographies"])
        * len(dims["time_horizons"])
    )


def total_scenarios() -> int:
    return len(BASE_SCENARIO_PLANS) + _template_count()


def random_topic() -> str:
    return random.choice(MBA_TOPICS)


def random_question_set() -> dict[str, Any]:
    return random.choice(MCQ_QUESTION_SETS)


def _generated_scenario() -> ScenarioPlan:
    dims = SCENARIO_TEMPLATE_DIMENSIONS
    industry = random.choice(dims["industries"])
    challenge = random.choice(dims["business_challenges"])
    geography = random.choice(dims["geographies"])
    horizon = random.choice(dims["time_horizons"])
    competencies = random.sample(dims["competency_pool"], k=3)
    evaluation_focus = random.sample(dims["evaluation_focus_pool"], k=3)

    return ScenarioPlan(
        name=f"{industry} {challenge} ({geography})",
        context=(
            f"You lead a {industry.lower()} business in {geography}. "
            f"The organization faces {challenge.lower()} over the next {horizon.lower()}."
        ),
        competencies=competencies,
        stressor=(
            f"Leadership expects measurable progress in {horizon.lower()} "
            "despite constrained resources and competing priorities."
        ),
        evaluation_focus=evaluation_focus,
    )


def random_scenario() -> ScenarioPlan:
    if random.random() < 0.25:
        return random.choice(BASE_SCENARIO_PLANS)
    return _generated_scenario()


def dynamic_scenario_from_model(client: OllamaCloudClient, topic: str) -> ScenarioPlan:
    prompt = (
        "Return ONLY valid JSON for an MBA interview scenario with keys: "
        "name, context, competencies, stressor, evaluation_focus. "
        "competencies and evaluation_focus must be arrays of 3 short strings each. "
        f"Topic: {topic}"
    )
    response = client.chat(
        [
            {"role": "system", "content": "You generate valid JSON only."},
            {"role": "user", "content": prompt},
        ]
    )
    try:
        parsed = json.loads(response)
        return ScenarioPlan(
            name=str(parsed["name"]).strip(),
            context=str(parsed["context"]).strip(),
            competencies=[str(x).strip() for x in parsed["competencies"]][:3],
            stressor=str(parsed["stressor"]).strip(),
            evaluation_focus=[str(x).strip() for x in parsed["evaluation_focus"]][:3],
        )
    except Exception:
        return _generated_scenario()
