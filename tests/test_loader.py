from __future__ import annotations

from pathlib import Path

from mesotes.loader import load_jsonl, load_records, save_records
from mesotes.schema import ScenarioRecord

from conftest import PILOT_DIR


def test_round_trip_pilot_train_records(tmp_path: Path) -> None:
    source_path = PILOT_DIR / "train.jsonl"
    records = load_records(source_path, ScenarioRecord)
    round_trip_path = tmp_path / "round_trip.jsonl"
    save_records(round_trip_path, records)
    reloaded = load_records(round_trip_path, ScenarioRecord)
    assert [record.id for record in reloaded] == [record.id for record in records]
    assert len(load_jsonl(round_trip_path)) == len(records)
