# Quickstart

This quickstart is for first-time visitors who want to see the repository do something useful in a few minutes.

## 1. Install

```bash
python -m pip install -e ".[dev]"
```

MESOTES targets Python 3.11+.

## 2. Validate the research-validation pilot

```bash
python scripts/validate_dataset.py \
  data/pilot_v2/train.jsonl \
  data/pilot_v2/dev.jsonl \
  data/pilot_v2/test_inputs.jsonl \
  data/pilot_v2/test_labels.jsonl
```

What this shows:

- the JSONL files are schema-valid
- the ontology and Pydantic models agree
- the blind inputs and labeled records have the expected structure

## 3. Run evaluation on the mock predictions

```bash
python scripts/evaluate_predictions.py \
  data/pilot_v2/mock_predictions.jsonl \
  data/pilot_v2/test_labels.jsonl
```

What to notice:

- core accuracy metrics
- midpoint-trap behavior
- family metrics such as nuisance invariance and salience responsiveness

The included mock predictions are for tooling demonstration only. They are not research claims.

## 4. Generate an adjudication summary

```bash
python scripts/adjudication_report.py \
  data/pilot_v2/train.jsonl \
  data/pilot_v2/dev.jsonl \
  data/pilot_v2/test_labels.jsonl
```

What this shows:

- confidence distribution
- disagreement-flag counts
- which items look most in need of expert review

## 5. Export prompt-ready JSONL

```bash
python scripts/export_model_prompts.py \
  data/pilot_v2/test_inputs.jsonl \
  data/pilot_v2/prompts_direct.jsonl \
  --condition direct
```

Try the other baseline conditions too:

- `direct`
- `chain_of_thought`
- `ontology_primed`
- `glossary_retrieval`

If you want to understand how those exported records relate to training or fine-tuning workflows, read [docs/training_workflow.md](training_workflow.md).

## 6. Build a benchmark report

```bash
python scripts/make_benchmark_report.py \
  data/pilot_v2/train.jsonl \
  data/pilot_v2/dev.jsonl \
  data/pilot_v2/test_labels.jsonl \
  --predictions data/pilot_v2/mock_predictions.jsonl \
  --gold data/pilot_v2/test_labels.jsonl
```

This produces a compact markdown-ready summary of:

- dataset composition
- variant-type counts
- annotation-confidence distribution
- disagreement-flag distribution
- metric outputs

## Recommended reading order

If you want the fast conceptual path:

1. [README.md](../README.md)
2. [docs/examples.md](examples.md)
3. [docs/benchmark_protocol.md](benchmark_protocol.md)

If you want the research-design path:

1. [docs/project_overview.md](project_overview.md)
2. [docs/philosophical_framework.md](philosophical_framework.md)
3. [docs/baseline_experiments.md](baseline_experiments.md)
4. [docs/training_workflow.md](training_workflow.md)
5. [docs/analysis_plan.md](analysis_plan.md)
