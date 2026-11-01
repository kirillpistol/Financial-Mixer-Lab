from scripts.case03_benchmark import benchmark
from scripts.case03_report import render_report

def test_report_is_self_contained():
    html = render_report(benchmark())
    assert "<html" in html
    assert "Кейс 3" in html
    assert "cash_exception" in html
    assert "6000000" not in html.replace("6 000 000", "")
    assert "http://" not in html and "https://" not in html
