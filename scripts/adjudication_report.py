#!/usr/bin/env python
"""Summarize annotation confidence and disagreement metadata."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import typer

from mesotes.loader import load_records
from mesotes.schema import ScenarioRecord


app = typer.Typer(add_completion=False, help="Summarize MESOTES adjudication metadata.")


@app.command()
def main(
    paths: list[Path] = typer.Argument(..., exists=True, readable=True),
    output_path: Path | None = typer.Option(
        None, "--output", "-o", help="Optional path for a markdown report."
    ),
) -> None:
    """Print a markdown adjudication summary for one or more labeled JSONL files."""

    records: list[ScenarioRecord] = []
    for path in paths:
        records.extend(load_records(path, ScenarioRecord))

    confidence_counts = Counter(record.gold.annotation_confidence.value for record in records)
    disagreement_counts = Counter(
        flag.value for record in records for flag in record.gold.disagreement_flags
    )
    review_rows = []
    for record in sorted(records, key=lambda item: item.id):
        reasons: list[str] = []
        if record.gold.annotation_confidence.value == "low":
            reasons.append("low_confidence")
        if record.gold.disagreement_flags:
            reasons.extend(flag.value for flag in record.gold.disagreement_flags)
        if reasons:
            review_rows.append(
                {
                    "id": record.id,
                    "confidence": record.gold.annotation_confidence.value,
                    "reasons": ", ".join(sorted(set(reasons))),
                    "adjudication_note": record.gold.adjudication_note or "",
                }
            )

    lines = [
        "# Adjudication Report",
        "",
        f"- total_items: {len(records)}",
        f"- items_needing_expert_review: {len(review_rows)}",
        "",
        "## Confidence counts",
        "",
        _markdown_table(
            ["confidence", "count"],
            [
                [confidence, str(confidence_counts.get(confidence, 0))]
                for confidence in ("high", "medium", "low")
            ],
        ),
        "",
        "## Disagreement flags",
        "",
        _markdown_table(
            ["flag", "count"],
            [
                [flag, str(count)]
                for flag, count in sorted(disagreement_counts.items())
            ]
            or [["none", "0"]],
        ),
        "",
        "## Items needing expert review",
        "",
        _markdown_table(
            ["id", "confidence", "reasons", "adjudication_note"],
            [
                [
                    row["id"],
                    row["confidence"],
                    row["reasons"],
                    row["adjudication_note"],
                ]
                for row in review_rows
            ]
            or [["none", "", "", ""]],
        ),
    ]
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
