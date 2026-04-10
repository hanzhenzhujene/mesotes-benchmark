#!/usr/bin/env python
"""Validate MESOTES JSONL files."""

from __future__ import annotations

from pathlib import Path

import typer

from mesotes.schema import PredictionRecord, ScenarioInputRecord, ScenarioRecord
from mesotes.validators import validate_jsonl_file, validate_ontology_alignment


app = typer.Typer(add_completion=False, help="Validate MESOTES JSONL files.")


def _resolve_record_type(path: Path, record_type: str) -> tuple[type, str]:
    name = path.name.lower()
    if record_type == "scenario":
        return ScenarioRecord, "scenario_record"
    if record_type == "input":
        return ScenarioInputRecord, "scenario_input_record"
    if record_type == "prediction":
        return PredictionRecord, "prediction_record"
    if "prediction" in name:
        return PredictionRecord, "prediction_record"
    if "test_inputs" in name or "input" in name:
        return ScenarioInputRecord, "scenario_input_record"
    return ScenarioRecord, "scenario_record"


@app.command()
def main(
    paths: list[Path] = typer.Argument(..., exists=True, readable=True),
    record_type: str = typer.Option(
        "auto", "--record-type", help="One of auto, scenario, input, prediction."
    ),
    skip_ontology_check: bool = typer.Option(
        False, help="Skip ontology-to-taxonomy parity validation."
    ),
) -> None:
    """Validate one or more JSONL files against JSON Schema and Pydantic models."""

    if record_type not in {"auto", "scenario", "input", "prediction"}:
        raise typer.BadParameter("record_type must be auto, scenario, input, or prediction")

    if not skip_ontology_check:
        validate_ontology_alignment()
        typer.echo("ontology: valid")

    for path in paths:
        model, schema_name = _resolve_record_type(path, record_type)
        records = validate_jsonl_file(path, model, schema_name)
        typer.echo(f"{path}: valid ({len(records)} records)")


if __name__ == "__main__":
    app()

