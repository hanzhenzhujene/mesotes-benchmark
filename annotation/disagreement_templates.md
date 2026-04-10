# Disagreement Templates

These templates are lightweight internal forms for recording why an item still needs review. They are intentionally simple so annotators can use them quickly.

## Sphere dispute

```text
item_id:
annotator_a_primary_sphere:
annotator_b_primary_sphere:
shared_relevant_factors:
what makes the sphere choice difficult:
adjudicated_primary_sphere:
adjudication_note:
```

## Mean dispute

```text
item_id:
annotator_a_mean_action_id:
annotator_b_mean_action_id:
annotator_a_false_midpoint_action_id:
annotator_b_false_midpoint_action_id:
shared_deficiency_action_id:
shared_excess_action_id:
salient_factors_in_dispute:
adjudicated_mean_action_id:
adjudication_note:
```

## Phronesis dispute

```text
item_id:
annotator_a_phronesis_salience:
annotator_b_phronesis_salience:
annotator_a_needs_more_info:
annotator_b_needs_more_info:
annotator_a_missing_information_fields:
annotator_b_missing_information_fields:
what particulars seem decisive:
adjudicated_phronesis_salience:
adjudicated_needs_more_info:
adjudication_note:
```

## Suggested disagreement flags

Use the controlled `disagreement_flags` field when one of these categories applies:

- `sphere_dispute`
- `mean_dispute`
- `phronesis_dispute`
- `false_midpoint_dispute`
- `needs_more_info_dispute`
- `no_mean_exception_dispute`
- `factor_salience_dispute`

## Review reminder

The goal is not to eliminate all disagreement from the record. The goal is to preserve where disagreement happened, why it happened, and how the release decision was made.
