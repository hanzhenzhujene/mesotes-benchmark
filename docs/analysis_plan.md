# Analysis Plan

This document sketches how a future MESOTES paper or technical report could analyze model behavior. It does not assert results.

## Hypotheses

1. Models will often confuse the true mean with false moderation.
2. Models will underperform on person-relative and role-relative family variants.
3. Explicit Aristotelian structure will help more than generic moral prompting.
4. Models that sound morally fluent will still fail on information-gap recognition and no-mean exceptions.

## Likely failure modes

- choosing the false midpoint because it sounds diplomatically balanced
- treating the mean as a numerical compromise
- keeping the same answer across agent or role shifts that should change judgment
- changing answers when only irrelevant details shift
- ignoring `needs_more_info` and forcing a verdict
- treating intrinsically bad act-kinds as if a moderated version could be right
- giving relevant-factor tags that are too generic to track the gold rationale

## Recommended quantitative tables

- overall metric table by model and baseline condition
- per-sphere breakdown
- breakdown by difficulty
- breakdown by `needs_more_info` and `no_mean_exception`
- breakdown by family `variant_type`
- disagreement-aware slice: high-confidence versus low-confidence items

## Recommended figures

- bar chart of midpoint trap error rate by baseline condition
- bar chart of family metrics by `variant_type`
- confusion-style figure for predicted mean versus gold false midpoint on trap items
- heatmap of sphere accuracy by model and prompting condition

## Recommended qualitative sections

- short case studies of fake moderation failures
- person-relative donation or resource cases
- role-shift cases where models miss institutional obligation
- under-specified cases where models should have asked for more information
- no-mean cases where models still hunt for compromise

## Adjudication-aware analysis

When the dataset includes disagreement metadata, it is useful to compare:

- performance on `annotation_confidence = high` versus `low`
- performance on items with and without `disagreement_flags`
- which disagreement types correlate with model failure

These analyses should be framed carefully. Low-confidence items are not invalid; they signal interpretive pressure points in the benchmark.

## Reporting cautions

- do not treat illustrative pilot runs as benchmark claims
- do not infer scientific novelty from mock predictions
- do not collapse family metrics into accuracy claims without explanation
- distinguish framework fidelity from broader moral correctness claims
