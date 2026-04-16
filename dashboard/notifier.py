import requests
import os
import json
from elasticsearch import Elasticsearch

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL", "")
ES_HOST = "http://localhost:9200"
ES_INDEX = "soc-alerts"
SEVERITY_THRESHOLD = 5

es = Elasticsearch(ES_HOST)

def send_slack_alert(alert):
    severity = alert.get("severity", 0)
    description = alert.get("description", "Unknown")
    source = alert.get("source", "unknown").upper()
    category = ", ".join(alert.get("category", []))
    mitre = ", ".join(alert.get("mitre", []))
    timestamp = alert.get("timestamp", "")[:19]

    emoji = "🔴" if severity >= 10 else "🟠"

    message = {
        "text": f"{emoji} *CRITICAL SOC ALERT*",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"{emoji} Critical Alert Detected"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Source:*\n{source}"},
                    {"type": "mrkdwn", "text": f"*Severity:*\n{severity}/10"},
                    {"type": "mrkdwn", "text": f"*Description:*\n{description}"},
                    {"type": "mrkdwn", "text": f"*Timestamp:*\n{timestamp}"},
                    {"type": "mrkdwn", "text": f"*Category:*\n{category}"},
                    {"type": "mrkdwn", "text": f"*MITRE:*\n{mitre if mitre else 'N/A'}"}
                ]
            },
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": "SOC Triage Lab — AI-powered alert system"}]
            }
        ]
    }

    response = requests.post(SLACK_WEBHOOK, json=message)
    if response.status_code == 200:
        print(f"[+] Slack alert sent: {description[:60]}")
    else:
        print(f"[ERROR] Slack failed: {response.status_code} {response.text}")

def check_critical_alerts():
    print("[*] Checking for critical alerts...")
    result = es.search(
        index=ES_INDEX,
        body={
            "query": {"range": {"severity": {"gte": SEVERITY_THRESHOLD}}},
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 5
        }
    )
    alerts = [hit["_source"] for hit in result["hits"]["hits"]]
    print(f"[*] Found {len(alerts)} critical alerts")
    for alert in alerts:
        send_slack_alert(alert)

if __name__ == "__main__":
    check_critical_alerts()
