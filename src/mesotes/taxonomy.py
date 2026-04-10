"""Ontology constants for the MESOTES benchmark."""

from __future__ import annotations

from enum import StrEnum


class Split(StrEnum):
    TRAIN = "train"
    DEV = "dev"
    TEST = "test"


class CoreSphere(StrEnum):
    FEAR_CONFIDENCE = "fear_confidence"
    PLEASURE_APPETITE = "pleasure_appetite"
    WEALTH_RESOURCE_USE = "wealth_resource_use"
    HONOR_RECOGNITION = "honor_recognition"
    ANGER_RESPONSE = "anger_response"
    TRUTHFULNESS_SELF_PRESENTATION = "truthfulness_self_presentation"
    AMUSEMENT_HUMOR = "amusement_humor"
    SOCIAL_PLEASANTNESS = "social_pleasantness"


class AdvancedModule(StrEnum):
    MAGNIFICENCE_LARGE_SCALE_SPENDING = "magnificence_large_scale_spending"
    RESPONSE_TO_OTHERS_FORTUNE = "response_to_others_fortune"
    SHAME_MODESTY = "shame_modesty"
    NO_MEAN_EXCEPTION = "no_mean_exception"


class ExplanationTag(StrEnum):
    TIMING_SENSITIVE = "timing_sensitive"
    MOTIVE_SENSITIVE = "motive_sensitive"
    MANNER_SENSITIVE = "manner_sensitive"
    RELATIONSHIP_SENSITIVE = "relationship_sensitive"
    ROLE_OBLIGATION = "role_obligation"
    RESOURCE_RELATIVE = "resource_relative"
    STAKES_ASYMMETRIC = "stakes_asymmetric"
    PUBLIC_PRIVATE_DIFFERENCE = "public_private_difference"
    HISTORY_SENSITIVE = "history_sensitive"
    JUSTICE_CONSTRAINT = "justice_constraint"
    OBJECT_KIND_EXCEPTION = "object_kind_exception"


class PhronesisSalience(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class VariantType(StrEnum):
    BASE = "base"
    MINIMAL_PAIR = "minimal_pair"
    IRRELEVANT_DETAIL_SHIFT = "irrelevant_detail_shift"
    SALIENCE_SHIFT = "salience_shift"
    AGENT_SHIFT = "agent_shift"
    ROLE_SHIFT = "role_shift"


class AnnotationConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DisagreementFlag(StrEnum):
    SPHERE_DISPUTE = "sphere_dispute"
    MEAN_DISPUTE = "mean_dispute"
    PHRONESIS_DISPUTE = "phronesis_dispute"
    FALSE_MIDPOINT_DISPUTE = "false_midpoint_dispute"
    NEEDS_MORE_INFO_DISPUTE = "needs_more_info_dispute"
    NO_MEAN_EXCEPTION_DISPUTE = "no_mean_exception_dispute"
    FACTOR_SALIENCE_DISPUTE = "factor_salience_dispute"


class TrapType(StrEnum):
    FALSE_BALANCE = "false_balance"
    TIMID_DELAY = "timid_delay"
    NUMERIC_SPLIT = "numeric_split"
    VAGUE_HALF_TRUTH = "vague_half_truth"
    ROLE_AVOIDANCE = "role_avoidance"
    PUBLIC_PRIVATE_BLUR = "public_private_blur"


class ActionRole(StrEnum):
    DEFICIENCY = "deficiency"
    EXCESS = "excess"
    MEAN = "mean"
    FALSE_MIDPOINT = "false_midpoint"
    NEEDS_MORE_INFO_RESPONSE = "needs_more_info_response"
    NO_MEAN_EXCEPTION = "no_mean_exception"


CROSS_CUTTING_CONSIDERATIONS = frozenset({ExplanationTag.JUSTICE_CONSTRAINT.value})


def core_sphere_values() -> tuple[str, ...]:
    """Return the closed set of core sphere identifiers."""

    return tuple(item.value for item in CoreSphere)


def advanced_module_values() -> tuple[str, ...]:
    """Return the advanced module identifiers."""

    return tuple(item.value for item in AdvancedModule)


def explanation_tag_values() -> tuple[str, ...]:
    """Return the explanation and relevant-factor tag identifiers."""

    return tuple(item.value for item in ExplanationTag)


def phronesis_salience_values() -> tuple[str, ...]:
    """Return the phronesis salience labels."""

    return tuple(item.value for item in PhronesisSalience)


def variant_type_values() -> tuple[str, ...]:
    """Return the supported counterfactual variant labels."""

    return tuple(item.value for item in VariantType)


def annotation_confidence_values() -> tuple[str, ...]:
    """Return the supported annotation confidence levels."""

    return tuple(item.value for item in AnnotationConfidence)


def disagreement_flag_values() -> tuple[str, ...]:
    """Return the supported disagreement flags."""

    return tuple(item.value for item in DisagreementFlag)


def trap_type_values() -> tuple[str, ...]:
    """Return the supported author-intended trap types."""

    return tuple(item.value for item in TrapType)


def secondary_consideration_values() -> tuple[str, ...]:
    """Return the allowed secondary consideration identifiers."""

    return (*core_sphere_values(), *CROSS_CUTTING_CONSIDERATIONS)
