# Financial Mixer Lab

Open research sandbox for simulating payment flows and studying transaction monitoring.

**Safety boundary:** simulated funds only. No live bank connections, real payment rails, anonymity service, or monitoring evasion.

## Features
- SQLite-backed accounts and double-entry transfers.
- Integer minor-unit balances (no floating-point money).
- Atomic debit/credit with insufficient-funds rejection.
- Idempotency keys and immutable journal entries.
- Read-only account, ledger and transfer inspection API.
- Monitoring-oriented synthetic case annotations can be added later.

## Run

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs.

## Test

```bash
python -m pytest -q
```

SQLite data defaults to `financial_lab.db`; set `FML_DATABASE` to change it. Monetary values are expressed as integer minor units (e.g. 10000 = 100.00 RUB). Use only fictional identities and artificial balances.

## API
- `POST /accounts` with `{"name":"Alice","currency":"RUB","opening_balance":100000}`
- `GET /accounts/{account_id}`
- `POST /transfers` with `{"from_account":1,"to_account":2,"amount":2000,"idempotency_key":"demo-001"}`
- `GET /transfers/{transfer_id}`
- `GET /ledger/{account_id}`

Opening balances are journaled against a synthetic system funding account per currency. No deposits or withdrawals of real money are supported.

## Next milestone
Add anonymized historical case descriptions, synthetic replay events, alerts, and monitoring evaluation metrics (recall, precision, false-positive rate).
