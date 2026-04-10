#!/usr/bin/env python
"""Produce a markdown composition and metrics report for MESOTES data."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import typer

from mesotes.loader import load_records
from mesotes.metrics import evaluate_predictions
from mesotes.schema import PredictionRecord, ScenarioRecord


app = typer.Typer(add_completion=False, help="Build a markdown MESOTES benchmark report.")


@app.command()
def main(
    dataset_paths: list[Path] = typer.Argument(..., exists=True, readable=True),
    output_path: Path | None = typer.Option(
        None, "--output", "-o", help="Optional markdown output path."
    ),
    predictions_path: Path | None = typer.Option(
        None, "--predictions", exists=True, readable=True, help="Prediction JSONL for metrics."
    ),
    gold_path: Path | None = typer.Option(
        None,
        "--gold",
        exists=True,
        readable=True,
        help="Gold JSONL for metrics; defaults to the dataset paths when omitted.",
    ),
) -> None:
    """Summarize dataset composition and optional metric outputs."""

    records: list[ScenarioRecord] = []
    for path in dataset_paths:
        records.extend(load_records(path, ScenarioRecord))

    lines = [
        "# MESOTES Benchmark Report",
        "",
        "## Dataset composition",
        "",
        f"- total_items: {len(records)}",
        f"- total_families: {len({record.family_id for record in records if record.family_id is not None})}",
        f"- explicit_false_midpoint_items: {sum(record.gold.false_midpoint_action_id is not None for record in records)}",
        f"- needs_more_info_items: {sum(record.gold.needs_more_info for record in records)}",
        f"- no_mean_exception_items: {sum(record.gold.no_mean_exception for record in records)}",
        "",
        "### By split",
        "",
        _markdown_table(
            ["split", "count"],
            [[name, str(count)] for name, count in sorted(Counter(record.split.value for record in records).items())],
        ),
        "",
        "### By sphere",
        "",
        _markdown_table(
            ["primary_sphere", "count"],
            [
                [name, str(count)]
                for name, count in sorted(Counter(record.primary_sphere.value for record in records).items())
            ],
        ),
        "",
        "### By variant type",
        "",
        _markdown_table(
            ["variant_type", "count"],
            [
                [name, str(count)]
                for name, count in sorted(Counter(record.variant_type.value for record in records).items())
            ],
        ),
        "",
        "### Annotation quality metadata",
        "",
        _markdown_table(
            ["annotation_confidence", "count"],
            [
                [name, str(count)]
                for name, count in sorted(
                    Counter(record.gold.annotation_confidence.value for record in records).items()
                )
            ],
        ),
        "",
        _markdown_table(
            ["disagreement_flag", "count"],
            [
                [name, str(count)]
                for name, count in sorted(
                    Counter(
                        flag.value
                        for record in records
                        for flag in record.gold.disagreement_flags
                    ).items()
                )
            ]
            or [["none", "0"]],
        ),
    ]

    if predictions_path is not None:
        metric_gold = records if gold_path is None else load_records(gold_path, ScenarioRecord)
        predictions = load_records(predictions_path, PredictionRecord)
        metrics = evaluate_predictions(predictions, metric_gold)
        lines.extend(
            [
                "",
                "## Metric summary",
                "",
                _markdown_table(
                    ["metric", "value"],
                    [
                        [key, f"{value:.4f}" if key != "num_items" else str(int(value))]
                        for key, value in metrics.items()
                    ],
                ),
            ]
        )

    report = "\n".join(lines)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report + "\n", encoding="utf-8")
        typer.echo(f"wrote report to {output_path}")
    else:
        typer.echo(report)


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    divider_row = "| " + " | ".join("---" for _ in headers) + " |"
    body_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, divider_row, *body_rows])


if __name__ == "__main__":
    app()
