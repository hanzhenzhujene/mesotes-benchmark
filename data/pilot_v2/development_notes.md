# Pilot v2 Development Notes

`data/pilot_v2/` is an illustrative research-validation pilot. It is stronger than the original scaffold pilot, but it is still not benchmark-ready gold.

The main additions are:

- counterfactual family structure
- harder false-midpoint cases
- more under-specified items
- more no-mean exceptions
- explicit annotation-confidence and disagreement metadata

## Counterfactual families

### `family-donation-capacity`

- Sphere: `wealth_resource_use`
- Purpose: test person-relative judgment through an `agent_shift`
- Design: the same outward donation options appear under materially different resource positions, so a fixed "middle amount" should not stay stable

### `family-lab-feedback-noise`

- Sphere: `truthfulness_self_presentation`
- Purpose: test `irrelevant_detail_shift`
- Design: salient facts stay fixed while room, weather, and incidental details move; the correct structured judgment should remain stable

### `family-asthma-care-plan`

- Sphere: `fear_confidence`
- Purpose: test `salience_shift`
- Design: the base case is under-specified and favors information-seeking practical judgment, while the variant adds acute danger cues that should change the best action

### `family-team-joke-channel`

- Sphere: `social_pleasantness`
- Purpose: test `role_shift`
- Design: the same chat comment should be handled differently by a peer versus a manager responsible for channel norms

### `family-playground-teasing`

- Sphere: `amusement_humor`
- Purpose: test `salience_shift`
- Design: the difference between one-off teasing and a repeated humiliating pattern should matter to the degree and manner of intervention

### `family-neighbor-fence-role`

- Sphere: `anger_response`
- Purpose: test `role_shift`
- Design: private neighbor conduct and condo-board mediation should not collapse into the same response

### `family-award-credit`

- Sphere: `honor_recognition`
- Purpose: test `minimal_pair`
- Design: small wording changes around award criteria make it harder to rely on canned "share the credit" responses

### `family-dessert-duty`

- Sphere: `pleasure_appetite`
- Purpose: test `agent_shift`
- Design: tasting boundaries look different for a volunteer helper than for the pastry chef responsible for quality control

## Review metadata

The new metadata fields are intentionally modest:

- `annotation_confidence` signals how stable the illustrative label looks under the current guidelines
- `disagreement_flags` highlights where a future annotator or adjudicator may want to revisit the item
- `adjudication_note` stores a short internal memo instead of pretending every hard case is fully settled
- `author_intended_trap_type` marks why a false midpoint was authored, but it is not intended as model-facing gold

## Release caution

This folder is still scaffold-era illustrative material. It is designed to support better validation tooling and baseline experimentation, not to stand in for a final expert-adjudicated release.
