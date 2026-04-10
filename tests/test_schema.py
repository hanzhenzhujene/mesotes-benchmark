from __future__ import annotations

import pytest

from mesotes.loader import load_records
from mesotes.schema import PredictionRecord, ScenarioRecord
from conftest import PILOT_DIR


def make_valid_scenario() -> dict:
    return {
        "id": "mesotes_train_9999",
        "split": "train",
        "domain": "workplace",
        "scenario": "A release lead finds a hidden deployment blocker an hour before launch.",
        "agent_profile": {
            "role": "release_lead",
            "experience_level": "high",
            "resource_position": "moderate",
            "power_relation": "supervises_engineer",
        },
        "family_id": "family-release-blocker",
        "variant_type": "base",
        "primary_sphere": "fear_confidence",
        "secondary_considerations": ["truthfulness_self_presentation", "justice_constraint"],
        "relevant_factors": [
            "timing_sensitive",
            "role_obligation",
            "stakes_asymmetric",
            "public_private_difference",
        ],
        "candidate_actions": [
            {"id": "a1", "text": "Wait quietly and hope the issue disappears."},
            {"id": "a2", "text": "Expose the engineer in front of the full team."},
            {
                "id": "a3",
                "text": "Pause the launch, alert the right leads, and address the problem privately.",
            },
            {"id": "a4", "text": "Hint that there may be a problem but keep the launch moving."},
        ],
        "gold": {
            "deficiency_action_id": "a1",
            "excess_action_id": "a2",
            "mean_action_id": "a3",
            "false_midpoint_action_id": "a4",
            "mean_not_midpoint_tags": [
                "timing_sensitive",
                "role_obligation",
                "stakes_asymmetric",
            ],
            "phronesis_salience": "high",
            "needs_more_info": False,
            "missing_information_fields": [],
            "no_mean_exception": False,
            "short_rationale": "The stakes require timely intervention without public shaming.",
            "annotation_confidence": "high",
            "disagreement_flags": [],
            "adjudication_note": None,
            "author_intended_trap_type": "timid_delay",
        },
        "meta": {
            "source_type": "illustrative_seed",
            "adjudication_status": "illustrative_only",
            "difficulty": "hard",
        },
    }


def test_valid_scenario_record_passes() -> None:
    record = ScenarioRecord.model_validate(make_valid_scenario())
    assert record.primary_sphere == "fear_confidence"
    assert record.family_id == "family-release-blocker"


def test_old_pilot_record_still_validates_without_new_fields() -> None:
    payload = make_valid_scenario()
    payload.pop("family_id")
    payload.pop("variant_type")
    payload["gold"].pop("annotation_confidence")
    payload["gold"].pop("disagreement_flags")
    payload["gold"].pop("adjudication_note")
    payload["gold"].pop("author_intended_trap_type")
    record = ScenarioRecord.model_validate(payload)
    assert record.variant_type == "base"
    assert record.gold.annotation_confidence == "medium"


def test_candidate_action_count_must_be_four() -> None:
    payload = make_valid_scenario()
    payload["candidate_actions"] = payload["candidate_actions"][:3]
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_duplicate_candidate_action_ids_fail() -> None:
    payload = make_valid_scenario()
    payload["candidate_actions"][3]["id"] = "a3"
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_mean_not_midpoint_tags_must_be_subset_of_relevant_factors() -> None:
    payload = make_valid_scenario()
    payload["gold"]["mean_not_midpoint_tags"] = ["timing_sensitive", "history_sensitive"]
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_needs_more_info_requires_missing_fields() -> None:
    payload = make_valid_scenario()
    payload["gold"]["needs_more_info"] = True
    payload["gold"]["missing_information_fields"] = []
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_invalid_secondary_consideration_fails() -> None:
    payload = make_valid_scenario()
    payload["secondary_considerations"] = ["anger_response", "not_a_real_value"]
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_prediction_record_rejects_duplicate_relevant_factors() -> None:
    scenario = ScenarioRecord.model_validate(make_valid_scenario())
    prediction = {
        "id": scenario.id,
        "primary_sphere": scenario.primary_sphere,
        "relevant_factors": ["timing_sensitive", "timing_sensitive"],
        "deficiency_action_id": "a1",
        "excess_action_id": "a2",
        "mean_action_id": "a3",
        "false_midpoint_action_id": "a4",
        "mean_not_midpoint_tags": ["timing_sensitive"],
        "phronesis_salience": "high",
        "needs_more_info": False,
        "missing_information_fields": [],
        "no_mean_exception": False,
    }
    with pytest.raises(Exception):
        PredictionRecord.model_validate(prediction)


def test_variant_type_requires_family_id() -> None:
    payload = make_valid_scenario()
    payload["family_id"] = None
    payload["variant_type"] = "salience_shift"
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_author_trap_type_requires_false_midpoint() -> None:
    payload = make_valid_scenario()
    payload["gold"]["false_midpoint_action_id"] = None
    with pytest.raises(Exception):
        ScenarioRecord.model_validate(payload)


def test_existing_pilot_files_remain_loadable() -> None:
    records = load_records(PILOT_DIR / "train.jsonl", ScenarioRecord)
    assert len(records) == 12
