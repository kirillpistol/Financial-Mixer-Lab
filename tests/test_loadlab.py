import pytest
from app import core
from app.loadlab import estimate, run_synthetic


def test_estimate_writes_and_duration():
    plan = estimate(10, 50, 5)
    assert plan["duration_seconds"] == 10
    assert plan["estimated_payment_writes"] == 250
    assert plan["estimated_journal_entries"] == 120
    assert plan["estimated_total_db_writes"] == 300


@pytest.mark.parametrize("accounts,operations,tps", [
    (1, 10, 5), (1001, 10, 5), (5, -1, 5), (5, 10001, 5),
    (5, 5, 0), (5, 5, 101),
])
def test_limits(accounts, operations, tps):
    with pytest.raises(ValueError):
        estimate(accounts, operations, tps)


def test_synthetic_run_is_balanced(tmp_path):
    path = str(tmp_path / "load.db")
    result = run_synthetic(3, 6, 100, seed=42, path=path)
    assert result["created_accounts"] == 3
    assert result["successful_payments"] == 6
    assert result["failed_or_skipped"] == 0
    assert result["unbalanced_transfer_ids"] == []
    assert core.validate_journal(path) == []
