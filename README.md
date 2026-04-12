<h1 align="center">MESOTES</h1>
<p align="center"><strong>MESOTES: An Aristotelian Benchmark for Phronesis and the Doctrine of the Mean</strong></p>
<p align="center">A research-oriented benchmark for testing whether models can actually reason in an Aristotelian way in concrete situations.</p>

<p align="center">
  <a href="https://github.com/hanzhenzhujene/mesotes-benchmark/actions/workflows/tests.yml"><img src="https://github.com/hanzhenzhujene/mesotes-benchmark/actions/workflows/tests.yml/badge.svg" alt="tests"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB" alt="python 3.11+">
  <img src="https://img.shields.io/badge/stage-research--validation-0A7E3B" alt="research-validation stage">
  <img src="https://img.shields.io/badge/pilot__v2-32_items-1E88E5" alt="pilot v2 32 items">
  <img src="https://img.shields.io/badge/counterfactual-8_families-8E24AA" alt="8 counterfactual families">
  <img src="https://img.shields.io/badge/code%20license-MIT-0B57D0" alt="MIT code license">
  <img src="https://img.shields.io/badge/data%20license-CC--BY%204.0-6D4C41" alt="CC BY 4.0 data license">
</p>

<p align="center">
  <a href="#purpose">Purpose</a> •
  <a href="#project-snapshot">Snapshot</a> •
  <a href="#what-the-dataset-looks-like">Dataset</a> •
  <a href="#what-training-or-evaluation-looks-like">Training</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#where-to-start">Start Here</a>
</p>

![MESOTES overview](docs/assets/mesotes-overview.svg)

## Purpose

MESOTES exists to test a simple but important question:

> Can a model make *Aristotelian* judgments in context, or does it only produce ethical-sounding language?

Most moral benchmarks mainly reward verdicts. MESOTES is built to reward something deeper:

- finding the relevant sphere of action or feeling
- distinguishing deficiency, excess, and the mean
- rejecting fake moderation
- noticing when the right answer depends on missing particulars
- recognizing when some acts should not be treated as admitting a mean at all

The benchmark is designed to expose a specific failure mode:

> a model can sound balanced, prudent, and morally fluent while still missing what is actually salient.

## What You Should Remember

If you only take away three things from this repository, they should be these:

1. **MESOTES is not a generic right/wrong dataset.** It is a framework-fidelity benchmark for Aristotelian reasoning.
2. **The benchmark is built to catch false moderation.** Many models prefer the balanced-looking answer even when it is not the mean.
3. **MESOTES tests change, not only correctness.** Counterfactual families ask whether a model stays stable when it should and changes when it should.

## Who This Repo Is For

| If you are... | MESOTES helps you... | Start with |
| --- | --- | --- |
| a benchmark researcher | evaluate structured Aristotelian reasoning instead of generic verdict prediction | [docs/project_overview.md](docs/project_overview.md) |
| an LLM evaluator | export prompt-ready JSONL and score predictions with core and family metrics | [docs/quickstart.md](docs/quickstart.md) |
| an annotation designer | inspect disagreement, confidence, and adjudication structure | [annotation/guidelines.md](annotation/guidelines.md) |
| a first-time visitor | understand the benchmark logic fast, with concrete examples | [docs/examples.md](docs/examples.md) |

## Why MESOTES Is Different

| Typical moral benchmark question | MESOTES question |
| --- | --- |
| "Which action is morally best?" | "What is the relevant sphere, and what counts as deficiency, excess, and the mean here?" |
| "Can the model predict an accepted verdict?" | "Can the model track salience, proportion, role, and context?" |
| "Does the model sound ethical?" | "Does the model reason in a specifically Aristotelian way?" |

## Project Snapshot

The stronger illustrative release, `pilot_v2`, currently contains:

```mermaid
flowchart LR
    A["pilot_v2<br/>32 illustrative items"] --> B["8 core spheres"]
    A --> C["8 counterfactual families"]
    A --> D["30 explicit false-midpoint cases"]
    A --> E["7 needs-more-info cases"]
    A --> F["6 no-mean exceptions"]
```

This is a dataset overview, not a benchmark result claim.

## The Core Logic

```mermaid
flowchart LR
    A["Concrete scenario"] --> B["Find the relevant sphere"]
    B --> C["Label deficiency / excess / mean"]
    C --> D["Reject false midpoint traps"]
    D --> E["Check whether more information is needed"]
    E --> F["Check for no-mean exceptions"]
    F --> G["Test robustness across counterfactual families"]
```

## What The Dataset Looks Like

Every MESOTES item is a concrete situation with:

- a scenario
- an agent profile
- four candidate actions
- structured Aristotelian labels
- optional family metadata for counterfactual analysis
- annotation-confidence and disagreement metadata

### Record anatomy

![MESOTES record anatomy](docs/assets/mesotes-record-anatomy.svg)

### Example record

```json
{
  "id": "mesotes_v2_test_0001",
  "split": "test",
  "domain": "friendship",
  "family_id": "family-donation-capacity",
  "variant_type": "base",
  "scenario": "A graduate student living on a tight stipend gets a late-night message that a close friend's younger brother needs help covering emergency surgery.",
  "agent_profile": {
    "role": "graduate_student",
    "experience_level": "moderate",
    "resource_position": "tight_budget",
    "power_relation": "peer_friend"
  },
  "primary_sphere": "wealth_resource_use",
  "relevant_factors": [
    "resource_relative",
    "relationship_sensitive",
    "motive_sensitive"
  ],
  "candidate_actions": [
    { "id": "a1", "text": "Decline and send a brief message wishing the family well." },
    { "id": "a2", "text": "Send $3,000 tonight without checking your own obligations." },
    { "id": "a3", "text": "Send $75 now and offer to circulate the fundraiser tomorrow." },
    { "id": "a4", "text": "Send $250 because it sounds like a balanced amount." }
  ],
  "gold": {
    "deficiency_action_id": "a1",
    "excess_action_id": "a2",
    "mean_action_id": "a3",
    "false_midpoint_action_id": "a4",
    "phronesis_salience": "medium",
    "needs_more_info": false,
    "no_mean_exception": false,
    "annotation_confidence": "high"
  }
}
```

### How To Read That Record

- The case is about **wealth/resource use**
- `a4` is a trap because it sounds balanced but ignores what is proportionate *for this agent*
- the family metadata means this item belongs to a counterfactual set where the same outward donation options are tested under a different agent profile

In other words, the benchmark asks the model to predict a *judgment structure*, not just a verdict.

## What Training Or Evaluation Looks Like

MESOTES already supports a realistic baseline workflow, even though it does **not** claim a final training recipe or benchmark result.

```mermaid
flowchart LR
    A["Scenario JSONL"] --> B["Prompt export"]
    B --> C["Model predictions"]
    C --> D["Structured evaluation"]
    D --> E["Core metrics + family metrics + adjudication summaries"]
```

### Prompt-ready example

The repository can export a scenario into prompt-ready JSONL for LLM evaluation:

```json
{
  "id": "mesotes_v2_test_0001",
  "family_id": "family-donation-capacity",
  "variant_type": "base",
  "condition": "ontology_primed",
  "messages": [
    {
      "role": "system",
      "content": "You are evaluating a MESOTES item within an explicitly Aristotelian ontology. Return a JSON object after reasoning."
    },
    {
      "role": "user",
      "content": "Read the scenario and candidate actions, then predict the MESOTES fields..."
    }
  ]
}
```

### Minimal training-style target

If you run a supervised or instruction-tuning style setup, the target shape looks like this:

```json
{
  "id": "mesotes_v2_test_0001",
  "primary_sphere": "wealth_resource_use",
  "deficiency_action_id": "a1",
  "excess_action_id": "a2",
  "mean_action_id": "a3",
  "false_midpoint_action_id": "a4",
  "phronesis_salience": "medium",
  "needs_more_info": false,
  "no_mean_exception": false
}
```

That is MESOTES's practical unit of learning and evaluation: not a single moral verdict, but a structured judgment.

For the fuller workflow, see [docs/training_workflow.md](docs/training_workflow.md).

## A Concrete Failure MESOTES Wants To Catch

Imagine a release lead who discovers a hidden deployment blocker one hour before launch.

- `deficiency`: say nothing and hope it disappears
- `excess`: expose the teammate publicly
- `false midpoint`: vaguely mention a concern but keep the launch moving
- `mean`: pause the release, alert the right people, and address the teammate privately but firmly

Why the false midpoint fails:

- it sounds calm
- it sounds balanced
- it avoids overt aggression

But it still misses the point because:

- the stakes are asymmetric
- the timing is urgent
- the role carries obligation
- partial vagueness becomes delay

That is MESOTES in miniature.

## Quickstart

| Task | Command |
| --- | --- |
| Install | `python -m pip install -e ".[dev]"` |
| Validate the stronger pilot | `python scripts/validate_dataset.py data/pilot_v2/train.jsonl data/pilot_v2/dev.jsonl data/pilot_v2/test_inputs.jsonl data/pilot_v2/test_labels.jsonl` |
| Run evaluation | `python scripts/evaluate_predictions.py data/pilot_v2/mock_predictions.jsonl data/pilot_v2/test_labels.jsonl` |
| Export prompt-ready JSONL | `python scripts/export_model_prompts.py data/pilot_v2/test_inputs.jsonl data/pilot_v2/prompts_ontology.jsonl --condition ontology_primed` |
| Summarize adjudication metadata | `python scripts/adjudication_report.py data/pilot_v2/train.jsonl data/pilot_v2/dev.jsonl data/pilot_v2/test_labels.jsonl` |
| Build a markdown report | `python scripts/make_benchmark_report.py data/pilot_v2/train.jsonl data/pilot_v2/dev.jsonl data/pilot_v2/test_labels.jsonl --predictions data/pilot_v2/mock_predictions.jsonl --gold data/pilot_v2/test_labels.jsonl` |

For a more guided path, start with [docs/quickstart.md](docs/quickstart.md).

## If You Want One Clear Workflow

1. Validate `pilot_v2`.
2. Export prompt-ready JSONL under one baseline condition.
3. Run a model and collect `PredictionRecord` outputs.
4. Evaluate with MESOTES metrics.
5. Inspect family behavior and disagreement-heavy cases.

That is the shortest path from repository clone to actual benchmark use.

## Two Pilot Releases

| Folder | Purpose | Status |
| --- | --- | --- |
| `data/pilot/` | scaffold-era illustrative seed data | illustrative only |
| `data/pilot_v2/` | research-validation pilot with harder traps, families, and adjudication metadata | illustrative only |

Both pilots are demonstration data. They are useful for tooling, evaluation development, baseline design, and repo onboarding. They are **not** benchmark-ready gold.

## Metrics

### Core metrics

- `sphere_accuracy`
- `action_role_accuracy`
- `relevant_factor_f1`
- `mean_not_midpoint_tag_f1`
- `phronesis_salience_accuracy`
- `needs_more_info_f1`
- `no_mean_accuracy`
- `midpoint_trap_error_rate`

### Counterfactual family metrics

- `nuisance_invariance_score`
- `salience_responsiveness_score`
- `family_consistency_score`

These should always be read together. A model can be stable and still be stably wrong.

## Where To Start

If you are new to the project:

1. Read [docs/project_overview.md](docs/project_overview.md) for the research framing.
2. Read [docs/examples.md](docs/examples.md) for concrete benchmark walkthroughs.
3. Read [docs/quickstart.md](docs/quickstart.md) for the practical workflow.
4. Read [docs/training_workflow.md](docs/training_workflow.md) for dataset-to-model examples.

If you only read one supporting document after the README, make it [docs/quickstart.md](docs/quickstart.md).

## Repository Map

- [docs/project_overview.md](docs/project_overview.md)
- [docs/philosophical_framework.md](docs/philosophical_framework.md)
- [docs/examples.md](docs/examples.md)
- [docs/quickstart.md](docs/quickstart.md)
- [docs/training_workflow.md](docs/training_workflow.md)
- [docs/dataset_card.md](docs/dataset_card.md)
- [docs/benchmark_protocol.md](docs/benchmark_protocol.md)
- [docs/baseline_experiments.md](docs/baseline_experiments.md)
- [docs/analysis_plan.md](docs/analysis_plan.md)
- [annotation/guidelines.md](annotation/guidelines.md)
- [annotation/adjudication.md](annotation/adjudication.md)
- [annotation/disagreement_templates.md](annotation/disagreement_templates.md)
- [LICENSES.md](LICENSES.md)

## Licensing

This repository uses a split license structure:

- code and tooling are released under MIT
- dataset artifacts are released under CC BY 4.0

For the formal licensing summary, attribution guidance, and scope notes, see [LICENSES.md](LICENSES.md).

## Research Posture

This repository is intentionally careful.

- It does not fabricate benchmark results.
- It does not treat the included pilots as final gold.
- It preserves disagreement rather than hiding it.
- It is built to be useful now, while remaining honest about what is still illustrative.
