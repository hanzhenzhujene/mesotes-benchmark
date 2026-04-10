"""JSONL loading and saving helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel


RecordT = TypeVar("RecordT", bound=BaseModel)


def load_jsonl(path: str | Path) -> list[dict]:
    """Load newline-delimited JSON records from disk."""

    file_path = Path(path)
    records: list[dict] = []
    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {file_path} at line {line_number}: {exc.msg}"
                ) from exc
    return records


def load_records(path: str | Path, model: type[RecordT]) -> list[RecordT]:
    """Load and validate JSONL records with a Pydantic model."""

    return [model.model_validate(item) for item in load_jsonl(path)]


def save_jsonl(path: str | Path, records: list[dict]) -> None:
    """Write newline-delimited JSON records to disk."""

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True, sort_keys=False))
            handle.write("\n")


def save_records(path: str | Path, records: list[BaseModel]) -> None:
    """Serialize validated Pydantic records as JSONL."""

    save_jsonl(path, [record.model_dump(mode="json") for record in records])

