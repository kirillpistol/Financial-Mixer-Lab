# Synthetic account volume and load module

The `app.loadlab` module generates **fictional** accounts and rate-limited transactions only inside a local SQLite ledger. It cannot connect to financial institutions, automate account registrations, or send payments externally.

## Examples

Run with the project root in Python's import path:

```bash
python -m scripts.load_test --accounts 50 --operations 200 --tps 20
python -m scripts.load_test --accounts 50 --operations 200 --tps 20 --execute
```

Without `--execute`, no accounts or transactions are written.

## Limits
- Up to 1,000 synthetic accounts per run.
- Up to 10,000 synthetic payments per run.
- Target at most 100 transactions/sec.
- Single-threaded sequential load, to ensure resource usage remains bounded.
- Only integer-minor-unit RUB artificial balances.
- Local SQLite database only, with no configurable remote URL.

## Metrics
- Requested TPS and theoretical operation duration.
- Estimated SQL writes and journal entries (approximate).
- Successful/failed or skipped operations.
- Actual achieved TPS, elapsed seconds and p95 transfer latency.
- Double-entry invariant verification.

## Caveats
The estimate is not a real-world performance guarantee; it excludes account creation time, disk sync overhead, and read queries. Measurements depend on machine and file system. The module is useful for deterministic local workload development, not bank-scale performance claims.

Future extensions can add synthetic personas, transaction event export, alert simulation, and workload configuration. External plugins should implement explicit offline-only interfaces rather than arbitrary code execution or third-party connectors.
