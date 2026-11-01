from scripts.case03_benchmark import benchmark

def test_reproducible():
    assert benchmark(3003, 200) == benchmark(3003, 200)

def test_all_case_counts():
    r = benchmark()
    assert r["cases"] == 200
    assert r["synthetic_positive_labels"] == 50
    assert r["synthetic_negative_labels"] == 150
    assert sum(r["observations_by_type"].values()) == r["observations_total"]

def test_face_value_not_deposit():
    r = benchmark()
    assert r["planned_face_value_usd_context_only"] == 6000000
    assert r["actual_deposit_amount_usd"] is None
    assert r["actual_loss_usd"] is None

def test_metrics_confusion_matrix():
    r = benchmark()
    m = r["metrics"]
    assert m["tp"] + m["fn"] == 50
    assert m["fp"] + m["tn"] == 150
    assert 0 <= m["precision"] <= 1
