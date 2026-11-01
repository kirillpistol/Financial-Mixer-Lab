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

## Reproducible 200-case benchmark and HTML statistics

From the repository root, run:

```powershell
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
python -m scripts.case03_benchmark --seed 3003 --cases 200 --output case03_benchmark.json
python -m scripts.case03_report --seed 3003 --cases 200 --output case03_report.html
start .\case03_report.html
```

- **$6,000,000** is the narrator's **planned face-value context**, **not** a claim about processed cash, funds deposited, settlement or losses. All actual volumes remain unspecified.
- The 200 cases and 25% positive-labelled share are deliberately chosen QA inputs, **not empirical estimates**. All observations are created offline by a seeded generator. Positives are labelled by design to test detector behavior; the detector's alerts are not proof of fraud.
- JSON includes counts by observation type, alert totals, a confusion matrix, precision, recall, and false-positive rate. HTML is a self-contained visualization built from the same computed report.
- Run with `--cases 1000` to test larger synthetic datasets (permitted range: 20–5000). No monetary transactions, card operations, SMS or external APIs are exercised.

## Unified CASE 003 dashboard

Generate the dashboard from the current Python detector and benchmark:

```powershell
git pull origin main
python -m pytest -q
python -m scripts.case03_unified --seed 3003 --cases 200 --output case03_unified.html
start .\case03_unified.html
```

The output keeps the existing technical tabs and adds **06 · Аналитика** with computed metrics, event counts, rule activations, reconciliation definitions, and a filterable 40-record investigation sample. It runs locally in a browser without CDN dependencies, live payment rails, real bank accounts, SMS delivery, or API access.

The actual amounts deposited and any proven loss remain unknown. The $6 million figure is narrative face-value context only and does not generate any money or simulate successful fraud. Indicators are computed from synthetic QA events and are not calibrated detection rates from a bank.
