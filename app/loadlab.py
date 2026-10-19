"""Bounded, synthetic-account workload generator. No external payment rails."""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, asdict
from app import core

MAX_ACCOUNTS = 1000
MAX_OPERATIONS = 10000
MAX_RATE = 100


@dataclass(frozen=True)
class WorkloadPlan:
    accounts: int
    operations: int
    target_tps: float
    duration_seconds: float
    estimated_accounts_per_second: float
    estimated_payment_writes: int
    estimated_journal_entries: int
    estimated_total_db_writes: int


def estimate(accounts: int, operations: int, target_tps: float) -> dict:
    if type(accounts) is not int or not 2 <= accounts <= MAX_ACCOUNTS:
        raise ValueError(f"accounts must be 2..{MAX_ACCOUNTS}")
    if type(operations) is not int or not 0 <= operations <= MAX_OPERATIONS:
        raise ValueError(f"operations must be 0..{MAX_OPERATIONS}")
    if not 0 < target_tps <= MAX_RATE:
        raise ValueError(f"target_tps must be >0 and <= {MAX_RATE}")
    # Per funded account: account insert, funding transfer, two entries and balance update.
    # Per payment: transfer insert, two balance updates, two entries.
    payment_writes = operations * 5
    return asdict(WorkloadPlan(
        accounts=accounts, operations=operations, target_tps=target_tps,
        duration_seconds=operations / target_tps,
        estimated_accounts_per_second=0.0,
        estimated_payment_writes=payment_writes,
        estimated_journal_entries=accounts * 2 + operations * 2,
        estimated_total_db_writes=accounts * 5 + payment_writes,
    ))


def run_synthetic(accounts: int, operations: int, target_tps: float = 10,
                  seed: int = 1, path: str | None = None) -> dict:
    """Generate fictional accounts and replay controlled inter-account payments.

    Intended for a fresh isolated database. No threads, credentials, or external APIs.
    Throughput is rate limited with a monotonic clock; slow systems may achieve less.
    """
    plan = estimate(accounts, operations, target_tps)
    if type(seed) is not int:
        raise ValueError("seed must be integer")
    rng = random.Random(seed)
    core.initialize(path)
    stamp = f"synthetic-{time.time_ns()}-{rng.randrange(10**9)}"
    ids = [core.create_account(f"{stamp}-account-{i}", "RUB", 100000,
                               path)["id"] for i in range(accounts)]
    latencies_ms = []
    started = time.perf_counter()
    errors = 0
    for i in range(operations):
        due = started + i / target_tps
        delay = due - time.perf_counter()
        if delay > 0:
            time.sleep(delay)
        src_index = rng.randrange(accounts)
        dst_index = rng.randrange(accounts - 1)
        if dst_index >= src_index:
            dst_index += 1
        src, dst = ids[src_index], ids[dst_index]
        current = core.get_account(src, path)["balance"]
        if current <= 0:
            # Skip rather than mint additional funds or risk a failed payment.
            errors += 1
            continue
        amount = min(current, rng.randint(1, 100))
        t0 = time.perf_counter()
        try:
            core.transfer(src, dst, amount, f"{stamp}-payment-{i}", path)
        except ValueError:
            errors += 1
        else:
            latencies_ms.append((time.perf_counter() - t0) * 1000)
    elapsed = time.perf_counter() - started
    latencies_ms.sort()
    p95 = latencies_ms[min(len(latencies_ms) - 1, max(0, int(len(latencies_ms) * .95)))] if latencies_ms else 0.0
    return {
        "mode": "synthetic_only", "plan": plan, "created_accounts": len(ids),
        "successful_payments": len(latencies_ms), "failed_or_skipped": errors,
        "elapsed_seconds": round(elapsed, 4),
        "achieved_tps": round(len(latencies_ms) / elapsed, 2) if elapsed else 0.0,
        "p95_payment_latency_ms": round(p95, 3),
        "unbalanced_transfer_ids": core.validate_journal(path),
    }
