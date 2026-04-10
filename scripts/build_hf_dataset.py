#!/usr/bin/env python
"""Generate a lightweight Hugging Face datasets loader script."""

from __future__ import annotations

from pathlib import Path

import typer


app = typer.Typer(add_completion=False, help="Generate a Hugging Face datasets loader script.")


HF_LOADER_TEMPLATE = '''"""Hugging Face datasets loader for the MESOTES benchmark."""

import json
from pathlib import Path

import datasets


_CITATION = """\
@misc{{mesotes_benchmark,
  title={{MESOTES: An Aristotelian Benchmark for Phronesis and the Doctrine of the Mean}},
  author={{Hanzhen Zhu}},
  year={{2026}},
  note={{Repository scaffold and illustrative pilot release}},
}}
"""

_DESCRIPTION = """\
MESOTES is a benchmark scaffold for evaluating Aristotelian reasoning with
structured labels for sphere identification, action roles, false midpoint
rejection, phronesis salience, and no-mean exceptions.
"""


class MesotesConfig(datasets.BuilderConfig):
    pass


class Mesotes(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.1.0")
    BUILDER_CONFIGS = [MesotesConfig(name="default", version=VERSION)]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            features=datasets.Features({{"record": datasets.Value("string")}}),
        )

    def _split_generators(self, dl_manager):
        data_dir = Path(self.config.data_dir or "{data_dir}")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={{"path": data_dir / "train.jsonl"}},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={{"path": data_dir / "dev.jsonl"}},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={{"path": data_dir / "test_labels.jsonl"}},
            ),
        ]

    def _generate_examples(self, path):
        with Path(path).open("r", encoding="utf-8") as handle:
            for index, line in enumerate(handle):
                if not line.strip():
                    continue
                yield index, {{"record": line.strip()}}
'''


@app.command()
def main(
    output_path: Path = typer.Argument(...),
    data_dir: Path = typer.Option(
        Path("data/pilot"), help="Directory containing train/dev/test_labels JSONL files."
    ),
) -> None:
    """Write a minimal datasets loader script to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        HF_LOADER_TEMPLATE.format(data_dir=data_dir.as_posix()), encoding="utf-8"
    )
    typer.echo(f"wrote loader script to {output_path}")


if __name__ == "__main__":
    app()
