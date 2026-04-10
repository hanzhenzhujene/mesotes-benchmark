from __future__ import annotations

from mesotes.validators import load_ontology, validate_ontology_alignment


def test_ontology_alignment_matches_python_taxonomy() -> None:
    ontology = validate_ontology_alignment()
    assert ontology["core_spheres"]
    assert ontology["advanced_modules"]
    assert ontology["explanation_tags"]
    assert ontology["phronesis_salience"]


def test_ontology_loader_parses_expected_sections() -> None:
    ontology = load_ontology()
    assert set(ontology) == {
        "core_spheres",
        "advanced_modules",
        "explanation_tags",
        "phronesis_salience",
    }

