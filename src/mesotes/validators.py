"""Validation helpers for ontology, JSON Schema, and JSONL datasets."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from collections.abc import Sequence
from pathlib import Path
from typing import TypeVar, cast

from jsonschema import ValidationError as JsonSchemaValidationError  # type: ignore[import-untyped]
from jsonschema import validate as validate_jsonschema  # type: ignore[import-untyped]
from pydantic import BaseModel, ValidationError as PydanticValidationError

from .loader import load_jsonl
from .schema import ScenarioInputRecord, ScenarioRecord
from .taxonomy import (
    advanced_module_values,
    core_sphere_values,
    explanation_tag_values,
    phronesis_salience_values,
    VariantType,
)


RecordT = TypeVar("RecordT", bound=BaseModel)

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ONTOLOGY_PATH = ROOT_DIR / "annotation" / "ontology.yaml"
DEFAULT_SCHEMA_DIR = ROOT_DIR / "data" / "schemas"


def load_ontology(path: str | Path = DEFAULT_ONTOLOGY_PATH) -> dict[str, list[str]]:
    """Load the lightweight YAML ontology file."""

    text = Path(path).read_text(encoding="utf-8")
    data: dict[str, list[str]] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not raw_line.startswith(" ") and stripped.endswith(":"):
            current_key = stripped[:-1]
            data[current_key] = []
            continue
        if raw_line.startswith("  - "):
            if current_key is None:
                raise ValueError("ontology.yaml contains a list item before any key")
            data[current_key].append(stripped[2:].strip())
            continue
        raise ValueError(f"Unsupported ontology.yaml line: {raw_line}")
    return data


def validate_ontology_alignment(path: str | Path = DEFAULT_ONTOLOGY_PATH) -> dict[str, list[str]]:
    """Ensure the human-facing ontology file matches the Python taxonomy."""

    ontology = load_ontology(path)
    expected = {
        "core_spheres": set(core_sphere_values()),
        "advanced_modules": set(advanced_module_values()),
        "explanation_tags": set(explanation_tag_values()),
        "phronesis_salience": set(phronesis_salience_values()),
    }
    for key, expected_values in expected.items():
        actual_values = set(ontology.get(key, []))
        if actual_values != expected_values:
            raise ValueError(
                f"Ontology mismatch for {key}: expected {sorted(expected_values)}, got {sorted(actual_values)}"
            )
    return ontology


def load_json_schema(schema_name: str, schema_dir: str | Path = DEFAULT_SCHEMA_DIR) -> dict:
    """Load a JSON Schema document by filename stem."""

    schema_path = Path(schema_dir) / f"{schema_name}.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_payload_with_schema(payload: dict, schema_name: str) -> None:
    """Validate a single payload against a stored JSON Schema document."""

    schema = load_json_schema(schema_name)
    try:
        validate_jsonschema(instance=payload, schema=schema)
    except JsonSchemaValidationError as exc:
        raise ValueError(f"JSON Schema validation failed: {exc.message}") from exc


def validate_record_payload(
    payload: dict, model: type[RecordT], schema_name: str
) -> RecordT:
    """Validate a payload against both JSON Schema and a Pydantic model."""

    validate_payload_with_schema(payload, schema_name)
    try:
        return model.model_validate(payload)
    except PydanticValidationError as exc:
        raise ValueError(str(exc)) from exc


def validate_jsonl_file(
    path: str | Path, model: type[RecordT], schema_name: str
) -> list[RecordT]:
    """Validate every JSONL record in a file and return parsed models."""

    parsed: list[RecordT] = []
    for payload in load_jsonl(path):
        parsed.append(validate_record_payload(payload, model, schema_name))
    _validate_unique_ids(parsed)
    if model in {ScenarioRecord, ScenarioInputRecord}:
        validate_scenario_collection(
            cast(Sequence[ScenarioRecord | ScenarioInputRecord], parsed)
        )
    return parsed


def validate_scenario_collection(
    records: Sequence[ScenarioRecord | ScenarioInputRecord],
) -> Sequence[ScenarioRecord | ScenarioInputRecord]:
    """Validate cross-record family structure for scenario collections."""

    families: dict[str, list[ScenarioRecord | ScenarioInputRecord]] = defaultdict(list)
    for record in records:
        if record.family_id is not None:
            families[record.family_id].append(record)

    for family_id, members in families.items():
        if len(members) < 2:
            raise ValueError(
                f"family_id {family_id!r} must appear on at least two records in the same file"
            )
        variant_counts = Counter(member.variant_type for member in members)
        if variant_counts[VariantType.BASE] != 1:
            raise ValueError(
                f"family_id {family_id!r} must contain exactly one base variant"
            )
    return records


def _validate_unique_ids(records: Sequence[RecordT]) -> None:
    """Reject duplicate record ids inside a JSONL file."""

    record_ids = [getattr(record, "id", None) for record in records]
    duplicates = [
        record_id
        for record_id, count in Counter(record_ids).items()
        if record_id is not None and count > 1
    ]
    if duplicates:
        raise ValueError(f"duplicate record ids found: {sorted(duplicates)}")
