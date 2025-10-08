import requests
from dotenv import load_dotenv
import os
import json
import time

REPO = "IanEAbba/IanETrading"
load_dotenv('.env')
TOKEN = os.getenv("GitHub_Token")
PROJECT_ID = "PVT_kwHODGb1Hs4BE0pE"
if not TOKEN:
    raise ValueError("❌ Missing GitHub_Token in .env")

headers_rest = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

headers_graphql = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


sprint_items = [
    # 🧩 DataFetcher
    {
        "title": "DataFetcher – Create class skeleton",
        "body": "Create `DataFetcher` class with constructor and method stubs.",
        "labels": ["sprint-1", "data", "feature"]
    },
    {
        "title": "DataFetcher – Implement fetch()",
        "body": "Implement `fetch(symbols, timeframe, limit)` using `alpaca_client.get_bars()` to retrieve OHLCV data.",
        "labels": ["sprint-1", "data", "feature"]
    },
    {
        "title": "DataFetcher – Add retry logic",
        "body": "Add retry and error handling for API rate limits and network failures.",
        "labels": ["sprint-1", "data", "resilience"]
    },
    {
        "title": "DataFetcher – Add caching/export",
        "body": "Implement caching and CSV export to `data/latest_<date>.csv` for fetched results.",
        "labels": ["sprint-1", "data", "storage"]
    },
    {
        "title": "DataFetcher – Unit test",
        "body": "Fetch 3 tickers and confirm DataFrame contains required columns (`open`, `high`, `low`, `close`, `volume`).",
        "labels": ["sprint-1", "data", "test"]
    },

    # 📈 SignalManager
    {
        "title": "SignalManager – Create class skeleton",
        "body": "Create `SignalManager` class with method stubs `detect_overbuy()` and `generate_signal()`.",
        "labels": ["sprint-1", "signals", "feature"]
    },
    {
        "title": "SignalManager – Move check_momentum() logic",
        "body": "Move `check_momentum()` from `strategy.py` into `SignalManager` class.",
        "labels": ["sprint-1", "signals", "refactor"]
    },
    {
        "title": "SignalManager – Add config support",
        "body": "Load configurable thresholds (price, volume) from `config.yaml` or environment variables.",
        "labels": ["sprint-1", "signals", "config"]
    },
    {
        "title": "SignalManager – Add structured logging",
        "body": "Replace print statements with structured JSON/CSV logs saved to `logs/signals.log`.",
        "labels": ["sprint-1", "signals", "logging"]
    },
    {
        "title": "SignalManager – Return signal list",
        "body": "Return signals as list of `{symbol, action, strength}` dictionaries for downstream use.",
        "labels": ["sprint-1", "signals", "feature"]
    },
    {
        "title": "SignalManager – Unit test",
        "body": "Use mock DataFrame to test detection logic and threshold edge cases.",
        "labels": ["sprint-1", "signals", "test"]
    },

    # 💸 TradeExecutor
    {
        "title": "TradeExecutor – Create class skeleton",
        "body": "Define `TradeExecutor` class with method stubs for `execute_order()` and `verify_order()`.",
        "labels": ["sprint-1", "trading", "feature"]
    },
    {
        "title": "TradeExecutor – Integrate submit_order()",
        "body": "Use Alpaca client `submit_order()` to place buy/sell orders.",
        "labels": ["sprint-1", "trading", "integration"]
    },
    {
        "title": "TradeExecutor – Add dry-run flag",
        "body": "Implement dry-run mode that logs simulated orders without calling API.",
        "labels": ["sprint-1", "trading", "safety"]
    },
    {
        "title": "TradeExecutor – Add logging",
        "body": "Record all executed orders to `logs/trades.csv` including timestamp, symbol, qty, and side.",
        "labels": ["sprint-1", "trading", "logging"]
    },
    {
        "title": "TradeExecutor – Error handling",
        "body": "Catch API and balance errors, log gracefully without crash.",
        "labels": ["sprint-1", "trading", "error"]
    },
    {
        "title": "TradeExecutor – Paper trade verification",
        "body": "Submit a 1-share paper order and verify success response.",
        "labels": ["sprint-1", "trading", "test"]
    },

    # ⚙️ GitHub Actions / Automation
    {
        "title": "Workflow – Move app.py to src/main.py",
        "body": "Refactor entry point to import modules (`DataFetcher`, `SignalManager`, `TradeExecutor`) instead of inline logic.",
        "labels": ["sprint-1", "automation", "ci-cd"]
    },
    {
        "title": "Workflow – Create daily.yml",
        "body": "Create `.github/workflows/daily.yml` with cron and manual dispatch to run `python src/main.py`.",
        "labels": ["sprint-1", "automation", "ci-cd"]
    },
    {
        "title": "Workflow – Add Secrets",
        "body": "Add `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`, `APCA_API_BASE_URL`, and `GITHUB_TOKEN` to repository secrets.",
        "labels": ["sprint-1", "automation", "security"]
    },
    {
        "title": "Workflow – Test manual dispatch",
        "body": "Trigger workflow manually (`workflow_dispatch`) and verify full run completes without error.",
        "labels": ["sprint-1", "automation", "test"]
    }
]


# === Helper: Create issue ===
def create_issue(title, body, labels):
    url = f"https://api.github.com/repos/{REPO}/issues"
    data = {"title": title, "body": body, "labels": labels}
    res = requests.post(url, headers=headers_rest, json=data)
    if res.status_code == 201:
        issue = res.json()
        print(f"✅ Created issue: {issue['title']} (#{issue['number']})")
        return issue["node_id"]  # needed for GraphQL link
    else:
        print(f"❌ Failed to create issue ({res.status_code}): {res.text}")
        return None

# === Helper: Link issue to project board ===
def add_issue_to_project(issue_node_id):
    query = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item { id }
      }
    }
    """
    variables = {"projectId": PROJECT_ID, "contentId": issue_node_id}
    res = requests.post(
        "https://api.github.com/graphql",
        headers=headers_graphql,
        json={"query": query, "variables": variables}
    )
    if res.status_code == 200:
        if "errors" in res.json():
            print(f"⚠️ GraphQL error: {json.dumps(res.json()['errors'], indent=2)}")
        else:
            print("🗂️ Added to project board.")
    else:
        print(f"❌ GraphQL request failed: {res.status_code} - {res.text}")

# === Main workflow ===
for item in sprint_items:
    node_id = create_issue(item["title"], item["body"], item["labels"])
    if node_id:
        time.sleep(1)  # slight delay to avoid rate limits
        add_issue_to_project(node_id)
