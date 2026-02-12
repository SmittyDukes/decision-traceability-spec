# Decision Traceability Spec

A spec + schemas for logging ML/LLM decisions so every decision is reproducible, auditable, and linkable to outcomes and overrides.

## What this repo contains
- `specs/` — decision contract + traceability requirements (human-readable)
- `schemas/` — JSON Schemas for decision/outcome/override events (machine-validatable)
- `examples/` — example events that must validate against schemas
- `queries/` — audit checks to detect contract violations, policy drift, and override misuse
- `tools/` — lightweight validators (business-rule guardrails)

## Decision Lifecycle
1. **decision_event** emitted at decision time (inputs, model_version, policy_version, threshold, decision)
2. **override_event** emitted when a human overrides (who/why)
3. **outcome_event** emitted when ground truth becomes available (delayed labels)

## Key Guarantees
- Reproducible decisions via strict versioning (`model_version`, `policy_version`)
- Input contract enforcement (`additionalProperties: false`)
- Runtime decision-rule validation before action/logging
