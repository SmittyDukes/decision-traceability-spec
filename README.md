# Decision Traceability Spec

A spec + schemas for logging ML/LLM decisions so every decision is reproducible, auditable, and linkable to outcomes and overrides.

## Problem Statement

In production ML systems, decisions are irreversible actions that impact real-world entities.
Without strict traceability, teams cannot:

- Reconstruct what happened at decision time
- Detect silent policy misconfiguration
- Audit model or threshold drift
- Investigate human override misuse
- Link decisions to delayed outcomes

This repository defines a strict decision contract and event schema to prevent decision entropy.

## System Boundary

This repository does NOT train models.

It defines the governance layer between:
- Model inference
- Policy interpretation
- Action execution
- Human override
- Outcome reconciliation

The goal is separation of concerns:
- model_version → prediction logic
- policy_version → decision logic
- event schema → traceability layer

## Failure Modes Prevented

This specification prevents:

- Silent model swaps without auditability
- Threshold changes without version control
- Input schema drift
- Decision-rule inconsistencies
- Untracked overrides
- Irreproducible historical decisions

All decisions are versioned, schema-validated, and rule-validated before logging.

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

## Decision Lineage

Each decision participates in a lineage chain:

model_version → decision_event → override_event (optional) → outcome_event → evaluation

This enables:
- Replaying decisions
- Measuring regret
- Evaluating policy effectiveness
- Monitoring trust over time


## Key Guarantees
- Reproducible decisions via strict versioning (`model_version`, `policy_version`)
- Input contract enforcement (`additionalProperties: false`)
- Runtime decision-rule validation before action/logging
