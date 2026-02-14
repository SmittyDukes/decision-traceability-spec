# Traceability Requirements

## Goal
Every automated decision must be reproducible, auditable, and linkable to (a) overrides and (b) outcomes.

## Required Event Types
1. decision_event — emitted at decision time
2. override_event — emitted when a human overrides
3. outcome_event — emitted when ground truth becomes available

## Required Properties (Decision)
A decision_event MUST include:
- decision_id (unique)
- timestamp (ISO 8601)
- entity_id (stable identifier)
- input_features_snapshot (strict schema, no extra fields)
- model_version
- policy_version
- model_score
- threshold
- decision

## Invariants
- The decision must be consistent with the decision rule (e.g., score >= threshold → EXTEND_MINUTES).
- Event schemas are versioned; changes require version bump + backward compatibility plan.
- Decision events are immutable once written.

## Audit Questions This Must Answer
- What decision was made, when, and for whom?
- What inputs were used?
- Which model and policy interpreted the inputs?
- What threshold was applied?
- Was the decision rule applied correctly?
- Was there an override? By whom and why?
- What was the outcome later, and how did it compare?

# Audit Checklist

## Contract Integrity
- [ ] Find decisions where model_score >= threshold but decision != EXTEND_MINUTES
- [ ] Find decisions where model_score < threshold but decision != HOLD_MINUTES

## Policy & Configuration Drift
- [ ] List decisions grouped by policy_version and threshold to detect unexpected threshold changes
- [ ] Find decisions where policy_version changed within the same game context window

## Human Override Governance
- [ ] Find override events where override_reason is missing
- [ ] Flag games where override rate exceeds X% (potential trust or misuse issue)

## Immutability & Append-Only Guarantees
- Decision events MUST be append-only and immutable once written.
- Corrections MUST be expressed as new events (e.g., override_event, correction_event) referencing the original decision_id.
- Any mutation of historical decision_event records is a traceability violation.

## Schema Versioning
- All event schemas MUST include schema_version.
- Backward-incompatible changes require a major version bump.
- Producers MUST not emit events that violate the declared schema_version.

## Idempotency Requirements

- decision_id MUST be globally unique.
- decision_id MUST be deterministic per request (idempotency key).
- Storage layer MUST enforce uniqueness constraint on decision_id.
- Duplicate decision events MUST be rejected or validated as identical.
