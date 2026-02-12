import json

def validate_decision_rule(event: dict) -> None:
    score = event["model_score"]
    threshold = event["threshold"]
    decision = event["decision"]

    should_extend = score >= threshold
    if should_extend and decision != "EXTEND_MINUTES":
        raise ValueError("Decision mismatch: score>=threshold but decision != EXTEND_MINUTES")
    if (not should_extend) and decision != "HOLD_MINUTES":
        raise ValueError("Decision mismatch: score<threshold but decision != HOLD_MINUTES")

if __name__ == "__main__":
    with open("examples/decision_event.example.json", "r") as f:
        event = json.load(f)
    validate_decision_rule(event)
    print("Decision rule check passed.")
