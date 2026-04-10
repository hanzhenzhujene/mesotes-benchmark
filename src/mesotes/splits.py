"""Deterministic split creation utilities."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from collections.abc import Sequence

from .schema import ScenarioInputRecord, ScenarioRecord


def stratified_split(
    records: Sequence[ScenarioRecord],
    train_ratio: float = 0.7,
    dev_ratio: float = 0.15,
    seed: int = 13,
) -> dict[str, list[ScenarioRecord]]:
    """Split records by `(primary_sphere, domain)` with deterministic shuffling."""

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")
    if not 0 <= dev_ratio < 1:
        raise ValueError("dev_ratio must be between 0 and 1")
    if train_ratio + dev_ratio >= 1:
        raise ValueError("train_ratio + dev_ratio must be less than 1")

    test_ratio = 1.0 - train_ratio - dev_ratio
    rng = random.Random(seed)
    grouped: dict[tuple[str, str], list[ScenarioRecord]] = defaultdict(list)
    for record in records:
        grouped[(record.primary_sphere, record.domain)].append(record)

    splits: dict[str, list[ScenarioRecord]] = {"train": [], "dev": [], "test": []}
    for group_key in sorted(grouped):
        items = list(grouped[group_key])
        rng.shuffle(items)
        counts = _allocate_counts(len(items), (train_ratio, dev_ratio, test_ratio))
        train_end = counts[0]
        dev_end = train_end + counts[1]
        splits["train"].extend(items[:train_end])
        splits["dev"].extend(items[train_end:dev_end])
        splits["test"].extend(items[dev_end:])

    for split_name in splits:
        rng.shuffle(splits[split_name])
    return splits


def build_test_inputs(records: Sequence[ScenarioRecord]) -> list[ScenarioInputRecord]:
    """Strip gold labels from test records."""

    return [ScenarioInputRecord.from_scenario_record(record) for record in records]


def _allocate_counts(total: int, ratios: tuple[float, float, float]) -> tuple[int, int, int]:
    if total == 0:
        return (0, 0, 0)
    raw = [total * ratio for ratio in ratios]
    counts = [math.floor(value) for value in raw]
    remainder = total - sum(counts)
    fractional_parts = sorted(
        ((raw[index] - counts[index], index) for index in range(len(ratios))),
        reverse=True,
    )
    for _, index in fractional_parts[:remainder]:
        counts[index] += 1
    return counts[0], counts[1], counts[2]
