from __future__ import annotations

from mesotes.loader import load_records
from mesotes.metrics import (
    evaluate_predictions,
    family_consistency_score,
    nuisance_invariance_score,
    salience_responsiveness_score,
)
from mesotes.schema import PredictionRecord, ScenarioRecord
from conftest import PILOT_V2_DIR


def test_counterfactual_metrics_on_pilot_v2_mock_predictions() -> None:
    predictions = load_records(PILOT_V2_DIR / "mock_predictions.jsonl", PredictionRecord)
    gold_records = load_records(PILOT_V2_DIR / "test_labels.jsonl", ScenarioRecord)

    assert nuisance_invariance_score(predictions, gold_records) == 1.0
    assert salience_responsiveness_score(predictions, gold_records) == 2 / 3
    assert family_consistency_score(predictions, gold_records) == 0.75

    metrics = evaluate_predictions(predictions, gold_records)
    assert metrics["nuisance_invariance_score"] == 1.0
    assert metrics["salience_responsiveness_score"] == 2 / 3
    assert metrics["family_consistency_score"] == 0.75
