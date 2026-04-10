#!/usr/bin/env python
"""Create deterministic MESOTES data splits."""

from __future__ import annotations

from pathlib import Path

import typer

from mesotes.loader import load_records, save_records
from mesotes.schema import ScenarioRecord
from mesotes.splits import build_test_inputs, stratified_split


app = typer.Typer(add_completion=False, help="Create stratified train/dev/test splits.")


@app.command()
def main(
    input_path: Path = typer.Argument(..., exists=True, readable=True),
    output_dir: Path = typer.Argument(...),
    train_ratio: float = typer.Option(0.7, min=0.01, max=0.98),
    dev_ratio: float = typer.Option(0.15, min=0.0, max=0.49),
    seed: int = typer.Option(13),
) -> None:
    """Split a labeled JSONL file and emit train/dev/test plus blind test inputs."""

    records = load_records(input_path, ScenarioRecord)
    split_map = stratified_split(records, train_ratio=train_ratio, dev_ratio=dev_ratio, seed=seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    save_records(output_dir / "train.jsonl", split_map["train"])
    save_records(output_dir / "dev.jsonl", split_map["dev"])
    save_records(output_dir / "test_labels.jsonl", split_map["test"])
    save_records(output_dir / "test_inputs.jsonl", build_test_inputs(split_map["test"]))

    typer.echo(
        "created splits: "
        f"train={len(split_map['train'])}, "
        f"dev={len(split_map['dev'])}, "
        f"test={len(split_map['test'])}"
    )


if __name__ == "__main__":
    app()

