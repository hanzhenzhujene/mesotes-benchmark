# Contributing to MESOTES

Thank you for helping improve MESOTES.

## Scope

MESOTES is intended as a framework-fidelity benchmark scaffold for Aristotelian reasoning. Contributions should preserve that focus. Changes that flatten the benchmark into generic right/wrong classification are usually out of scope unless they clearly support the Aristotelian task structure.

## Development setup

```bash
python -m pip install -e ".[dev]"
pytest
```

Useful first commands:

```bash
python scripts/validate_dataset.py data/pilot_v2/train.jsonl data/pilot_v2/dev.jsonl data/pilot_v2/test_inputs.jsonl data/pilot_v2/test_labels.jsonl
python scripts/evaluate_predictions.py data/pilot_v2/mock_predictions.jsonl data/pilot_v2/test_labels.jsonl
python scripts/adjudication_report.py data/pilot_v2/train.jsonl data/pilot_v2/dev.jsonl data/pilot_v2/test_labels.jsonl
```

## Contribution guidelines

- Keep claims careful and sourceable. Do not add benchmark results or literature comparisons without citations.
- Preserve the split between code and data licensing. Code is MIT licensed; released dataset artifacts are CC BY 4.0 licensed.
- Treat the pilot data as illustrative seed material rather than adjudicated gold.
- Add or update tests whenever you change schema, metrics, or CLI behavior.
- Prefer concrete, context-rich examples over abstract moral prompts.
- Keep the repo welcoming to first-time readers. If you add a powerful feature, add the example or quickstart note that makes it discoverable.

## Pull requests

- Describe the motivation for the change.
- Note any schema, ontology, or annotation-guideline updates.
- Include validation commands or test results when relevant.
