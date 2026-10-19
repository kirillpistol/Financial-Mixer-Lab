"""Isolated transaction ledger. Amounts are integer minor currency units."""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("FML_DATABASE", "financial_lab.db")


def connect(path: str | None = None):
    db = sqlite3.connect(path or DB_PATH, timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def initialize(path: str | None = None):
    with connect(path) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          currency TEXT NOT NULL,
          balance INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS transfers (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          source INTEGER NOT NULL REFERENCES accounts(id),
          destination INTEGER NOT NULL REFERENCES accounts(id),
          amount INTEGER NOT NULL CHECK(amount > 0),
          currency TEXT NOT NULL,
          idempotency_key TEXT NOT NULL UNIQUE,
          kind TEXT NOT NULL DEFAULT 'payment',
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS entries (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          transfer_id INTEGER NOT NULL REFERENCES transfers(id),
          account_id INTEGER NOT NULL REFERENCES accounts(id),
          amount INTEGER NOT NULL CHECK(amount != 0),
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_entries_account ON entries(account_id);
        """)
    return path or DB_PATH


@contextmanager
def transaction(path: str | None = None):
    db = connect(path)
    try:
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.execute("COMMIT")
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()


def _account(db, account_id: int):
    row = db.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
    if row is None:
        raise ValueError("Account not found")
    return row


def get_account(account_id: int, path: str | None = None):
    with connect(path) as db:
        return dict(_account(db, account_id))


def create_account(name: str, currency: str = "RUB", opening_balance: int = 0,
                   path: str | None = None):
    if not name.strip() or len(name) > 120:
        raise ValueError("Invalid account name")
    if not (len(currency) == 3 and currency.isalpha() and currency.isupper()):
        raise ValueError("Currency must be three uppercase letters")
    if type(opening_balance) is not int or opening_balance < 0:
        raise ValueError("Opening balance must be nonnegative integer")
    with transaction(path) as db:
        cur = db.execute("INSERT INTO accounts(name,currency,balance) VALUES(?,?,?)",
                         (name.strip(), currency, opening_balance))
        account_id = cur.lastrowid
        if opening_balance:
            system_name = "__SYSTEM_FUNDING__:" + currency
            system = db.execute("SELECT * FROM accounts WHERE name=?",
                                (system_name,)).fetchone()
            if system is None:
                system_id = db.execute(
                    "INSERT INTO accounts(name,currency,balance) VALUES(?,?,0)",
                    (system_name, currency)).lastrowid
            else:
                system_id = system["id"]
            db.execute("UPDATE accounts SET balance=balance-? WHERE id=?",
                       (opening_balance, system_id))
            transfer_id = db.execute(
                """INSERT INTO transfers(source,destination,amount,currency,
                   idempotency_key,kind) VALUES(?,?,?,?,?,?)""",
                (system_id, account_id, opening_balance, currency,
                 f"funding:{account_id}", "simulation_funding")).lastrowid
            db.executemany(
                "INSERT INTO entries(transfer_id,account_id,amount) VALUES(?,?,?)",
                [(transfer_id, system_id, -opening_balance),
                 (transfer_id, account_id, opening_balance)])
    return get_account(account_id, path)


def transfer(source: int, destination: int, amount: int, key: str,
             path: str | None = None):
    if source == destination:
        raise ValueError("Source and destination must differ")
    if type(amount) is not int or amount <= 0:
        raise ValueError("Amount must be a positive integer")
    if not key or len(key) > 128 or key.startswith("funding:"):
        raise ValueError("Invalid idempotency key")
    with transaction(path) as db:
        previous = db.execute("SELECT * FROM transfers WHERE idempotency_key=?",
                              (key,)).fetchone()
        if previous:
            if (previous["source"], previous["destination"], previous["amount"]) != (
                    source, destination, amount):
                raise ValueError("Idempotency key reused for different payment")
            result = dict(previous)
        else:
            a, b = _account(db, source), _account(db, destination)
            if a["currency"] != b["currency"]:
                raise ValueError("Currency mismatch")
            if a["name"].startswith("__SYSTEM_FUNDING__:") or b["name"].startswith("__SYSTEM_FUNDING__:"):
                raise ValueError("System account cannot be used in payments")
            if a["balance"] < amount:
                raise ValueError("Insufficient funds")
            transfer_id = db.execute(
                """INSERT INTO transfers(source,destination,amount,currency,
                   idempotency_key) VALUES(?,?,?,?,?)""",
                (source, destination, amount, a["currency"], key)).lastrowid
            db.execute("UPDATE accounts SET balance=balance-? WHERE id=?",
                       (amount, source))
            db.execute("UPDATE accounts SET balance=balance+? WHERE id=?",
                       (amount, destination))
            db.executemany(
                "INSERT INTO entries(transfer_id,account_id,amount) VALUES(?,?,?)",
                [(transfer_id, source, -amount), (transfer_id, destination, amount)])
            result = dict(db.execute("SELECT * FROM transfers WHERE id=?",
                                     (transfer_id,)).fetchone())
    return result


def get_transfer(transfer_id: int, path: str | None = None):
    with connect(path) as db:
        result = db.execute("SELECT * FROM transfers WHERE id=?",
                            (transfer_id,)).fetchone()
        if result is None:
            raise ValueError("Transfer not found")
        return dict(result)


def ledger(account_id: int, path: str | None = None):
    with connect(path) as db:
        _account(db, account_id)
        return [dict(x) for x in db.execute(
            """SELECT e.*, t.kind, t.currency FROM entries e
               JOIN transfers t ON e.transfer_id=t.id
               WHERE account_id=? ORDER BY e.id""", (account_id,))]


def validate_journal(path: str | None = None):
    """Return IDs of unbalanced transfers (normally empty)."""
    with connect(path) as db:
        return [r["transfer_id"] for r in db.execute(
            """SELECT transfer_id FROM entries GROUP BY transfer_id
               HAVING COUNT(*) != 2 OR SUM(amount) != 0""")]
