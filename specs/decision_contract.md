# Decision Contract: Minutes Extension

## Decision
Decide whether a player’s minutes should be extended over the next 10 minutes.

## Entity
player_id

## Inputs (required)
- points (int)
- minutes_played (int)
- fouls (int)
- fatigue_index (float)
- injury_status (enum: "clear" | "limited" | "out")
- game_context (object: score_margin, quarter, time_remaining)

## Model Output
- raw_score (float)  # model score
- calibrated_prob (float)  # optional but preferred

## Policy / Decision Rule
- threshold (float)
- decision = (calibrated_prob >= threshold)

## Action Space
- EXTEND_MINUTES
- HOLD_MINUTES

## Constraints
- input_freshness_ms <= 5000 
- latency_ms <= 175
- injury_status != "out"

## Required Logging
Decision must emit a decision_event with:
decision_id, timestamp, entity_id, inputs snapshot, model scores, threshold, decision, constraints, and trace IDs.
