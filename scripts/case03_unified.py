"""Build CASE 003 unified, offline dashboard using benchmark output."""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
from scripts.case03_benchmark import benchmark

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "visuals" / "case-03" / "dashboard.html"

def build_dashboard(report: dict, template: str) -> str:
    if 'id="panel-qa"' not in template or 'role="tablist"' not in template:
        raise ValueError("Expected CASE 003 tab layout is missing")
    metric = report["metrics"]
    count = report["cases"]
    observations = report["observations_by_type"]
    alerts = report["alerts_by_rule"]
    def e(value):
        return html.escape(str(value), quote=True)
    def bar(label, value, maximum):
        percentage = round(value * 100 / max(maximum, 1), 2)
        return (f'<div class="event"><div style="display:flex;justify-content:space-between;gap:12px">'
                f'<span>{e(label)}</span><b>{value}</b></div>'
                f'<div style="margin-top:7px;height:10px;border-radius:9px;background:#34363c;overflow:hidden">'
                f'<div style="width:{percentage}%;background:#c8ad85;height:100%"></div></div></div>')
    observation_bars = "".join(bar(k, v, max(observations.values())) for k,v in observations.items())
    alert_bars = "".join(bar(k, v, max(alerts.values()) if alerts else 1) for k,v in sorted(alerts.items()))
    items = []
    # Reviewer workbench is artificial and intentionally contains only event categories and case IDs.
    for i in range(min(count, 40)):
        case_id = f"FIC-{i+1:05d}"
        positive = i % 4 == 0
        signal = "На проверку" if positive else "Рутинный контроль"
        kinds = ("cash_exception, credit_posted, merchant_dispute, mandate_invalid"
                 if positive else "benign_purchase")
        items.append({"id":case_id,"status":signal,"events":kinds})
    payload = json.dumps(items, ensure_ascii=False).replace("<", "\\u003c")
    review = "".join(
        f'<div class="event" data-review-item="{e(x["id"])}" data-review-status="{e(x["status"])}">'
        f'<b>{e(x["id"])}</b> · {e(x["status"])}<div class="meta">{e(x["events"])}</div></div>'
        for x in items)
    finance = (
        '<p>Исходный номинал в описании: <b>$6 000 000</b>. '
        'Фактическая сумма внесения и установленный ущерб: <b>не определены</b>. '
        'Плановый номинал не является реальным балансом или результатом операций.</p>'
        '<div class="warning">Финансовая сверка: заявленный номинал ≠ принято банком ≠ '
        'учтённые средства ≠ платёж ≠ подтверждённый убыток.</div>')
    panel = f'''<section role="tabpanel" id="panel-data" aria-labelledby="tab-data" hidden>
    <div class="grid">
    <article class="card full"><h2>Аналитика и результаты детектора</h2>
    <div class="kpis"><div class="kpi"><span class="label">Инциденты</span><strong>{count}</strong></div>
    <div class="kpi"><span class="label">Precision</span><strong>{metric["precision"]:.1%}</strong></div>
    <div class="kpi"><span class="label">Recall</span><strong>{metric["recall"]:.1%}</strong></div>
    <div class="kpi"><span class="label">FPR</span><strong>{metric["false_positive_rate"]:.1%}</strong></div></div>
    <p class="small">Seed: {report["seed"]}; всего наблюдений: {report["observations_total"]}.
    Матрица: TP {metric["tp"]} · FP {metric["fp"]} · FN {metric["fn"]} · TN {metric["tn"]}.</p>
    </article>
    <article class="card"><h2>Профиль событий</h2>{observation_bars}</article>
    <article class="card"><h2>Срабатывания правил</h2>{alert_bars}</article>
    <article class="card full"><h2>Финансовая сверка</h2>{finance}</article>
    <article class="card full"><h2>Рабочее место аналитика</h2><p>
    Выберите категорию, затем исследуйте связанные журнальные признаки. Только тестовые записи.</p>
    <label for="review-filter">Фильтр:</label>
    <select id="review-filter" style="margin:0 0 14px 10px;background:#262931;color:white;padding:8px">
    <option value="all">Все</option><option value="На проверку">На проверку</option>
    <option value="Рутинный контроль">Рутинный контроль</option></select>
    <div id="review-count" class="small" aria-live="polite"></div>
    <div id="review-items" style="max-height:350px;overflow:auto">{review}</div></article>
    </div></section>'''
    button = ('<button role="tab" id="tab-data" data-tab="data" aria-selected="false" '
              'aria-controls="panel-data">06 · Аналитика</button>')
    # Existing case tabs, evidence panels and static demo remain intact.
    template = template.replace('</nav>', button + '</nav>', 1)
    template = template.replace('<footer>', panel + '<footer>', 1)
    script = """<script>
    (function(){
      const filter=document.getElementById('review-filter');
      if(!filter)return;
      function update(){
        let visible=0;
        document.querySelectorAll('[data-review-item]').forEach(function(item){
          const show=filter.value==='all'||item.dataset.reviewStatus===filter.value;
          item.hidden=!show;
          if(show)visible++;
        });
        document.getElementById('review-count').textContent='Записей в выборке: '+visible;
      }
      filter.addEventListener('change',update);update();
    })();
    </script>"""
    return template.replace('</body>', script + '</body>', 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases",type=int,default=200)
    parser.add_argument("--seed",type=int,default=3003)
    parser.add_argument("--output",default="case03_unified.html")
    args=parser.parse_args()
    report=benchmark(args.seed,args.cases)
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(build_dashboard(report,TEMPLATE.read_text(encoding="utf-8")),encoding="utf-8")
    print(f"Generated {output}; cases={report['cases']}; seed={report['seed']}")

if __name__=="__main__":
    main()
