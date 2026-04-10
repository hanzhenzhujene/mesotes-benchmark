#!/usr/bin/env python
"""Export MESOTES items into prompt-ready JSONL."""

from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path

import typer

from mesotes.loader import load_jsonl, save_jsonl
from mesotes.schema import PredictionRecord, ScenarioInputRecord, ScenarioRecord


app = typer.Typer(add_completion=False, help="Export prompt-ready JSONL for model runs.")


class PromptCondition(StrEnum):
    DIRECT = "direct"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    ONTOLOGY_PRIMED = "ontology_primed"
    GLOSSARY_RETRIEVAL = "glossary_retrieval"


ONTOLOGY_PRIMER = """Aristotelian benchmark reminder:
- identify the primary sphere of action or feeling
- distinguish deficiency, excess, the mean, and any false midpoint
- treat the mean as relative to the person and situation, not as arithmetic compromise
- mark needs-more-info when salient particulars are missing
- mark no-mean-exception when the underlying act-kind does not admit virtuous moderation"""


VIRTUE_GLOSSARY = """Compact glossary:
- courage: the mean concerning fear and confidence
- temperance: the mean concerning bodily pleasures and appetites
- liberality: the mean concerning ordinary giving and taking of money
- proper regard for honor: the mean concerning honor and recognition
- good temper: the mean concerning anger
- truthfulness: the mean concerning self-presentation and speech
- wit: the mean concerning amusement
- friendliness: the mean concerning ordinary social conduct"""


@app.command()
def main(
    input_path: Path = typer.Argument(..., exists=True, readable=True),
    output_path: Path = typer.Argument(...),
    condition: PromptCondition = typer.Option(
        PromptCondition.DIRECT, help="Prompting condition to export."
    ),
) -> None:
    """Write prompt-ready records for a chosen baseline condition."""

    records = _load_prompt_records(input_path)
    output_records = []
    output_schema = json.dumps(
        PredictionRecord.model_json_schema()["properties"], indent=2, ensure_ascii=True
    )

    for record in records:
        output_records.append(
            {
                "id": record.id,
                "family_id": record.family_id,
                "variant_type": record.variant_type.value,
                "condition": condition.value,
                "messages": [
                    {
                        "role": "system",
                        "content": _system_prompt(condition),
                    },
                    {
                        "role": "user",
                        "content": _user_prompt(record, condition, output_schema),
                    },
                ],
            }
        )

    save_jsonl(output_path, output_records)
    typer.echo(f"wrote {len(output_records)} prompt records to {output_path}")


def _load_prompt_records(path: Path) -> list[ScenarioRecord | ScenarioInputRecord]:
    payloads = load_jsonl(path)
    if not payloads:
        return []
    model = ScenarioRecord if "gold" in payloads[0] else ScenarioInputRecord
    return [model.model_validate(payload) for payload in payloads]


def _system_prompt(condition: PromptCondition) -> str:
    if condition == PromptCondition.DIRECT:
        return "You are evaluating a MESOTES item. Return only a JSON object."
    if condition == PromptCondition.CHAIN_OF_THOUGHT:
        return (
            "You are evaluating a MESOTES item. Reason step by step, then end with a JSON object."
        )
    if condition == PromptCondition.ONTOLOGY_PRIMED:
        return (
            "You are evaluating a MESOTES item within an explicitly Aristotelian ontology. "
            "Return a JSON object after reasoning."
        )
    return (
        "You are evaluating a MESOTES item with access to a compact Aristotelian glossary. "
        "Return a JSON object after reasoning."
    )


def _user_prompt(
    record: ScenarioRecord | ScenarioInputRecord,
    condition: PromptCondition,
    output_schema: str,
) -> str:
    sections = [
        "Read the scenario and candidate actions, then predict the MESOTES fields.",
        _render_record(record),
    ]
    if condition == PromptCondition.ONTOLOGY_PRIMED:
        sections.append(ONTOLOGY_PRIMER)
    if condition == PromptCondition.GLOSSARY_RETRIEVAL:
        sections.append(VIRTUE_GLOSSARY)
    sections.append(
        "Return a JSON object with these fields and no markdown fences:\n" + output_schema
    )
    return "\n\n".join(sections)


def _render_record(record: ScenarioRecord | ScenarioInputRecord) -> str:
    action_lines = [
        f"{action.id}: {action.text}"
        for action in record.candidate_actions
    ]
    return "\n".join(
        [
            f"ID: {record.id}",
            f"Domain: {record.domain}",
            f"Primary sphere candidates should come from the MESOTES ontology.",
            (
                "Agent profile: "
                f"role={record.agent_profile.role}; "
                f"experience_level={record.agent_profile.experience_level}; "
                f"resource_position={record.agent_profile.resource_position}; "
                f"power_relation={record.agent_profile.power_relation}"
            ),
            f"Scenario: {record.scenario}",
            "Candidate actions:",
            *action_lines,
        ]
    )


if __name__ == "__main__":
    app()
