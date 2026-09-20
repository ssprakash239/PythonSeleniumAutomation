"""Self-contained HTML Extent-style test report generator (no external report libraries required)."""
import html
import os
from datetime import datetime

STATUS_COLORS = {
    "passed": "#2e7d32",
    "failed": "#c62828",
    "skipped": "#f9a825",
}


def _format_duration(total_seconds: float) -> str:
    minutes, seconds = divmod(int(total_seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def _build_donut_style(passed: int, failed: int, skipped: int) -> str:
    total = passed + failed + skipped
    if total == 0:
        return "background: #e0e0e0;"
    pass_end = passed / total * 100
    fail_end = pass_end + (failed / total * 100)
    return (
        f"background: conic-gradient("
        f"{STATUS_COLORS['passed']} 0% {pass_end:.2f}%, "
        f"{STATUS_COLORS['failed']} {pass_end:.2f}% {fail_end:.2f}%, "
        f"{STATUS_COLORS['skipped']} {fail_end:.2f}% 100%);"
    )


def _build_step_rows(steps: list) -> str:
    if not steps:
        return "<tr><td colspan=\"3\">No step details captured.</td></tr>"
    rows = []
    for step in steps:
        status = step["status"].lower()
        message = step.get("message") or ""
        message = message.splitlines()[-1] if message else "-"
        rows.append(
            f"""
            <tr>
                <td><span class="step-keyword">{html.escape(step['keyword'])}</span> {html.escape(step['name'])}</td>
                <td><span class="badge badge-{status}">{html.escape(step['status'])}</span></td>
                <td>{step['duration']:.2f}s</td>
                <td class="message">{html.escape(message)}</td>
            </tr>"""
        )
        screenshot = step.get("screenshot")
        if status == "failed" and screenshot:
            rows.append(
                f"""
            <tr>
                <td colspan="4" class="screenshot-cell">
                    <a href="data:image/png;base64,{screenshot}" target="_blank" rel="noopener">
                        <img class="screenshot-thumb" src="data:image/png;base64,{screenshot}" alt="Failure screenshot" />
                    </a>
                </td>
            </tr>"""
            )
    return "".join(rows)


def _build_test_cards(test_results: list) -> str:
    if not test_results:
        return "<p class=\"empty\">No tests were executed.</p>"
    cards = []
    for i, result in enumerate(test_results, start=1):
        status = result["status"].lower()
        message = result.get("message") or ""
        message = message.splitlines()[-1] if message else ""
        step_rows = _build_step_rows(result.get("steps", []))
        open_attr = " open" if status == "failed" else ""
        cards.append(
            f"""
            <details class="test-card"{open_attr}>
                <summary>
                    <span class="test-index">#{i}</span>
                    <span class="test-name">{html.escape(result['name'])}</span>
                    <span class="badge badge-{status}">{html.escape(result['status'])}</span>
                    <span class="test-duration">{result['duration']:.2f}s</span>
                </summary>
                {f'<div class="message top-message">{html.escape(message)}</div>' if message else ''}
                <table>
                    <thead>
                        <tr><th>Step</th><th>Status</th><th>Duration</th><th>Error</th></tr>
                    </thead>
                    <tbody>{step_rows}</tbody>
                </table>
            </details>"""
        )
    return "".join(cards)


def generate_extent_report(test_results: list, browser_name: str, start_time: datetime,
                            end_time: datetime, output_dir: str = "reports/extent-reports") -> str:
    """Build the HTML report and write it to disk, returning the report file path."""
    os.makedirs(output_dir, exist_ok=True)

    total = len(test_results)
    passed = sum(1 for t in test_results if t["status"] == "Passed")
    failed = sum(1 for t in test_results if t["status"] == "Failed")
    skipped = sum(1 for t in test_results if t["status"] == "Skipped")
    duration_str = _format_duration((end_time - start_time).total_seconds())
    donut_style = _build_donut_style(passed, failed, skipped)
    test_cards_html = _build_test_cards(test_results)
    browser_label = html.escape(browser_name.strip().capitalize() or "Unknown")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Extent Report - {browser_label} - {end_time.strftime('%d-%b-%Y %H:%M')}</title>
<style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f8; margin: 0; color: #263238; }}
    .header {{ background: #1a237e; color: #fff; padding: 24px 32px; }}
    .header h1 {{ margin: 0 0 8px 0; font-size: 24px; }}
    .header .meta {{ font-size: 14px; opacity: 0.9; }}
    .container {{ padding: 24px 32px; }}
    .summary {{ display: flex; align-items: center; gap: 32px; background: #fff; border-radius: 8px;
                padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-bottom: 24px; flex-wrap: wrap; }}
    .donut {{ width: 150px; height: 150px; border-radius: 50%; {donut_style} display: flex;
              align-items: center; justify-content: center; flex-shrink: 0; }}
    .donut-hole {{ width: 100px; height: 100px; border-radius: 50%; background: #fff; display: flex;
                   flex-direction: column; align-items: center; justify-content: center; }}
    .donut-hole .total-num {{ font-size: 26px; font-weight: bold; }}
    .donut-hole .total-label {{ font-size: 12px; color: #607d8b; }}
    .tiles {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .tile {{ min-width: 110px; padding: 14px 18px; border-radius: 6px; color: #fff; text-align: center; }}
    .tile .num {{ font-size: 24px; font-weight: bold; display: block; }}
    .tile.total {{ background: #37474f; }}
    .tile.passed {{ background: {STATUS_COLORS['passed']}; }}
    .tile.failed {{ background: {STATUS_COLORS['failed']}; }}
    .tile.skipped {{ background: {STATUS_COLORS['skipped']}; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; }}
    th, td {{ padding: 10px 16px; text-align: left; border-bottom: 1px solid #eceff1; font-size: 13px; }}
    th {{ background: #eceff1; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
    .message {{ color: #c62828; font-family: Consolas, monospace; font-size: 12px; }}
    .badge {{ padding: 4px 10px; border-radius: 12px; color: #fff; font-size: 12px; white-space: nowrap; }}
    .badge-passed {{ background: {STATUS_COLORS['passed']}; }}
    .badge-failed {{ background: {STATUS_COLORS['failed']}; }}
    .badge-skipped {{ background: {STATUS_COLORS['skipped']}; }}
    .screenshot-cell {{ background: #fafafa; text-align: center; padding: 12px; }}
    .screenshot-thumb {{ max-width: 320px; max-height: 220px; border: 1px solid #cfd8dc; border-radius: 4px; }}
    .step-keyword {{ font-weight: 700; color: #1a237e; }}
    .test-card {{ background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-bottom: 16px;
                  padding: 0 20px 12px 20px; }}
    .test-card summary {{ list-style: none; cursor: pointer; padding: 16px 0; display: flex; align-items: center;
                          gap: 14px; font-size: 15px; }}
    .test-card summary::-webkit-details-marker {{ display: none; }}
    .test-card summary::before {{ content: '\\25B8'; color: #607d8b; }}
    .test-card[open] summary::before {{ content: '\\25BE'; }}
    .test-index {{ color: #90a4ae; font-weight: bold; }}
    .test-name {{ flex: 1; font-weight: 600; }}
    .test-duration {{ color: #607d8b; font-size: 13px; }}
    .top-message {{ margin-bottom: 12px; }}
    .empty {{ text-align: center; color: #607d8b; padding: 32px; }}
</style>
</head>
<body>
    <div class="header">
        <h1>OnniProject AM25R1 Automation - Extent Report</h1>
        <div class="meta">
            Browser: {browser_label} &nbsp;|&nbsp;
            Execution Start: {start_time.strftime('%d-%b-%Y %H:%M:%S')} &nbsp;|&nbsp;
            Execution End: {end_time.strftime('%d-%b-%Y %H:%M:%S')} &nbsp;|&nbsp;
            Total Duration: {duration_str}
        </div>
    </div>
    <div class="container">
        <div class="summary">
            <div class="donut"><div class="donut-hole">
                <span class="total-num">{total}</span>
                <span class="total-label">Total</span>
            </div></div>
            <div class="tiles">
                <div class="tile total"><span class="num">{total}</span>Total</div>
                <div class="tile passed"><span class="num">{passed}</span>Passed</div>
                <div class="tile failed"><span class="num">{failed}</span>Failed</div>
                <div class="tile skipped"><span class="num">{skipped}</span>Skipped</div>
            </div>
        </div>
        {test_cards_html}
    </div>
</body>
</html>"""

    timestamp = end_time.strftime("%Y%m%d_%H%M")
    filename = f"{browser_name.strip().capitalize() or 'Unknown'}_ExtentReport_{timestamp}.html"
    report_path = os.path.join(output_dir, filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return report_path
