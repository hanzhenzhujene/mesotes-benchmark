# MESOTES Adjudication Workflow

MESOTES is designed around expert-facing adjudication rather than crowd gold labels.

## Workflow

1. Annotator A labels the item independently.
2. Annotator B labels the item independently.
3. An adjudicator reviews disagreements and issues the release label.
4. The adjudicator records confidence, disagreement flags, and a short adjudication note.

The adjudicator should preserve disagreement for hard cases rather than flattening uncertainty out of the record-creation process.

## Required outputs per item

- ontology tags
- action-role labels
- short rationale
- confidence score
- disagreement flags if any
- adjudication note for non-trivial review cases

## Calibration round

Before a new annotation batch:

- run a shared calibration set
- compare sphere choices, mean labels, false-midpoint labels, and `needs_more_info` decisions
- update examples in the guidelines when repeated disagreements reveal ambiguity in the operationalization

## Confidence guidance

Use a simple three-level internal scale:

- `high`: labels are clear under the current guidelines
- `medium`: one or two distinctions were difficult but the adjudicated answer is stable enough for current use
- `low`: case remains contestable and should be revisited before any public release claiming strong gold quality

## Suggested disagreement flags

- `sphere_dispute`
- `mean_dispute`
- `phronesis_dispute`
- `false_midpoint_dispute`
- `needs_more_info_dispute`
- `no_mean_exception_dispute`
- `factor_salience_dispute`

See [annotation/disagreement_templates.md](disagreement_templates.md) for lightweight review templates.

## Adjudication log template

```text
item_id:
annotator_a_primary_sphere:
annotator_b_primary_sphere:
annotator_a_mean_action_id:
annotator_b_mean_action_id:
annotator_a_false_midpoint_action_id:
annotator_b_false_midpoint_action_id:
annotator_a_needs_more_info:
annotator_b_needs_more_info:
disagreement_flags:
adjudicator_decision:
adjudicator_rationale:
annotation_confidence:
adjudication_note:
```

## Release note

The pilots in this repository are illustrative seed material. They are intentionally marked `illustrative_only` rather than final adjudicated benchmark gold.
