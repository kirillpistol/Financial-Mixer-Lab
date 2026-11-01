# CASE 003 — Offline QA monitoring demo

Run:

```bash
python -m pytest -q tests/test_case03_monitor.py
python -c "import json; from app.case03_monitor import demo; print(json.dumps(demo(), indent=2))"
```

Open `visuals/case-03/dashboard.html` directly in a browser for an interactive **illustrative** dashboard. The chart uses deterministic fictional data mirroring the Python demo; it does not connect to the API.

## Evidence model

`Observation(case_id, minute, kind, reference, verified=True)` uses artificial IDs and arbitrary fictional observation minutes. The detector checks combinations of independently verified audit events, not actual card-network or banking activity.

The demo includes one labelled positive, one benign case and one case with a complaint but a cash/credit exception. The latter deliberately yields a false positive for demonstration. Expected case-level precision 0.5, recall 1.0, FPR 0.5 on only three artificial cases; **not a real performance claim**.

The labels, time positions and linked events are synthetic. No operational thresholds, real payment gateways, SMS delivery, personal information, deposit instructions or subscription automation are included.
