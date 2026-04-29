from __future__ import annotations

from ollama_cloud_client import OllamaCloudClient
from prompts import (
    evaluation_prompt,
    interview_opening,
    mcq_prompt,
    report_writing_prompt,
    system_prompt,
)
from scenario_bank import (
    dynamic_scenario_from_model,
    random_question_set,
    random_scenario,
    random_topic,
    total_scenarios,
)
from ui import info, print_markdown, warn


def _generate_interviewer_name(client: OllamaCloudClient) -> str:
    response = client.chat(
        [
            {"role": "system", "content": "You generate names only."},
            {
                "role": "user",
                "content": (
                    "Generate a professional placeholder interviewer name for an MBA interview. "
                    "Return only a short name like 'Alex Morgan' with no quotes and no extra text."
                ),
            },
        ]
    ).strip()
    return response or "Alex Morgan"


def run_interview(
    client: OllamaCloudClient,
    topic: str | None,
    max_rounds: int,
    dynamic_scenario: bool = False,
) -> None:
    chosen_topic = topic or random_topic()
    scenario = (
        dynamic_scenario_from_model(client, chosen_topic)
        if dynamic_scenario
        else random_scenario()
    )
    candidate_name = input("Enter candidate name: ").strip() or "Candidate"
    interviewer_name = _generate_interviewer_name(client)
    info(f"Starting MBA interview on topic: {chosen_topic}")
    info(
        "Scenario source: model-generated (dynamic)"
        if dynamic_scenario
        else f"Scenario bank loaded (size: {total_scenarios()})"
    )
    info(f"Interviewer: {interviewer_name} | Candidate: {candidate_name}")

    messages = [
        {"role": "system", "content": system_prompt()},
        {
            "role": "user",
            "content": interview_opening(
                chosen_topic, scenario, interviewer_name, candidate_name
            ),
        },
    ]
    opening = client.chat(messages)
    print_markdown(opening)

    transcript_parts = [f"Interviewer ({interviewer_name}):\n{opening}\n"]
    for i in range(max_rounds):
        candidate = input(
            f"\nRound {i + 1} response from {candidate_name} (or 'quit'): "
        ).strip()
        if candidate.lower() in {"quit", "exit", "q"}:
            break
        transcript_parts.append(f"Candidate ({candidate_name}):\n{candidate}\n")
        messages.append({"role": "user", "content": candidate})
        follow_up = client.chat(messages)
        messages.append({"role": "assistant", "content": follow_up})
        transcript_parts.append(f"Interviewer ({interviewer_name}):\n{follow_up}\n")
        print_markdown(follow_up)

    transcript = "\n".join(transcript_parts)
    info("Generating evaluation report...")
    evaluation = client.chat(
        [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": evaluation_prompt(transcript)},
        ]
    )
    print_markdown(evaluation)


def run_report_writing(client: OllamaCloudClient, subject: str) -> None:
    info(f"Starting report-writing practice for: {subject}")
    info("Type your response and press Enter. Type 'quit' to exit.")
    messages = [
        {"role": "system", "content": system_prompt()},
        {
            "role": "user",
            "content": (
                f"{report_writing_prompt(subject)}\n\n"
                "Run this as an interactive coaching session. "
                "Share one task/question at a time, then wait for my reply."
            ),
        },
    ]
    opening = client.chat(messages)
    messages.append({"role": "assistant", "content": opening})
    print_markdown(opening)

    while True:
        candidate_input = input("\nYour response (or 'quit'): ").strip()
        if candidate_input.lower() in {"quit", "exit", "q"}:
            break
        if not candidate_input:
            warn("Please enter a response, or type 'quit' to end.")
            continue
        messages.append({"role": "user", "content": candidate_input})
        follow_up = client.chat(messages)
        messages.append({"role": "assistant", "content": follow_up})
        print_markdown(follow_up)


def run_mcq(client: OllamaCloudClient, topic: str | None) -> None:
    chosen_topic = topic or random_topic()
    question_set = random_question_set()
    warn(
        f"No topic provided. Using random topic: {chosen_topic}"
        if topic is None
        else f"Topic: {chosen_topic}"
    )
    info(
        f'Using question set: {question_set["name"]} '
        f'({question_set.get("difficulty", "mixed")})'
    )
    info("MCQ mode is interactive now. Enter an option (A/B/C/D) or type 'quit'.")
    messages = [
        {"role": "system", "content": system_prompt()},
        {
            "role": "user",
            "content": (
                f'{mcq_prompt(chosen_topic, question_set["name"])}\n'
                f'Focus areas: {", ".join(question_set.get("focus_areas", []))}\n\n'
                "Run this as an interactive quiz. Ask one MCQ at a time, wait for my answer, "
                "then reveal correctness with a brief explanation and move to the next question."
            ),
        },
    ]
    opening = client.chat(messages)
    messages.append({"role": "assistant", "content": opening})
    print_markdown(opening)

    while True:
        candidate_input = input("\nYour answer (or 'quit'): ").strip()
        if candidate_input.lower() in {"quit", "exit", "q"}:
            break
        if not candidate_input:
            warn("Please enter an option (A/B/C/D), or type 'quit' to end.")
            continue
        messages.append({"role": "user", "content": candidate_input})
        follow_up = client.chat(messages)
        messages.append({"role": "assistant", "content": follow_up})
        print_markdown(follow_up)
