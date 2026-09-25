import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from backend.config import settings

app = FastAPI(
    title="Policy-to-Code Mapper API",
    description="Context-aware IDE backend for real-time security policy guidance.",
    version="0.1.0",
)

DATA_DIR = Path(__file__).parent / "data"


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "policy-to-code-mapper"}


@app.get("/mock-analysis")
def get_mock_analysis() -> dict:
    mock_file = DATA_DIR / "mock_findings.json"
    if not mock_file.exists():
        return {"error": "Mock findings file not found"}
    with open(mock_file, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/mock-guidance", response_class=HTMLResponse)
def get_mock_guidance_card() -> str:
    mock_file = DATA_DIR / "mock_findings.json"
    if not mock_file.exists():
        return "<h1>Error: Mock findings not found</h1>"

    with open(mock_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    finding = data["findings"][0]
    code_evidence = finding["code_evidence"]
    policy = finding["policy_reference"]
    reg = finding["supporting_regulatory_context"][0]
    trace = finding["traceability"]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Policy-to-Code Guidance Card</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 24px;
            margin: 0;
        }}
        .card {{
            background-color: #252526;
            border: 1px solid #3c3c3c;
            border-left: 5px solid #e5a50a;
            border-radius: 6px;
            max-width: 680px;
            margin: 0 auto;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #3c3c3c;
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .badge {{
            background-color: #388e3c;
            color: #ffffff;
            font-size: 11px;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 12px;
            text-transform: uppercase;
        }}
        .title {{
            font-size: 18px;
            font-weight: 600;
            color: #f1f1f1;
            margin: 0;
        }}
        .section-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #858585;
            font-weight: bold;
            margin-top: 14px;
            margin-bottom: 4px;
        }}
        .content-box {{
            background-color: #1e1e1e;
            padding: 10px 12px;
            border-radius: 4px;
            font-size: 13px;
            line-height: 1.5;
            color: #cccccc;
        }}
        code {{
            font-family: 'Consolas', 'Courier New', monospace;
            background-color: #2d2d2d;
            color: #ce9178;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        pre {{
            font-family: 'Consolas', 'Courier New', monospace;
            background-color: #1e1e1e;
            color: #dcdcaa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 4px 0;
            border: 1px solid #333;
        }}
        .traceability {{
            background-color: #1b2838;
            border: 1px solid #1769aa;
            border-radius: 4px;
            padding: 10px 12px;
            font-size: 12px;
            color: #9cdcfe;
        }}
        .disclaimer {{
            font-size: 11px;
            color: #808080;
            margin-top: 18px;
            font-style: italic;
            border-top: 1px dashed #3c3c3c;
            padding-top: 10px;
        }}
        .actions {{
            margin-top: 16px;
            display: flex;
            gap: 10px;
        }}
        .btn {{
            background-color: #0e639c;
            color: #ffffff;
            border: none;
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 3px;
            cursor: pointer;
        }}
        .btn-secondary {{
            background-color: #3c3c3c;
            color: #cccccc;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1 class="title">Policy-to-Code Guidance</h1>
            <span class="badge">Advisory</span>
        </div>

        <div class="section-label">Observed Code Evidence</div>
        <pre>{code_evidence['snippet']}</pre>

        <div class="section-label">Potential Policy Consideration</div>
        <div class="content-box">{finding['potential_policy_consideration']}</div>

        <div class="section-label">Relevant Organizational Policy</div>
        <div class="content-box">
            <strong>{policy['id']} — {policy['title']}</strong> ({policy['category']})
        </div>

        <div class="section-label">Why This Matters</div>
        <div class="content-box">{finding['why_this_matters']}</div>

        <div class="section-label">Supporting Regulatory Context</div>
        <div class="content-box">
            <strong>{reg['framework']} {reg['article']}</strong> — {reg['title']} <em>({reg['relationship']})</em>
        </div>

        <div class="section-label">Suggested Developer Action</div>
        <div class="content-box">{finding['recommended_action']}</div>

        <div class="section-label">Safer Example</div>
        <pre>{finding['safer_example']}</pre>

        <div class="section-label">Traceability Chain</div>
        <div class="traceability">
            Source Code ➔ <code>{trace['code_to_pattern']}</code><br>
            Policy Rule ➔ <code>{trace['pattern_to_policy']}</code><br>
            Regulatory Context ➔ <code>{trace['policy_to_context']}</code>
        </div>

        <div class="actions">
            <button class="btn">View Policy</button>
            <button class="btn btn-secondary">Show Safer Example</button>
            <button class="btn btn-secondary">Dismiss</button>
        </div>

        <div class="disclaimer">
            {finding['disclaimer']}
        </div>
    </div>
</body>
</html>
"""
    return html_content


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
