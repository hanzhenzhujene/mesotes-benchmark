# Project Overview

MESOTES is a benchmark scaffold for evaluating whether models can reason within a specifically Aristotelian frame. The project focuses on framework fidelity rather than generic moral verdict prediction.

In practical terms, MESOTES asks a sharper question than "can the model sound ethical?":

Can the model identify what is morally salient in an Aristotelian way, and can it keep that judgment stable or flexible when the case changes?

## Core idea

The benchmark asks whether a model can:

- identify the relevant sphere of action or feeling
- distinguish deficiency, excess, and the mean
- reject a false midpoint that looks moderate but is still wrong
- explain which particulars matter
- recognize when better judgment requires more information
- identify cases where moderation is the wrong heuristic altogether

The research motivation is that many systems can produce fluent moral prose while still failing at:

- relevance detection
- role-sensitive judgment
- fake moderation traps
- information-gap recognition
- person-relative variation

## What MESOTES is not

MESOTES is not intended to define universal morality, recover a complete historical reconstruction of Aristotle, or rank models by agreement with public opinion. The benchmark instead asks a narrower question: how well can a model operate inside an explicitly Aristotelian annotation frame built around mesotes and phronesis?

## Repository status

This repository is a research-validation scaffold rather than a finished benchmark release. It includes:

- an ontology and annotation manual
- validated JSONL schemas
- reusable metrics and CLI scripts
- illustrative pilot datasets, including a harder counterfactual `pilot_v2`
- disagreement and adjudication metadata
- prompt-export and markdown-report tooling
- a notebook for quick exploratory analysis

The shipped pilots are seed material for iteration and should not be treated as paper-ready gold labels.
