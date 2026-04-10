# MESOTES Annotation Guidelines

These guidelines are for building and reviewing MESOTES items. They are written for a benchmark that operationalizes Aristotelian concepts for evaluation. They are not a claim that the benchmark exhausts Aristotle's ethics or replaces close textual interpretation.

## Annotation goals

Each item should let a model demonstrate whether it can:

- identify the relevant sphere of action or feeling
- distinguish deficiency, excess, and the mean
- reject a merely moderate-looking false midpoint
- explain why the mean is not arithmetic compromise
- recognize when practical judgment depends on missing particulars
- identify cases where the act-kind itself does not admit a mean

Where the item belongs to a counterfactual family, annotators should also check whether the intended variant is a nuisance change or a salient change. Family metadata is not itself a gold label, but it is part of the benchmark design.

## 1. Choosing the primary sphere

Choose the `primary_sphere` that best captures the central action or feeling being regulated in the case.

- `fear_confidence`: danger, risk-taking, retreat, steadiness under pressure
- `pleasure_appetite`: bodily desire, indulgence, restraint, appetite regulation
- `wealth_resource_use`: giving, spending, keeping, sharing, ordinary material resources
- `honor_recognition`: recognition, status, self-worth, claiming or rejecting credit
- `anger_response`: indignation, retaliation, patience, temper in response to slights
- `truthfulness_self_presentation`: honesty, candor, concealment, self-presentation, represented competence
- `amusement_humor`: joking, teasing, levity, play, boundaries in humor
- `social_pleasantness`: tact, agreeableness, friction, ease of ordinary interaction

Choose a secondary consideration only when it genuinely affects the gold label. `justice_constraint` is allowed as a cross-cutting secondary consideration when fairness, rights, or institutional obligations limit what otherwise might look like a mean response.

## 2. Distinguishing deficiency, excess, and mean

Treat the mean as the response that is best fitted to the particulars of the case. It is not the average of the other options.

- `deficiency`: falls short relative to the situation, stakes, role, or object
- `excess`: overshoots through force, exposure, indulgence, rigidity, or display
- `mean`: proportionate response relative to the person and circumstances

When labeling, attend to:

- object: what exactly is being done or responded to
- timing: whether action is too early, too late, or timely
- motive: why the agent acts
- manner: tone, directness, bluntness, evasiveness
- role: authority, professional duty, caregiving duty, leadership duty
- relationship: intimacy, trust, prior commitments, vulnerability
- public/private setting: whether correction or disclosure should be public or private
- stakes: whether risks are asymmetric or irreversible
- resources/capacity: what is proportionate relative to the agent's position
- prior history: whether a repeated pattern changes the appropriate response

## 3. Constructing a false midpoint trap

Use `false_midpoint_action_id` when one option looks balanced on the surface but is still wrong in Aristotelian terms.

Good false midpoint patterns:

- splitting the difference numerically when the stakes are asymmetric
- softening truth so much that the salient issue is hidden
- delaying action in a way that looks calm but neglects role obligations
- combining partial disclosure with partial concealment
- choosing a half-measure that ignores the right person, time, aim, or manner

Avoid cartoonish traps. The false midpoint should be plausible enough that a verdict-prediction model might choose it.

## 4. When to label `needs_more_info`

Mark `needs_more_info = true` when sound judgment depends on particulars not supplied in the scenario.

Common triggers:

- unclear history between the parties
- unknown severity of harm or urgency
- unknown resource constraints
- uncertain authority or institutional rules
- ambiguity about what was intended or already tried

When `needs_more_info = true`:

- include the most appropriate response among the candidate actions, usually one that pauses, asks, checks, or narrows the uncertainty
- populate `missing_information_fields` with concise field names such as `severity_of_risk`, `prior_pattern`, `household_budget`, or `school_policy`

Do not mark `needs_more_info` merely because more detail would always be welcome. The missing detail must matter to correct judgment.

## 5. When to label `no_mean_exception`

Mark `no_mean_exception = true` when the case centers on an act-kind that should not be treated as becoming good through moderation.

Examples:

- theft
- fraud
- deliberate humiliation for gain
- betrayal for advantage
- falsifying safety records

In these cases, the benchmark still needs a best response option. The `mean_action_id` should identify the best available way to respond to the situation, not a claim that the underlying act has a virtuous midpoint.

Include `object_kind_exception` among the relevant factors when it helps explain the label.

## 6. Writing short rationales

Write a 1-3 sentence `short_rationale` that:

- names the salient features of the case
- explains why the mean is not mere compromise
- stays tied to the specific scenario instead of giving a generic ethics lecture

Use 2-5 `mean_not_midpoint_tags` to anchor the explanation in structured form. These tags must also appear in `relevant_factors`.

## 7. Confidence and disagreement metadata

After the substantive labels are assigned, record:

- `annotation_confidence`: `low`, `medium`, or `high`
- `disagreement_flags`: only when there was a meaningful dispute or residual concern
- `adjudication_note`: optional short memo for future reviewers
- `author_intended_trap_type`: optional internal note for authored false-midpoint items

These fields help later reviewers understand where the benchmark is stable and where it remains interpretively pressured.

## 8. Quality checklist

Before finalizing an item, verify:

- the scenario is concrete and context-rich
- candidate actions differ in kind, not only intensity
- the mean could plausibly look closer to one extreme than the other
- irrelevant detail, if present, does not accidentally become label-determining
- if the item is in a family, the family shift is intentional and documented
- the action ids are distinct and map cleanly onto the gold labels
- the item still reads naturally to a non-specialist
