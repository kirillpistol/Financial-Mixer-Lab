from pathlib import Path
from scripts.case03_unified import build_dashboard, TEMPLATE
from scripts.case03_benchmark import benchmark

def test_unified_dashboard_has_all_tabs_and_computed_metrics():
    result=benchmark(3003,200)
    html=build_dashboard(result,TEMPLATE.read_text(encoding="utf-8"))
    assert 'id="panel-prep"' in html
    assert 'id="panel-data"' in html
    assert 'id="tab-data"' in html
    assert f"{result['metrics']['precision']:.1%}" in html
    assert 'FIC-00001' in html
    assert 'Финансовая сверка' in html
    assert 'https://' not in html

def test_unified_dashboard_reproducible():
    template=TEMPLATE.read_text(encoding="utf-8")
    assert build_dashboard(benchmark(3003,50),template)==build_dashboard(benchmark(3003,50),template)
