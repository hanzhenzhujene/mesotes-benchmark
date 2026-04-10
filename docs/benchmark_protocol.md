# Benchmark Protocol

## Tasks

MESOTES evaluates five linked tasks:

1. `sphere_identification`
2. `action_role_classification`
3. `false_midpoint_rejection`
4. `phronesis_and_information_gap_recognition`
5. `no_mean_exception_recognition`

Each item presents a concrete scenario, an agent profile, and four candidate actions. In `pilot_v2`, some items also belong to counterfactual families so models can be tested for nuisance stability and salience responsiveness.

## Scenario metadata

The scenario-side schema now includes:

- `family_id`: nullable identifier for a counterfactual family
- `variant_type`: one of `base`, `minimal_pair`, `irrelevant_detail_shift`, `salience_shift`, `agent_shift`, `role_shift`

These fields are part of the benchmark item, not the prediction schema.

## Annotation metadata

Gold records also carry label-quality metadata:

- `annotation_confidence`: `low`, `medium`, `high`
- `disagreement_flags`: controlled list of adjudication issues
- `adjudication_note`: optional short memo for hard cases
- `author_intended_trap_type`: optional internal marker for the authored false-midpoint pattern

These fields are useful for review and reporting. They are not treated as model-output targets.

## Required prediction fields

The expected prediction schema is the `PredictionRecord` structure:

- `id`
- `primary_sphere`
- `relevant_factors`
- `deficiency_action_id`
- `excess_action_id`
- `mean_action_id`
- `false_midpoint_action_id`
- `mean_not_midpoint_tags`
- `phronesis_salience`
- `needs_more_info`
- `missing_information_fields`
- `no_mean_exception`
- optional `short_rationale`

## Core metrics

The repository computes:

- sphere accuracy
- deficiency accuracy
- excess accuracy
- mean accuracy
- false midpoint accuracy
- action role accuracy
- relevant factor F1
- mean-not-midpoint tag F1
- phronesis salience accuracy
- needs-more-info F1
- no-mean accuracy
- midpoint trap error rate
- midpoint trap rejection
- composite score

The composite score uses fixed weights tuned for the current protocol:

- 0.25 action role accuracy
- 0.15 sphere accuracy
- 0.15 relevant factor F1
- 0.10 mean-not-midpoint tag F1
- 0.10 midpoint trap rejection
- 0.10 phronesis salience accuracy
- 0.10 needs-more-info F1
- 0.05 no-mean accuracy

## Counterfactual family metrics

`pilot_v2` adds three family-aware metrics.

### `nuisance_invariance_score`

This score only looks at `irrelevant_detail_shift` variants whose gold judgment signature matches the family base item. It asks whether the model also keeps the prediction signature stable.

Interpretation:

- high is better
- read it jointly with accuracy, because a model can stay stably wrong

### `salience_responsiveness_score`

This score looks at `minimal_pair`, `salience_shift`, `agent_shift`, and `role_shift` variants when the gold judgment signature differs from the family base item. It asks whether the model also changes its prediction signature.

Interpretation:

- high is better
- the score is about changing when it should, not about whether the changed answer is correct in every field

### `family_consistency_score`

This score compares every non-base family member to its base item.

- if the gold signatures match, the prediction signatures should match
- if the gold signatures differ, the prediction signatures should differ

This provides one family-level summary of whether a run respects the dataset's intended sameness/change structure.

## Judgment signature used by family metrics

The family metrics compare a structured judgment signature built from:

- `primary_sphere`
- `relevant_factors`
- `deficiency_action_id`
- `excess_action_id`
- `mean_action_id`
- `false_midpoint_action_id`
- `mean_not_midpoint_tags`
- `phronesis_salience`
- `needs_more_info`
- `missing_information_fields`
- `no_mean_exception`

This is intentionally broader than mean-action matching alone.

## Evaluation notes

- `false_midpoint_accuracy` is only meaningful on items that include a false midpoint.
- `needs_more_info_f1` is computed as positive-class F1 on the boolean field.
- `midpoint_trap_error_rate` tracks how often the predicted mean action is actually the gold false midpoint.
- family metrics require `family_id` structure in the gold records
- family metrics are most informative when paired with the core metrics rather than used alone

## Reporting guidance

When presenting results from this repository's illustrative pilots:

- say explicitly that the pilots are illustrative seed data
- do not describe the labels as final adjudicated benchmark gold
- keep family-metric interpretations careful and descriptive
- do not claim scientific conclusions from the included mock predictions
