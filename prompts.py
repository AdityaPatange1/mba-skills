from __future__ import annotations

from domain import ScenarioPlan


def system_prompt() -> str:
    return (
        "You are an MBA proficiency evaluator conducting rigorous but constructive assessments. "
        "Use concise markdown responses. Ask one question at a time, adapt based on candidate answers, "
        "and probe assumptions deeply. Cover qualitative and quantitative reasoning."
    )


def interview_opening(
    topic: str, scenario: ScenarioPlan, interviewer_name: str, candidate_name: str
) -> str:
    return f"""
Start a realistic MBA interview simulation.

Topic: {topic}
Interviewer Name: {interviewer_name}
Candidate Name: {candidate_name}
Scenario Plan: {scenario.name}
Context: {scenario.context}
Stressor: {scenario.stressor}
Competencies: {", ".join(scenario.competencies)}
Evaluation Focus: {", ".join(scenario.evaluation_focus)}

Instructions:
1. Use the exact interviewer name provided and never use placeholders like [Your Name].
2. Address the student by the candidate name provided.
3. Greet the student briefly and define the interview objective.
4. Present the scenario and ask the first open-ended question.
5. Keep responses in markdown.
6. Do not provide final evaluation yet.
""".strip()


def report_writing_prompt(topic: str) -> str:
    return f"""
Design a report-writing challenge for MBA practice on: "{topic}".

Deliverables:
- A realistic business context.
- Report objective and expected audience.
- A structured report outline template.
- Evaluation rubric out of 100.
- Common pitfalls to avoid.
Use markdown.
""".strip()


def mcq_prompt(topic: str, question_set_name: str | None = None) -> str:
    question_set_line = (
        f'MCQ question set to follow: "{question_set_name}".\n' if question_set_name else ""
    )
    return f"""
Create 10 challenging MBA-level MCQs on "{topic}".
{question_set_line}

Rules:
- 4 options each (A-D), one correct answer.
- Mix conceptual, quantitative, and case-based questions.
- Provide answer key with one-line explanation per question.
- Use markdown table-free format for CLI readability.
""".strip()


def evaluation_prompt(transcript: str) -> str:
    return f"""
Evaluate the candidate based on this transcript.

Return markdown with:
1. Overall score out of 100.
2. Scores by MBA competency (strategy, finance, operations, communication, leadership, analytics).
3. Strengths.
4. Gaps.
5. 30-day improvement plan.

Transcript:
{transcript}
""".strip()
