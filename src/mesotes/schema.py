"""Pydantic models for MESOTES records."""

from __future__ import annotations

from typing import Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .taxonomy import (
    AnnotationConfidence,
    CoreSphere,
    DisagreementFlag,
    ExplanationTag,
    PhronesisSalience,
    Split,
    TrapType,
    VariantType,
    secondary_consideration_values,
)


ItemT = TypeVar("ItemT")


class CandidateAction(BaseModel):
    """A candidate response offered for a benchmark scenario."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    text: str = Field(min_length=1)


class AgentProfile(BaseModel):
    """The agent-facing profile that makes person-relative judgment possible."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    role: str = Field(min_length=1)
    experience_level: str = Field(min_length=1)
    resource_position: str = Field(min_length=1)
    power_relation: str = Field(min_length=1)


class GoldLabels(BaseModel):
    """Adjudicated labels and label-quality metadata for a scenario."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    deficiency_action_id: str = Field(min_length=1)
    excess_action_id: str = Field(min_length=1)
    mean_action_id: str = Field(min_length=1)
    false_midpoint_action_id: Optional[str] = None
    mean_not_midpoint_tags: list[ExplanationTag] = Field(default_factory=list)
    phronesis_salience: PhronesisSalience
    needs_more_info: bool
    missing_information_fields: list[str] = Field(default_factory=list)
    no_mean_exception: bool
    short_rationale: str = Field(min_length=1)
    annotation_confidence: AnnotationConfidence = AnnotationConfidence.MEDIUM
    disagreement_flags: list[DisagreementFlag] = Field(default_factory=list)
    adjudication_note: Optional[str] = Field(default=None, min_length=1)
    author_intended_trap_type: Optional[TrapType] = None

    @field_validator("missing_information_fields")
    @classmethod
    def _non_empty_missing_information_fields(cls, values: list[str]) -> list[str]:
        return _ensure_unique_strings(values, field_name="missing_information_fields")

    @field_validator("mean_not_midpoint_tags")
    @classmethod
    def _unique_mean_not_midpoint_tags(
        cls, values: list[ExplanationTag]
    ) -> list[ExplanationTag]:
        return _ensure_unique_items(values, field_name="mean_not_midpoint_tags")

    @field_validator("disagreement_flags")
    @classmethod
    def _unique_disagreement_flags(
        cls, values: list[DisagreementFlag]
    ) -> list[DisagreementFlag]:
        return _ensure_unique_items(values, field_name="disagreement_flags")

    @model_validator(mode="after")
    def _validate_information_gap(self) -> "GoldLabels":
        if self.needs_more_info and not self.missing_information_fields:
            raise ValueError(
                "missing_information_fields must be non-empty when needs_more_info is true"
            )
        if not self.needs_more_info and self.missing_information_fields:
            raise ValueError(
                "missing_information_fields must be empty when needs_more_info is false"
            )
        if self.false_midpoint_action_id is not None and self.false_midpoint_action_id in {
            self.deficiency_action_id,
            self.excess_action_id,
            self.mean_action_id,
        }:
            raise ValueError(
                "false_midpoint_action_id must be distinct from deficiency, excess, and mean"
            )
        if self.author_intended_trap_type is not None and self.false_midpoint_action_id is None:
            raise ValueError(
                "author_intended_trap_type may only be set when false_midpoint_action_id is present"
            )
        return self


class MetaRecord(BaseModel):
    """Metadata about provenance and release status."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_type: str = Field(min_length=1)
    adjudication_status: str = Field(min_length=1)
    difficulty: str = Field(min_length=1)


class ScenarioBase(BaseModel):
    """Fields shared by labeled and unlabeled scenario records."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    split: Split
    domain: str = Field(min_length=1)
    scenario: str = Field(min_length=1)
    agent_profile: AgentProfile
    primary_sphere: CoreSphere
    family_id: Optional[str] = None
    variant_type: VariantType = VariantType.BASE
    secondary_considerations: list[str] = Field(default_factory=list)
    relevant_factors: list[ExplanationTag] = Field(default_factory=list)
    candidate_actions: list[CandidateAction] = Field(min_length=4, max_length=4)
    meta: MetaRecord

    @field_validator("family_id")
    @classmethod
    def _clean_family_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("family_id must not be blank when provided")
        return stripped

    @field_validator("secondary_considerations")
    @classmethod
    def _valid_secondary_considerations(cls, values: list[str]) -> list[str]:
        valid_values = set(secondary_consideration_values())
        unique_values = _ensure_unique_strings(
            values, field_name="secondary_considerations"
        )
        invalid = [value for value in unique_values if value not in valid_values]
        if invalid:
            raise ValueError(
                "secondary_considerations contains invalid values: "
                f"{', '.join(sorted(invalid))}"
            )
        return unique_values

    @field_validator("relevant_factors")
    @classmethod
    def _unique_relevant_factors(
        cls, values: list[ExplanationTag]
    ) -> list[ExplanationTag]:
        return _ensure_unique_items(values, field_name="relevant_factors")

    @field_validator("candidate_actions")
    @classmethod
    def _distinct_candidate_actions(
        cls, values: list[CandidateAction]
    ) -> list[CandidateAction]:
        action_ids = [action.id for action in values]
        if len(set(action_ids)) != len(action_ids):
            raise ValueError("candidate action ids must be unique")
        return values

    @model_validator(mode="after")
    def _validate_family_metadata(self) -> "ScenarioBase":
        if self.family_id is None and self.variant_type != VariantType.BASE:
            raise ValueError("variant_type may only be non-base when family_id is provided")
        return self


class ScenarioRecord(ScenarioBase):
    """A fully labeled scenario record."""

    gold: GoldLabels

    @model_validator(mode="after")
    def _validate_gold_action_ids(self) -> "ScenarioRecord":
        action_ids = {action.id for action in self.candidate_actions}
        gold = self.gold
        referenced_ids = [
            gold.deficiency_action_id,
            gold.excess_action_id,
            gold.mean_action_id,
        ]
        if gold.false_midpoint_action_id is not None:
            referenced_ids.append(gold.false_midpoint_action_id)
        missing = [action_id for action_id in referenced_ids if action_id not in action_ids]
        if missing:
            raise ValueError(
                f"gold action ids must reference candidate_actions; missing {sorted(set(missing))}"
            )
        if len(set(referenced_ids)) != len(referenced_ids):
            raise ValueError(
                "gold action ids for deficiency, excess, mean, and false midpoint must be distinct"
            )
        midpoint_tag_values = {tag.value for tag in gold.mean_not_midpoint_tags}
        relevant_factor_values = {tag.value for tag in self.relevant_factors}
        if not midpoint_tag_values.issubset(relevant_factor_values):
            raise ValueError("mean_not_midpoint_tags must be a subset of relevant_factors")
        return self


class ScenarioInputRecord(ScenarioBase):
    """An unlabeled scenario record for blind evaluation."""

    @classmethod
    def from_scenario_record(cls, record: ScenarioRecord) -> "ScenarioInputRecord":
        """Strip gold labels from a full scenario record."""

        return cls.model_validate(record.model_dump(exclude={"gold"}))


class PredictionRecord(BaseModel):
    """Model predictions aligned with the benchmark's evaluable fields."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    primary_sphere: CoreSphere
    relevant_factors: list[ExplanationTag] = Field(default_factory=list)
    deficiency_action_id: str = Field(min_length=1)
    excess_action_id: str = Field(min_length=1)
    mean_action_id: str = Field(min_length=1)
    false_midpoint_action_id: Optional[str] = None
    mean_not_midpoint_tags: list[ExplanationTag] = Field(default_factory=list)
    phronesis_salience: PhronesisSalience
    needs_more_info: bool
    missing_information_fields: list[str] = Field(default_factory=list)
    no_mean_exception: bool
    short_rationale: Optional[str] = Field(default=None, min_length=1)

    @field_validator("relevant_factors")
    @classmethod
    def _unique_prediction_relevant_factors(
        cls, values: list[ExplanationTag]
    ) -> list[ExplanationTag]:
        return _ensure_unique_items(values, field_name="relevant_factors")

    @field_validator("mean_not_midpoint_tags")
    @classmethod
    def _unique_prediction_midpoint_tags(
        cls, values: list[ExplanationTag]
    ) -> list[ExplanationTag]:
        return _ensure_unique_items(values, field_name="mean_not_midpoint_tags")

    @field_validator("missing_information_fields")
    @classmethod
    def _unique_prediction_missing_information_fields(
        cls, values: list[str]
    ) -> list[str]:
        return _ensure_unique_strings(values, field_name="missing_information_fields")

    @model_validator(mode="after")
    def _validate_prediction(self) -> "PredictionRecord":
        if self.needs_more_info and not self.missing_information_fields:
            raise ValueError(
                "missing_information_fields must be non-empty when needs_more_info is true"
            )
        if not self.needs_more_info and self.missing_information_fields:
            raise ValueError(
                "missing_information_fields must be empty when needs_more_info is false"
            )
        if self.false_midpoint_action_id is not None and self.false_midpoint_action_id in {
            self.deficiency_action_id,
            self.excess_action_id,
            self.mean_action_id,
        }:
            raise ValueError(
                "false_midpoint_action_id must be distinct from deficiency, excess, and mean"
            )
        midpoint_tag_values = {tag.value for tag in self.mean_not_midpoint_tags}
        relevant_factor_values = {tag.value for tag in self.relevant_factors}
        if not midpoint_tag_values.issubset(relevant_factor_values):
            raise ValueError("mean_not_midpoint_tags must be a subset of relevant_factors")
        return self


def _ensure_unique_items(values: list[ItemT], field_name: str) -> list[ItemT]:
    """Ensure a list does not contain duplicates."""

    if len(set(values)) != len(values):
        raise ValueError(f"{field_name} must not contain duplicates")
    return values


def _ensure_unique_strings(values: list[str], field_name: str) -> list[str]:
    """Ensure a list of strings does not contain duplicates or blank items."""

    cleaned: list[str] = []
    for value in values:
        stripped = value.strip()
        if not stripped:
            raise ValueError(f"{field_name} must not contain blank strings")
        cleaned.append(stripped)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field_name} must not contain duplicates")
    return cleaned
