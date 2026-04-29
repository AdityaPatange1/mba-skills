from domain import ScenarioPlan
from prompts import interview_opening, mcq_prompt


def test_interview_prompt_contains_topic_and_plan() -> None:
    scenario = ScenarioPlan(
        name="Test Plan",
        context="Context",
        competencies=["a", "b"],
        stressor="Stressor",
        evaluation_focus=["x"],
    )
    prompt = interview_opening("finance", scenario, "Alex Morgan", "Riya")
    assert "finance" in prompt
    assert "Test Plan" in prompt
    assert "Alex Morgan" in prompt
    assert "Riya" in prompt


def test_mcq_prompt_mentions_topic() -> None:
    prompt = mcq_prompt("operations")
    assert "operations" in prompt
