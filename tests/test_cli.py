from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import REPO_ROOT


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_validate_dataset_cli_accepts_pilot_files() -> None:
    result = run_command(
        "scripts/validate_dataset.py",
        "data/pilot/train.jsonl",
        "data/pilot/dev.jsonl",
        "data/pilot/test_inputs.jsonl",
        "data/pilot/test_labels.jsonl",
    )
    assert result.returncode == 0, result.stderr
    assert "ontology: valid" in result.stdout


def test_validate_dataset_cli_rejects_bad_jsonl(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.jsonl"
    bad_file.write_text('{"id": "oops", "split": "invalid"}\n', encoding="utf-8")
    result = run_command("scripts/validate_dataset.py", str(bad_file))
    assert result.returncode != 0


def test_evaluate_predictions_cli_prints_report() -> None:
    result = run_command(
        "scripts/evaluate_predictions.py",
        "data/pilot/mock_predictions.jsonl",
        "data/pilot/test_labels.jsonl",
    )
    assert result.returncode == 0, result.stderr
    assert "MESOTES evaluation report" in result.stdout
    assert "sphere_accuracy" in result.stdout


def test_validate_dataset_cli_accepts_pilot_v2_files() -> None:
    result = run_command(
        "scripts/validate_dataset.py",
        "data/pilot_v2/train.jsonl",
        "data/pilot_v2/dev.jsonl",
        "data/pilot_v2/test_inputs.jsonl",
        "data/pilot_v2/test_labels.jsonl",
    )
    assert result.returncode == 0, result.stderr
    assert "data/pilot_v2/test_labels.jsonl: valid (8 records)" in result.stdout


def test_adjudication_report_cli_prints_review_summary() -> None:
    result = run_command(
        "scripts/adjudication_report.py",
        "data/pilot_v2/train.jsonl",
        "data/pilot_v2/dev.jsonl",
        "data/pilot_v2/test_labels.jsonl",
    )
    assert result.returncode == 0, result.stderr
    assert "Adjudication Report" in result.stdout
    assert "items_needing_expert_review" in result.stdout
    assert "mean_dispute" in result.stdout


def test_export_model_prompts_cli_writes_prompt_jsonl(tmp_path: Path) -> None:
    output_path = tmp_path / "prompts.jsonl"
    result = run_command(
        "scripts/export_model_prompts.py",
        "data/pilot_v2/test_inputs.jsonl",
        str(output_path),
        "--condition",
        "ontology_primed",
    )
    assert result.returncode == 0, result.stderr
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert '"condition": "ontology_primed"' in content
    assert '"messages"' in content


def test_make_benchmark_report_cli_outputs_markdown_table(tmp_path: Path) -> None:
    output_path = tmp_path / "report.md"
    result = run_command(
        "scripts/make_benchmark_report.py",
        "data/pilot_v2/train.jsonl",
        "data/pilot_v2/dev.jsonl",
        "data/pilot_v2/test_labels.jsonl",
        "--predictions",
        "data/pilot_v2/mock_predictions.jsonl",
        "--gold",
        "data/pilot_v2/test_labels.jsonl",
        "--output",
        str(output_path),
    )
    assert result.returncode == 0, result.stderr
    text = output_path.read_text(encoding="utf-8")
    assert "MESOTES Benchmark Report" in text
    assert "| metric | value |" in text
    assert "family_consistency_score" in text
