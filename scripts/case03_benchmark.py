"""CASE 003 reproducible synthetic AML/QA benchmark. Artificial data only."""
from __future__ import annotations
import argparse
import json
import random
from pathlib import Path
from app.case03_monitor import Observation, detect, evaluate

SEED = 3003
PLANNED_FACE_VALUE_USD = 6_000_000  # Narrator's nominal starting figure; not deposits.

def benchmark(seed: int = SEED, count: int = 200) -> dict:
    if count < 20 or count > 5000:
        raise ValueError("count must be between 20 and 5000")
    rng = random.Random(seed)
    observations = []
    positive = set()
    kinds = ("cash_exception", "credit_posted", "merchant_dispute",
             "mandate_invalid", "identity_mismatch", "payout_review",
             "notification_spike", "complaint", "benign_purchase")
    by_kind = dict.fromkeys(kinds, 0)
    # This is NOT a real distribution: 25% deliberately labelled positives.
    for i in range(count):
        case_id = f"FIC-{i+1:05d}"
        is_positive = i % 4 == 0
        if is_positive:
            positive.add(case_id)
            pattern = ["cash_exception", "credit_posted", "merchant_dispute",
                       "mandate_invalid", "identity_mismatch", "payout_review"]
            if rng.random() < .35:
                pattern.append("complaint")
            if rng.random() < .50:
                pattern.append("notification_spike")
        else:
            pattern = ["benign_purchase"]
            if rng.random() < .3:
                pattern.append("notification_spike")
            # Benign operational exceptions intentionally exercise false positives.
            if rng.random() < .12:
                pattern += ["cash_exception", "credit_posted"]
            if rng.random() < .15:
                pattern.append("complaint")
        for j, kind in enumerate(pattern):
            observations.append(Observation(case_id, j, kind, f"{case_id}-{j}"))
            by_kind[kind] += 1
    findings = detect(observations)
    metrics = evaluate(findings, positive,
                       {f"FIC-{i+1:05d}" for i in range(count)})
    alerts = {}
    for finding in findings:
        alerts[finding["rule"]] = alerts.get(finding["rule"], 0) + 1
    return {
        "dataset": "FICTIONAL_QA_ONLY",
        "seed": seed, "cases": count,
        "planned_face_value_usd_context_only": PLANNED_FACE_VALUE_USD,
        "actual_deposit_amount_usd": None,
        "actual_loss_usd": None,
        "synthetic_positive_labels": len(positive),
        "synthetic_negative_labels": count - len(positive),
        "observations_total": len(observations),
        "observations_by_type": by_kind,
        "alerts_by_rule": alerts,
        "metrics": metrics,
        "interpretation": "Invented labels and events; not empirically estimated crime or bank rates."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--cases", type=int, default=200)
    parser.add_argument("--output", default="case03_benchmark.json")
    args = parser.parse_args()
    result = benchmark(args.seed, args.cases)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
