"""Deterministic dual-station offline batch capacity model.

This model never provisions live accounts, buys numbers or calls third-party services.
"""
from dataclasses import dataclass, asdict
from math import ceil

@dataclass(frozen=True)
class Station:
    name: str
    capacity_per_hour: int
    failure_rate: float

def simulate_batch(total: int=5000, hours: float=24, station_a: Station|None=None,
                   station_b: Station|None=None) -> dict:
    if type(total) is not int or not 0 <= total <= 100_000:
        raise ValueError("total out of range")
    if not 0 < hours <= 720:
        raise ValueError("hours out of range")
    a = station_a or Station("Профиль", 240, .12)
    b = station_b or Station("Учёт", 220, .14)
    for s in (a,b):
        if type(s.capacity_per_hour) is not int or not 1 <= s.capacity_per_hour <= 10000:
            raise ValueError("station rate out of range")
        if not 0 <= s.failure_rate <= 1:
            raise ValueError("failure_rate out of range")
    # Each artificial record must pass both steps, so throughput is bottleneck-limited.
    cap_a = int(a.capacity_per_hour * hours)
    cap_b = int(b.capacity_per_hour * hours)
    processed = min(total, cap_a, cap_b)
    # Expected values, not observed accounts. No random third-party actions.
    pass_a = processed * (1-a.failure_rate)
    pass_b = pass_a * (1-b.failure_rate)
    return {
        "mode":"offline_synthetic", "requested":total, "hours":hours,
        "stations":[asdict(a),asdict(b)], "bottleneck_per_hour":min(a.capacity_per_hour,b.capacity_per_hour),
        "processed":processed, "remaining":total-processed,
        "expected_stage_a_success":round(pass_a,2),
        "expected_both_success":round(pass_b,2),
        "expected_combined_loss":round(processed-pass_b,2),
        "capacity_utilization_percent":round(100*processed/min(cap_a,cap_b),2) if min(cap_a,cap_b) else 0
    }
