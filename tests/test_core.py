import pytest
from app import core


@pytest.fixture
def path(tmp_path):
    p = str(tmp_path / "lab.db")
    core.initialize(p)
    return p


def test_transfer_is_double_entry_and_conserves_balance(path):
    alice = core.create_account("Alice", "RUB", 10000, path)
    bob = core.create_account("Bob", "RUB", 0, path)
    tx = core.transfer(alice["id"], bob["id"], 3500, "tx-1", path)
    assert tx["amount"] == 3500
    assert core.get_account(alice["id"], path)["balance"] == 6500
    assert core.get_account(bob["id"], path)["balance"] == 3500
    assert [x["amount"] for x in core.ledger(bob["id"], path)] == [3500]
    assert core.validate_journal(path) == []


def test_insufficient_funds_is_atomic(path):
    a = core.create_account("A", opening_balance=100, path=path)
    b = core.create_account("B", path=path)
    with pytest.raises(ValueError, match="Insufficient"):
        core.transfer(a["id"], b["id"], 101, "too-large", path)
    assert core.get_account(a["id"], path)["balance"] == 100
    assert core.get_account(b["id"], path)["balance"] == 0


def test_idempotency(path):
    a = core.create_account("A", opening_balance=200, path=path)
    b = core.create_account("B", path=path)
    first = core.transfer(a["id"], b["id"], 50, "same", path)
    again = core.transfer(a["id"], b["id"], 50, "same", path)
    assert first["id"] == again["id"]
    assert core.get_account(b["id"], path)["balance"] == 50
    with pytest.raises(ValueError, match="Idempotency"):
        core.transfer(a["id"], b["id"], 55, "same", path)


def test_currency_and_self_transfer_rejected(path):
    a = core.create_account("A", "RUB", 100, path)
    b = core.create_account("B", "USD", 0, path)
    with pytest.raises(ValueError, match="Currency"):
        core.transfer(a["id"], b["id"], 10, "cross-currency", path)
    with pytest.raises(ValueError, match="differ"):
        core.transfer(a["id"], a["id"], 10, "self", path)
