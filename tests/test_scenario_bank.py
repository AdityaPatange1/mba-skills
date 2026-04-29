from scenario_bank import random_question_set, random_scenario, total_scenarios


def test_total_scenarios_is_large() -> None:
    assert total_scenarios() > 10000


def test_random_scenario_has_required_fields() -> None:
    scenario = random_scenario()
    assert scenario.name
    assert scenario.context
    assert len(scenario.competencies) >= 3
    assert scenario.stressor


def test_random_question_set_has_name() -> None:
    question_set = random_question_set()
    assert "name" in question_set
    assert question_set["name"]
