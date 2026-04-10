# Dataset Card

## Motivation

MESOTES is motivated by the need for a benchmark that tests Aristotelian framework fidelity rather than broad moral verdict prediction. The central question is whether a model can reason about spheres, means, excesses, deficiencies, false moderation, practical judgment, and cases where additional information is needed.

## Composition

The repository currently ships:

- ontology and annotation instructions
- JSONL schemas for labeled scenarios, blind inputs, and predictions
- `data/pilot/`, a 24-item scaffold pilot
- `data/pilot_v2/`, a 32-item research-validation pilot with counterfactual families and adjudication metadata

`pilot_v2` includes:

- all eight core spheres
- explicit false-midpoint stress tests
- under-specified needs-more-info cases
- no-mean exceptions
- counterfactual families with `family_id` and `variant_type`
- annotation confidence and disagreement metadata

## Collection process

Both pilots are human-authored illustrative seed sets created to strengthen repository structure and evaluation plumbing. They are not presented as final public benchmark gold.

`pilot_v2` is intentionally more demanding than the original scaffold pilot. It is designed to surface failure modes that a cleaner, easier pilot would miss, especially:

- false-midpoint selection
- role-relative misses
- person-relative misses
- under-recognition of information gaps
- instability under nuisance details

## Annotation process

The intended workflow is:

1. ontology tagging
2. action-role labeling
3. short rationale writing
4. disagreement flagging and confidence assignment
5. adjudication by an experienced reviewer

See [annotation/guidelines.md](../annotation/guidelines.md), [annotation/adjudication.md](../annotation/adjudication.md), and [annotation/disagreement_templates.md](../annotation/disagreement_templates.md) for the operational details.

## Intended uses

- benchmark prototyping
- annotation pipeline development
- baseline prompt experiments
- counterfactual family analysis
- evaluation-tooling development
- adjudication and disagreement workflow testing

It is especially useful for early-stage experiments where the goal is to test whether a model is structurally tracking Aristotelian distinctions, not to claim final benchmark performance.

## Limitations

- the shipped pilots are small and illustrative
- labels are operationalized for benchmarking, not offered as definitive philosophical judgments
- included disagreement metadata is useful for review, but it does not replace expert adjudication
- no benchmark results are claimed in this repository

## Bias and risk statement

Ethics benchmarks can overstate objectivity. MESOTES reduces that risk by making the framework explicit, separating illustrative seed data from adjudicated gold, and preserving disagreement as metadata instead of flattening it away.

Even so:

- future public releases will still reflect interpretive choices
- Aristotelian operationalization remains historically and pedagogically contestable
- family metrics can reward stability or responsiveness without by themselves proving correctness
- mock predictions in this repository are for tooling demonstration only
