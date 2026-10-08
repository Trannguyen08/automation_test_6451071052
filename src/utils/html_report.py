from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path


VIETNAM_TIMEZONE = timezone(timedelta(hours=7))


def write_html_report(results, elapsed_seconds, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = len(results)
    passed = sum(result["outcome"] == "passed" for result in results)
    failed = sum(result["outcome"] == "failed" for result in results)
    skipped = sum(result["outcome"] == "skipped" for result in results)
    pass_rate = (passed / total * 100) if total else 0.0
    generated_at = datetime.now(VIETNAM_TIMEZONE).strftime("%d/%m/%Y %H:%M:%S UTC+7")

    rows = "".join(_result_row(result) for result in results)
    if not rows:
        rows = '<tr><td colspan="4" class="empty">Không có test case được chạy.</td></tr>'

    document = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Automation Test Report</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; }}
    body {{ margin: 0; background: #f4f7fb; color: #172033; }}
    main {{ max-width: 1050px; margin: 32px auto; padding: 0 20px; }}
    h1 {{ margin-bottom: 6px; }}
    .meta {{ color: #64748b; margin-top: 0; }}
    .cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 24px 0; }}
    .card, .panel {{ background: white; border-radius: 12px; padding: 18px; box-shadow: 0 3px 16px #1e293b12; }}
    .value {{ display: block; margin-top: 8px; font-size: 28px; font-weight: 700; }}
    .pass {{ color: #16803d; }} .fail {{ color: #c1262d; }} .skip {{ color: #a16207; }}
    .progress {{ height: 16px; overflow: hidden; background: #e2e8f0; border-radius: 999px; }}
    .progress > div {{ width: {pass_rate:.2f}%; height: 100%; background: #22a559; }}
    table {{ width: 100%; margin-top: 18px; border-collapse: collapse; }}
    th, td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: left; vertical-align: top; }}
    th {{ background: #eef3f8; }}
    .status {{ font-weight: 700; }}
    details pre {{ white-space: pre-wrap; max-width: 700px; color: #991b1b; }}
    .empty {{ text-align: center; color: #64748b; }}
    @media (max-width: 720px) {{ .cards {{ grid-template-columns: repeat(2, 1fr); }} }}
  </style>
</head>
<body>
<main>
  <h1>Báo cáo Automation Test</h1>
  <p class="meta">Tạo lúc {generated_at} · Thời gian chạy {elapsed_seconds:.2f} giây</p>

  <section class="cards">
    <div class="card">Tổng số test<span class="value">{total}</span></div>
    <div class="card">Pass<span class="value pass">{passed}</span></div>
    <div class="card">Fail<span class="value fail">{failed}</span></div>
    <div class="card">Skip<span class="value skip">{skipped}</span></div>
  </section>

  <section class="panel">
    <h2>Tỷ lệ pass: {pass_rate:.2f}%</h2>
    <div class="progress" aria-label="Tỷ lệ pass {pass_rate:.2f}%"><div></div></div>
  </section>

  <section class="panel" style="margin-top: 18px">
    <h2>Chi tiết test case</h2>
    <table>
      <thead><tr><th>Test case</th><th>Kết quả</th><th>Thời gian</th><th>Thông tin</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </section>
</main>
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")
    return {
        "path": output_path.resolve(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "pass_rate": pass_rate,
    }


def _result_row(result):
    outcome = result["outcome"]
    labels = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP"}
    message = str(result.get("message", "")).strip()
    details = ""
    if message:
        details = f"<details><summary>Xem chi tiết</summary><pre>{escape(message)}</pre></details>"

    return (
        "<tr>"
        f"<td>{escape(result['nodeid'])}</td>"
        f'<td class="status {outcome}">{labels[outcome]}</td>'
        f"<td>{result['duration']:.2f}s</td>"
        f"<td>{details}</td>"
        "</tr>"
    )

