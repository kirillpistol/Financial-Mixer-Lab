import pytest
from app.workload_profiles import get_profile, list_profiles

def test_profiles_are_selectable():
    assert get_profile("retail").min_amount == 1
    assert {p["name"] for p in list_profiles()} == {"retail", "corporate", "stress"}

def test_unknown_profile_rejected():
    with pytest.raises(ValueError):
        get_profile("external-bank")
