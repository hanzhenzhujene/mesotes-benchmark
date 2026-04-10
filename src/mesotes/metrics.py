"""Evaluation metrics for MESOTES predictions."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from typing import TypeAlias

from .schema import PredictionRecord, ScenarioRecord
from .taxonomy import VariantType


PredictionSignature: TypeAlias = tuple[
    str,
    tuple[str, ...],
    str,
    str,
    str,
    str | None,
    tuple[str, ...],
    str,
    bool,
    tuple[str, ...],
    bool,
]


SALIENCE_SHIFT_TYPES = frozenset(
    {
        VariantType.MINIMAL_PAIR,
        VariantType.SALIENCE_SHIFT,
        VariantType.AGENT_SHIFT,
        VariantType.ROLE_SHIFT,
    }
)


def evaluate_predictions(
    predictions: Sequence[PredictionRecord], gold_records: Sequence[ScenarioRecord]
) -> dict[str, float]:
    """Compute the benchmark metrics for a prediction run."""

    paired = _align_predictions(predictions, gold_records)
    sphere_accuracy = _mean_boolean(
        pred.primary_sphere == gold.primary_sphere for pred, gold in paired
    )
    deficiency_accuracy = _mean_boolean(
        pred.deficiency_action_id == gold.gold.deficiency_action_id for pred, gold in paired
    )
    excess_accuracy = _mean_boolean(
        pred.excess_action_id == gold.gold.excess_action_id for pred, gold in paired
    )
    mean_accuracy = _mean_boolean(
        pred.mean_action_id == gold.gold.mean_action_id for pred, gold in paired
    )
    false_midpoint_pairs = [
        (pred, gold)
        for pred, gold in paired
        if gold.gold.false_midpoint_action_id is not None
    ]
    false_midpoint_accuracy = (
        _mean_boolean(
            pred.false_midpoint_action_id == gold.gold.false_midpoint_action_id
            for pred, gold in false_midpoint_pairs
        )
        if false_midpoint_pairs
        else 0.0
    )

    relevant_factor_f1 = _micro_set_f1(
        ((pred.relevant_factors, gold.relevant_factors) for pred, gold in paired)
    )
    mean_not_midpoint_tag_f1 = _micro_set_f1(
        (
            (pred.mean_not_midpoint_tags, gold.gold.mean_not_midpoint_tags)
            for pred, gold in paired
        )
    )
    phronesis_salience_accuracy = _mean_boolean(
        pred.phronesis_salience == gold.gold.phronesis_salience for pred, gold in paired
    )
    needs_more_info_f1 = _positive_class_f1(
        ((pred.needs_more_info, gold.gold.needs_more_info) for pred, gold in paired)
    )
    no_mean_accuracy = _mean_boolean(
        pred.no_mean_exception == gold.gold.no_mean_exception for pred, gold in paired
    )
    midpoint_trap_error_rate = (
        _mean_boolean(
            pred.mean_action_id == gold.gold.false_midpoint_action_id
            for pred, gold in false_midpoint_pairs
        )
        if false_midpoint_pairs
        else 0.0
    )
    midpoint_trap_rejection = 1.0 - midpoint_trap_error_rate
    action_role_components = [deficiency_accuracy, excess_accuracy, mean_accuracy]
    if false_midpoint_pairs:
        action_role_components.append(false_midpoint_accuracy)
    action_role_accuracy = _mean_numeric(action_role_components)

    nuisance_invariance = nuisance_invariance_score(predictions, gold_records)
    salience_responsiveness = salience_responsiveness_score(predictions, gold_records)
    family_consistency = family_consistency_score(predictions, gold_records)

    composite_score = (
        0.25 * action_role_accuracy
        + 0.15 * sphere_accuracy
        + 0.15 * relevant_factor_f1
        + 0.10 * mean_not_midpoint_tag_f1
        + 0.10 * midpoint_trap_rejection
        + 0.10 * phronesis_salience_accuracy
        + 0.10 * needs_more_info_f1
        + 0.05 * no_mean_accuracy
    )

    return {
        "num_items": float(len(paired)),
        "sphere_accuracy": sphere_accuracy,
        "deficiency_accuracy": deficiency_accuracy,
        "excess_accuracy": excess_accuracy,
        "mean_accuracy": mean_accuracy,
        "false_midpoint_accuracy": false_midpoint_accuracy,
        "action_role_accuracy": action_role_accuracy,
        "relevant_factor_f1": relevant_factor_f1,
        "mean_not_midpoint_tag_f1": mean_not_midpoint_tag_f1,
        "phronesis_salience_accuracy": phronesis_salience_accuracy,
        "needs_more_info_f1": needs_more_info_f1,
        "no_mean_accuracy": no_mean_accuracy,
        "midpoint_trap_error_rate": midpoint_trap_error_rate,
        "midpoint_trap_rejection": midpoint_trap_rejection,
        "nuisance_invariance_score": nuisance_invariance,
        "salience_responsiveness_score": salience_responsiveness,
        "family_consistency_score": family_consistency,
        "composite_score": composite_score,
    }


def nuisance_invariance_score(
    predictions: Sequence[PredictionRecord], gold_records: Sequence[ScenarioRecord]
) -> float:
    """Measure whether nuisance variants preserve the base prediction signature.

    This score only evaluates `irrelevant_detail_shift` items whose gold signature
    matches the base item in the same family. It checks whether the prediction
    signature also stays the same. Interpret it jointly with core accuracy, since
    a model can be consistently wrong and still invariant.
    """

    paired = _align_predictions(predictions, gold_records)
    return _family_variant_score(
        paired,
        predicate=lambda variant, base: (
            variant.variant_type == VariantType.IRRELEVANT_DETAIL_SHIFT
            and _gold_signature(variant) == _gold_signature(base)
        ),
        require_change=False,
    )


def salience_responsiveness_score(
    predictions: Sequence[PredictionRecord], gold_records: Sequence[ScenarioRecord]
) -> float:
    """Measure whether salient family variants trigger a changed prediction.

    This score evaluates `minimal_pair`, `salience_shift`, `agent_shift`, and
    `role_shift` variants only when the gold signature differs from the base item.
    It then checks whether the model also changes its prediction signature.
    """

    paired = _align_predictions(predictions, gold_records)
    return _family_variant_score(
        paired,
        predicate=lambda variant, base: (
            variant.variant_type in SALIENCE_SHIFT_TYPES
            and _gold_signature(variant) != _gold_signature(base)
        ),
        require_change=True,
    )


def family_consistency_score(
    predictions: Sequence[PredictionRecord], gold_records: Sequence[ScenarioRecord]
) -> float:
    """Measure whether each variant matches the gold family's sameness/change pattern.

    For every non-base family member, this score compares the variant to the
    family's base item. If the gold signatures are the same, the prediction
    signatures should also be the same. If the gold signatures differ, the
    prediction signatures should differ.
    """

    paired = _align_predictions(predictions, gold_records)
    families = _family_pairings(paired)
    values: list[bool] = []
    for base, variants in families.values():
        base_prediction, base_gold = base
        base_prediction_signature = _prediction_signature(base_prediction)
        base_gold_signature = _gold_signature(base_gold)
        for prediction, gold in variants:
            gold_same = _gold_signature(gold) == base_gold_signature
            prediction_same = _prediction_signature(prediction) == base_prediction_signature
            values.append(gold_same == prediction_same)
    return _mean_boolean(values)


def format_metric_report(metrics: dict[str, float]) -> str:
    """Render a readable multiline metric report."""

    ordered_keys = [
        "num_items",
        "sphere_accuracy",
        "deficiency_accuracy",
        "excess_accuracy",
        "mean_accuracy",
        "false_midpoint_accuracy",
        "action_role_accuracy",
        "relevant_factor_f1",
        "mean_not_midpoint_tag_f1",
        "phronesis_salience_accuracy",
        "needs_more_info_f1",
        "no_mean_accuracy",
        "midpoint_trap_error_rate",
        "midpoint_trap_rejection",
        "nuisance_invariance_score",
        "salience_responsiveness_score",
        "family_consistency_score",
        "composite_score",
    ]
    lines = ["MESOTES evaluation report"]
    for key in ordered_keys:
        value = metrics[key]
        if key == "num_items":
            lines.append(f"- {key}: {int(value)}")
        else:
            lines.append(f"- {key}: {value:.4f}")
    return "\n".join(lines)


def _align_predictions(
    predictions: Sequence[PredictionRecord], gold_records: Sequence[ScenarioRecord]
) -> list[tuple[PredictionRecord, ScenarioRecord]]:
    gold_by_id = {record.id: record for record in gold_records}
    prediction_by_id = {record.id: record for record in predictions}
    if set(gold_by_id) != set(prediction_by_id):
        missing = sorted(set(gold_by_id) - set(prediction_by_id))
        extra = sorted(set(prediction_by_id) - set(gold_by_id))
        raise ValueError(
            f"Prediction ids must match gold ids exactly. Missing={missing}, Extra={extra}"
        )

    aligned_ids = sorted(gold_by_id)
    return [(prediction_by_id[record_id], gold_by_id[record_id]) for record_id in aligned_ids]


def _family_pairings(
    paired: Sequence[tuple[PredictionRecord, ScenarioRecord]],
) -> dict[str, tuple[tuple[PredictionRecord, ScenarioRecord], list[tuple[PredictionRecord, ScenarioRecord]]]]:
    grouped: dict[
        str,
        list[tuple[PredictionRecord, ScenarioRecord]],
    ] = defaultdict(list)
    for prediction, gold in paired:
        if gold.family_id is not None:
            grouped[gold.family_id].append((prediction, gold))

    families: dict[
        str,
        tuple[tuple[PredictionRecord, ScenarioRecord], list[tuple[PredictionRecord, ScenarioRecord]]],
    ] = {}
    for family_id, members in grouped.items():
        base_candidates = [
            member for member in members if member[1].variant_type == VariantType.BASE
        ]
        if len(base_candidates) != 1:
            continue
        base = base_candidates[0]
        variants = [
            member for member in members if member[1].variant_type != VariantType.BASE
        ]
        if variants:
            families[family_id] = (base, variants)
    return families


def _family_variant_score(
    paired: Sequence[tuple[PredictionRecord, ScenarioRecord]],
    predicate: Callable[[ScenarioRecord, ScenarioRecord], bool],
    require_change: bool,
) -> float:
    values: list[bool] = []
    for base, variants in _family_pairings(paired).values():
        base_prediction, base_gold = base
        base_prediction_signature = _prediction_signature(base_prediction)
        for prediction, gold in variants:
            if not predicate(gold, base_gold):
                continue
            prediction_changed = _prediction_signature(prediction) != base_prediction_signature
            values.append(prediction_changed if require_change else not prediction_changed)
    return _mean_boolean(values)


def _prediction_signature(record: PredictionRecord) -> PredictionSignature:
    return (
        record.primary_sphere.value,
        tuple(sorted(tag.value for tag in record.relevant_factors)),
        record.deficiency_action_id,
        record.excess_action_id,
        record.mean_action_id,
        record.false_midpoint_action_id,
        tuple(sorted(tag.value for tag in record.mean_not_midpoint_tags)),
        record.phronesis_salience.value,
        record.needs_more_info,
        tuple(sorted(record.missing_information_fields)),
        record.no_mean_exception,
    )


def _gold_signature(record: ScenarioRecord) -> PredictionSignature:
    return (
        record.primary_sphere.value,
        tuple(sorted(tag.value for tag in record.relevant_factors)),
        record.gold.deficiency_action_id,
        record.gold.excess_action_id,
        record.gold.mean_action_id,
        record.gold.false_midpoint_action_id,
        tuple(sorted(tag.value for tag in record.gold.mean_not_midpoint_tags)),
        record.gold.phronesis_salience.value,
        record.gold.needs_more_info,
        tuple(sorted(record.gold.missing_information_fields)),
        record.gold.no_mean_exception,
    )


def _micro_set_f1(
    pairs: Iterable[tuple[Sequence[object], Sequence[object]]]
) -> float:
    tp = fp = fn = 0
    for predicted, gold in pairs:
        predicted_set = set(predicted)
        gold_set = set(gold)
        tp += len(predicted_set & gold_set)
        fp += len(predicted_set - gold_set)
        fn += len(gold_set - predicted_set)
    return _f1(tp, fp, fn)


def _positive_class_f1(pairs: Iterable[tuple[bool, bool]]) -> float:
    tp = fp = fn = 0
    for predicted, gold in pairs:
        if predicted and gold:
            tp += 1
        elif predicted and not gold:
            fp += 1
        elif not predicted and gold:
            fn += 1
    return _f1(tp, fp, fn)


def _f1(tp: int, fp: int, fn: int) -> float:
    precision = 0.0 if tp + fp == 0 else tp / (tp + fp)
    recall = 0.0 if tp + fn == 0 else tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _mean_boolean(values: Iterable[bool]) -> float:
    numeric = [1.0 if value else 0.0 for value in values]
    if not numeric:
        return 0.0
    return sum(numeric) / len(numeric)


def _mean_numeric(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)
