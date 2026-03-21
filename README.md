# Decision Traceability Spec

A specification and schema layer for logging ML/LLM decisions so every decision is reproducible, auditable, and linked to outcomes, policies, and human overrides.

This project defines how decisions should be recorded, validated, versioned, and analyzed to ensure reliability and accountability in production systems.

## Problem Statement

In production ML systems, decisions are irreversible actions that impact real-world entities.
Without strict traceability, teams cannot:

- Reconstruct what happened at decision time
- Detect silent policy misconfiguration
- Audit model or threshold drift
- Investigate human override misuse
- Link decisions to delayed outcomes
Predictions may also fail silently due to:
- Schema mismatches
- Missing or invalid inputs
- Inconsistent decision logic across versions
This repository defines a strict decision contract to prevent decision entropy and make every decision inspectable.


## System Boundary
This repository does NOT train models or perform inference.

It defines the governance layer between:
- Model inference
- Policy interpretation
- Action execution
- Human override
- Outcome reconciliation
  
The goal is strict separation of concerns:
- model_version → prediction logic
- policy_version → decision logic
- event schema → traceability and audit layer
This ensures decisions remain reproducible even as models and policies evolve.

## System Integration

This specification was developed alongside the Minutes Extension ML System, which implements the decision logging, schema validation, and versioning patterns defined here.

The ML system demonstrates these contracts in a working FastAPI inference service, including:

- structured prediction responses
- threshold-based decisions
- JSONL-based event logging
Together, these repositories form a complete ML decision system:
- model → prediction
- policy → decision
- spec → traceability


## Decision Contract

Each model prediction is recorded as a structured decision event.

Required Fields:

- decision_id — unique identifier for traceability
- timestamp — event time in ISO format
- model_version — version of the model used
- policy_version — version of decision logic
- inputs — snapshot of input features
- extend_probability — model output probability
- threshold — decision boundary
- decision — final action (extend / do_not_extend)
- reason — explanation for the decision

Example:
{
  "decision_id": "792936ac-f022-4424-abbb-eb06551874be",
  "timestamp": "2026-03-20T22:14:00Z",
  "model_version": "v1",
  "policy_version": "p1",
  "inputs": {
    "minutes_played": 30,
    "fatigue_index": 0.55,
    "fouls": 3,
    "time_left": 240,
    "score_margin": 2,
    "timeouts_left": 1
  },
  "extend_probability": 0.87,
  "threshold": 0.60,
  "decision": "extend",
  "reason": "probability_above_threshold"
}

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


## Failure Modes Prevented
This specification explicitly guards against:
- Silent model swaps without auditability
- Threshold changes without version control
- Input schema drift
- Decision-rule inconsistencies
- Untracked overrides
- Irreproducible historical decisions
  
Additionally, it surfaces core ML/LLM failure classes:

1. Format Drift
Output does not match expected schema

2. Missing Context
Required inputs are absent or incomplete

3. Hallucinated Context
Model introduces unsupported information

4. Constraint Violation
Decision violates defined policies or rules

5. Overconfident Uncertainty
High-confidence predictions in low-signal scenarios

All decisions are schema-validated and rule-validated before logging.


## Key Guarantees
- Reproducible decisions via strict versioning (model_version, policy_version)
- Input contract enforcement (additionalProperties: false)
- Runtime decision-rule validation before execution
- Full audit trail across model, policy, and human layers

  ## What this repo contains
- `specs/` — decision contract + traceability requirements (human-readable)
- `schemas/` — JSON Schemas for decision/outcome/override events (machine-validatable)
- `examples/` — example events that must validate against schemas
- `queries/` — audit checks to detect contract violations, policy drift, and override misuse
- `tools/` — lightweight validators (business-rule guardrails)
