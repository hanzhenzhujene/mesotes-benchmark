# Baseline Experiments

This document defines baseline conditions for MESOTES experiments. It does not report model results.

## Goal

The baseline suite is meant to answer a modest question:

How much do structured Aristotelian prompting choices change performance on MESOTES-style tasks, especially on false-midpoint traps, information-gap cases, and counterfactual families?

## Common evaluation setup

For all baseline conditions:

- use the same prediction schema
- report the same core metrics and family metrics
- keep temperature, decoding limits, and post-processing rules constant where possible
- score the runs against the same gold split
- separate illustrative pilot runs from any later benchmark-ready release

## Condition 1: Direct answer

Prompting style:

- present the scenario and candidate actions
- ask for the MESOTES prediction fields directly
- provide no extra ontology guidance

Why include it:

- this is the most conservative benchmark baseline
- it shows how much structure the model can recover without extra framing

## Condition 2: Chain-of-thought style reasoning

Prompting style:

- ask the model to reason step by step before emitting the final JSON prediction
- keep the requested output fields unchanged

Why include it:

- many moral-reasoning evaluations test whether reasoning-style prompting helps
- this condition can reveal whether more explicit deliberation reduces false-midpoint mistakes

Reporting caution:

- do not claim that longer reasoning text itself proves deeper competence
- where policy or evaluation settings require it, store only the final structured outputs

## Condition 3: Ontology-primed Aristotelian reasoning

Prompting style:

- include a compact description of MESOTES task structure
- remind the model to identify sphere, deficiency, excess, mean, false midpoint, information gaps, and no-mean exceptions
- explicitly say that the mean is relative to the person and situation, not an arithmetic midpoint

Why include it:

- this condition tests whether framework-specific structure helps more than generic ethical prompting

## Condition 4: Retrieval of a compact virtue glossary

Prompting style:

- provide a short glossary of the core spheres and their associated virtues
- keep the glossary compact enough that it behaves like lightweight retrieval rather than full fine-tuning

Why include it:

- this tests whether small amounts of explicit Aristotelian background improve framework fidelity
- it is especially relevant on sphere identification and person-relative reasoning

## Recommended outputs

For each baseline condition, report at least:

- core metrics
- family metrics
- midpoint trap error rate
- breakdown by sphere
- breakdown by `needs_more_info` and `no_mean_exception`

## Recommended qualitative audit

For a small hand-inspected slice, record:

- where the model chose the false midpoint
- where the model missed the relevant sphere
- where the model failed to notice a family shift
- where the model treated no-mean cases as if moderation were still available

## Non-claims

This repository does not claim that any one baseline is best. The goal is to make comparisons easy and careful, not to pre-announce results.
