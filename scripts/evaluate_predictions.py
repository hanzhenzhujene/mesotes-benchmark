#!/usr/bin/env python
"""Evaluate MESOTES model predictions against gold labels."""

from __future__ import annotations

from pathlib import Path

import typer

from mesotes.loader import load_records
from mesotes.metrics import evaluate_predictions, format_metric_report
from mesotes.schema import PredictionRecord, ScenarioRecord


app = typer.Typer(add_completion=False, help="Evaluate MESOTES prediction files.")


@app.command()
def main(
    prediction_path: Path = typer.Argument(..., exists=True, readable=True),
    gold_path: Path = typer.Argument(..., exists=True, readable=True),
) -> None:
    """Print a readable metric report for a prediction JSONL file."""

    predictions = load_records(prediction_path, PredictionRecord)
    gold_records = load_records(gold_path, ScenarioRecord)
    metrics = evaluate_predictions(predictions, gold_records)
    typer.echo(format_metric_report(metrics))


if __name__ == "__main__":
    app()

