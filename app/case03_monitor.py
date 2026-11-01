"""CASE 003: offline defensive correlation of fictional incident observations.

No payment execution, network calls, card data, SMS delivery or external integrations.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Observation:
    case_id: str
    minute: int
    kind: str
    reference: str
    verified: bool = True

    def __post_init__(self):
        if not self.case_id or not self.reference or self.minute < 0:
            raise ValueError("Case ID, reference and nonnegative minute required")
        if self.kind not in {
            "cash_exception", "credit_posted", "mandate_invalid",
            "merchant_dispute", "notification_spike", "payout_review",
            "complaint", "identity_mismatch", "benign_purchase",
        }:
            raise ValueError("Unknown synthetic observation type")


RULES = {
    "CASH_CREDIT_REVIEW": ("cash_exception", "credit_posted"),
    "BILLING_CONSENT_REVIEW": ("mandate_invalid", "merchant_dispute"),
    "IDENTITY_PAYOUT_REVIEW": ("identity_mismatch", "payout_review"),
    "SILENT_FRAUD_REVIEW": ("cash_exception", "merchant_dispute"),
}


def detect(observations: Iterable[Observation]) -> list[dict]:
    """Correlate *verified* observations per case, preserving evidence references.

    No thresholds for real transaction amounts or actionable operational timing.
    """
    by_case: dict[str, list[Observation]] = defaultdict(list)
    for obs in observations:
        if obs.verified:
            by_case[obs.case_id].append(obs)
    findings = []
    for case_id, events in sorted(by_case.items()):
        for rule, required in RULES.items():
            chosen = [next((e for e in sorted(events, key=lambda x: x.minute)
                            if e.kind == kind), None) for kind in required]
            if any(event is None for event in chosen):
                continue
            if rule == "SILENT_FRAUD_REVIEW" and any(e.kind == "complaint" for e in events):
                continue
            if rule == "SILENT_FRAUD_REVIEW":
                label = "Correlated incident with no complaint on record"
            else:
                label = "Independent evidence review required"
            findings.append({
                "case_id": case_id, "rule": rule, "label": label,
                "evidence": [e.reference for e in chosen],
                "observed_at_minute": max(e.minute for e in chosen),
                "is_proof_of_fraud": False,
            })
    return findings


def evaluate(findings: list[dict], positives: set[str], all_cases: set[str]) -> dict:
    """Case-level precision / recall on fictional, labelled examples."""
    flagged = {f["case_id"] for f in findings}
    if not positives <= all_cases or not flagged <= all_cases:
        raise ValueError("Labels and findings must refer to known cases")
    tp = len(flagged & positives)
    fp = len(flagged - positives)
    fn = len(positives - flagged)
    tn = len(all_cases - positives - flagged)
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(tp / (tp + fp), 3) if tp + fp else 0.0,
        "recall": round(tp / (tp + fn), 3) if tp + fn else 0.0,
        "false_positive_rate": round(fp / (fp + tn), 3) if fp + tn else 0.0,
    }


def demo() -> dict:
    """Deterministic demonstration with unrelated fictional cases."""
    rows = [
        Observation("SYN-01", 0, "cash_exception", "atm-review-01"),
        Observation("SYN-01", 3, "credit_posted", "ledger-01"),
        Observation("SYN-01", 11, "merchant_dispute", "dispute-01"),
        Observation("SYN-01", 12, "notification_spike", "notice-01"),
        Observation("SYN-01", 13, "mandate_invalid", "consent-01"),
        Observation("SYN-01", 18, "identity_mismatch", "kyc-01"),
        Observation("SYN-01", 19, "payout_review", "review-01"),
        Observation("SYN-02", 2, "benign_purchase", "purchase-02"),
        Observation("SYN-02", 7, "notification_spike", "notice-02"),
        Observation("SYN-03", 4, "cash_exception", "atm-03"),
        Observation("SYN-03", 5, "credit_posted", "ledger-03"),
        Observation("SYN-03", 6, "complaint", "complaint-03"),
    ]
    findings = detect(rows)
    return {"scope": "synthetic-only", "observations": [asdict(r) for r in rows],
            "findings": findings,
            "metrics": evaluate(findings, {"SYN-01"}, {"SYN-01", "SYN-02", "SYN-03"})}
