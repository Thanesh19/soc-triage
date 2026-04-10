import json
import time
import os
from datetime import datetime
from elasticsearch import Elasticsearch

ES_HOST = "http://localhost:9200"
ES_INDEX = "soc-alerts"
WAZUH_ALERTS = "/var/ossec/logs/alerts/alerts.json"
SURICATA_ALERTS = "/var/log/suricata/eve.json"

es = Elasticsearch(ES_HOST)

def normalize_wazuh(alert):
    try:
        return {
            "source": "wazuh",
            "timestamp": alert.get("timestamp"),
            "agent": alert.get("agent", {}).get("name", "unknown"),
            "severity": alert.get("rule", {}).get("level", 0),
            "description": alert.get("rule", {}).get("description", ""),
            "rule_id": alert.get("rule", {}).get("id", ""),
            "category": alert.get("rule", {}).get("groups", []),
            "mitre": alert.get("rule", {}).get("mitre", {}).get("technique", []),
            "raw": alert
        }
    except Exception as e:
        print(f"[WARN] Failed to normalize Wazuh alert: {e}")
        return None

def normalize_suricata(alert):
    try:
        if alert.get("event_type") != "alert":
            return None
        return {
            "source": "suricata",
            "timestamp": alert.get("timestamp"),
            "agent": alert.get("in_iface", "unknown"),
            "severity": alert.get("alert", {}).get("severity", 0),
            "description": alert.get("alert", {}).get("signature", ""),
            "rule_id": str(alert.get("alert", {}).get("signature_id", "")),
            "category": [alert.get("alert", {}).get("category", "")],
            "mitre": [],
            "src_ip": alert.get("src_ip", ""),
            "dest_ip": alert.get("dest_ip", ""),
            "proto": alert.get("proto", ""),
            "raw": alert
        }
    except Exception as e:
        print(f"[WARN] Failed to normalize Suricata alert: {e}")
        return None

def index_alert(doc):
    try:
        es.index(index=ES_INDEX, document=doc)
        print(f"[+] Indexed: [{doc['source']}] {doc['description'][:80]}")
    except Exception as e:
        print(f"[ERROR] Failed to index alert: {e}")

def tail_file(filepath):
    try:
        with open(filepath, "r") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    yield line.strip()
                else:
                    time.sleep(0.5)
    except PermissionError:
        print(f"[ERROR] Permission denied: {filepath} — try running with sudo")
        return

def run():
    print("[*] SOC Normalizer starting...")
    print(f"[*] Watching Wazuh: {WAZUH_ALERTS}")
    print(f"[*] Watching Suricata: {SURICATA_ALERTS}")
    print(f"[*] Indexing to Elasticsearch: {ES_INDEX}")
    print("[*] Press Ctrl+C to stop\n")

    import threading

    def watch_wazuh():
        for line in tail_file(WAZUH_ALERTS):
            try:
                alert = json.loads(line)
                doc = normalize_wazuh(alert)
                if doc:
                    index_alert(doc)
            except json.JSONDecodeError:
                pass

    def watch_suricata():
        for line in tail_file(SURICATA_ALERTS):
            try:
                alert = json.loads(line)
                doc = normalize_suricata(alert)
                if doc:
                    index_alert(doc)
            except json.JSONDecodeError:
                pass

    t1 = threading.Thread(target=watch_wazuh, daemon=True)
    t2 = threading.Thread(target=watch_suricata, daemon=True)
    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Normalizer stopped.")

if __name__ == "__main__":
    run()
