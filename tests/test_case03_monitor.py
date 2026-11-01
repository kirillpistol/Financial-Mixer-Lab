from app.case03_monitor import Observation, detect, demo, evaluate
import pytest


def test_demo_detects_unreported_correlated_incident():
    result = demo()
    a = [f for f in result["findings"] if f["case_id"] == "SYN-01"]
    assert {f["rule"] for f in a} == {
        "CASH_CREDIT_REVIEW", "BILLING_CONSENT_REVIEW",
        "IDENTITY_PAYOUT_REVIEW", "SILENT_FRAUD_REVIEW"}
    assert all(not f["is_proof_of_fraud"] for f in a)


def test_unverified_observation_does_not_trigger():
    events = [Observation("A", 0, "cash_exception", "a"),
              Observation("A", 1, "credit_posted", "b", verified=False)]
    assert detect(events) == []


def test_complaint_excludes_silent_rule():
    events = [Observation("A", 0, "cash_exception", "a"),
              Observation("A", 1, "merchant_dispute", "b"),
              Observation("A", 2, "complaint", "c")]
    assert all(f["rule"] != "SILENT_FRAUD_REVIEW" for f in detect(events))


def test_benign_noise_does_not_trigger():
    events = [Observation("B", 0, "benign_purchase", "a"),
              Observation("B", 1, "notification_spike", "b")]
    assert detect(events) == []


def test_metrics_and_reproducibility():
    d = demo()
    assert d == demo()
    assert d["metrics"] == {"tp": 1, "fp": 1, "fn": 0, "tn": 1,
                            "precision": 0.5, "recall": 1.0,
                            "false_positive_rate": 0.5}


def test_rejects_invalid_kind():
    with pytest.raises(ValueError):
        Observation("A", 0, "unknown", "ref")
