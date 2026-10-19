"""Declarative offline workload profiles; no dynamic imports or external requests."""
from dataclasses import dataclass

@dataclass(frozen=True)
class WorkloadProfile:
    name: str
    description: str
    min_amount: int
    max_amount: int
    account_pool_size: int

PROFILES = {
    "retail": WorkloadProfile("retail", "Small synthetic retail payments", 1, 100, 20),
    "corporate": WorkloadProfile("corporate", "Synthetic corporate ledger workload", 100, 1000, 10),
    "stress": WorkloadProfile("stress", "Local throughput measurement", 1, 100, 100),
}

def get_profile(name: str) -> WorkloadProfile:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError("Unknown profile; use retail, corporate or stress") from exc

def list_profiles() -> list[dict]:
    return [vars(profile).copy() for profile in PROFILES.values()]
