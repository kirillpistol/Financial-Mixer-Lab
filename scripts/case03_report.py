"""Render a standalone offline HTML report from CASE 003 synthetic benchmark."""
from __future__ import annotations
import argparse
import html
from pathlib import Path
from scripts.case03_benchmark import benchmark

def render_report(report: dict) -> str:
    def esc(value):
        return html.escape(str(value))
    rows = report["observations_by_type"]
    alerts = report["alerts_by_rule"]
    metrics = report["metrics"]
    mx = max(rows.values(), default=1) or 1
    bars = "".join(
        f'<div class="barrow"><span>{esc(name)}</span><div class="track">'
        f'<div class="fill" style="width:{100*value/mx:.1f}%"></div></div>'
        f'<b>{value}</b></div>' for name, value in rows.items()
    )
    rule_rows = "".join(f"<tr><td>{esc(k)}</td><td>{v}</td></tr>"
                        for k, v in sorted(alerts.items()))
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Кейс 3 — Синтетическая статистика</title>
<style>:root{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#101114;color:#eee}}
*{{box-sizing:border-box}}body{{margin:0}}main{{max-width:1080px;margin:auto;padding:32px 20px}}
h1{{font-size:52px;letter-spacing:-.06em}}h2{{font-size:19px}}p,.muted{{color:#b1b5be;line-height:1.6}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.card{{background:#1d1f25;border:1px solid #393b44;border-radius:13px;padding:20px}}
.card b{{display:block;font-size:29px;margin:8px 0}}section{{margin:22px 0}}.barrow{{display:grid;grid-template-columns:175px 1fr 45px;align-items:center;gap:12px;margin:13px 0;font-size:13px}}
.track{{background:#34363c;height:15px;border-radius:8px;overflow:hidden}}.fill{{background:#d4b88e;height:100%}}table{{width:100%;border-collapse:collapse}}td,th{{padding:12px;text-align:left;border-bottom:1px solid #393b44}}.warn{{border-left:3px solid #d4b88e;padding:14px;background:#28272a}}
@media(max-width:690px){{.grid{{grid-template-columns:repeat(2,1fr)}}.barrow{{grid-template-columns:115px 1fr 35px}}h1{{font-size:40px}}}}
</style></head><body><main><div class="muted">PISTOL / FINANCIAL MIXER LAB · OFFLINE QA</div>
<h1>Кейс 3</h1><p>Воспроизводимый набор искусственных событий для оценки защитного мониторинга. Seed: {report["seed"]}; записей: {report["observations_total"]}.</p>
<div class="grid"><div class="card">Кейсы<b>{report["cases"]}</b></div>
<div class="card">Precision<b>{metrics["precision"]:.1%}</b></div>
<div class="card">Recall<b>{metrics["recall"]:.1%}</b></div>
<div class="card">FPR<b>{metrics["false_positive_rate"]:.1%}</b></div></div>
<section class="card"><h2>Категории наблюдений</h2>{bars}</section>
<section class="card"><h2>Срабатывания правил</h2><table><tr><th>Правило</th><th>Количество</th></tr>{rule_rows}</table></section>
<section class="card"><h2>Матрица ошибок</h2><div class="grid"><div class="card">TP<b>{metrics["tp"]}</b></div>
<div class="card">FP<b>{metrics["fp"]}</b></div>
<div class="card">FN<b>{metrics["fn"]}</b></div>
<div class="card">TN<b>{metrics["tn"]}</b></div></div></section>
<section class="card"><h2>Контекст кейса</h2><p>Исходный заявленный номинал банкнот: $6 000 000. Эта величина не используется при генерации платежей или расчёте эффективности детектора. Фактически внесённая сумма и ущерб неизвестны.</p></section>
<div class="warn">Все пропорции, события, метки и результаты полностью синтетические и не являются оценкой реального мошенничества или эффективности банковского мониторинга. Нет реальных счетов, карт, SMS или платежей.</div>
</main></body></html>"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=200)
    parser.add_argument("--seed", type=int, default=3003)
    parser.add_argument("--output", default="case03_report.html")
    args = parser.parse_args()
    report = benchmark(args.seed, args.cases)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(report), encoding="utf-8")
    print(f"Generated {path} with {report['cases']} fictional cases")

if __name__ == "__main__":
    main()
