import json
from elasticsearch import Elasticsearch
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

ES_HOST = "http://localhost:9200"
ES_INDEX = "soc-alerts"

es = Elasticsearch(ES_HOST)
llm = OllamaLLM(model="mistral")

PROMPT = PromptTemplate(
    input_variables=["source", "severity", "description", "category", "mitre"],
    template="""You are a SOC analyst. Analyze this security alert and respond in exactly this format:

SEVERITY: [Critical/High/Medium/Low]
ATTACK_TYPE: [type of attack]
MITRE_TECHNIQUE: [technique name and ID if known]
EXPLANATION: [1-2 sentences explaining what happened]
ACTION: [what the analyst should do]

Alert details:
- Source: {source}
- Severity score: {severity}
- Description: {description}
- Category: {category}
- MITRE tags: {mitre}"""
)

def get_recent_alerts(n=5):
    result = es.search(
        index=ES_INDEX,
        body={
            "query": {"match_all": {}},
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": n,
            "_source": ["source", "severity", "description", "category", "mitre", "timestamp"]
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

def triage_alert(alert):
    prompt = PROMPT.format(
        source=alert.get("source", "unknown"),
        severity=alert.get("severity", 0),
        description=alert.get("description", ""),
        category=alert.get("category", []),
        mitre=alert.get("mitre", [])
    )
    return llm.invoke(prompt)

def run():
    print("[*] SOC AI Triage starting...")
    print("[*] Fetching recent alerts from Elasticsearch...\n")
    alerts = get_recent_alerts(5)
    if not alerts:
        print("[!] No alerts found in Elasticsearch.")
        return
    for i, alert in enumerate(alerts, 1):
        print(f"{'='*60}")
        print(f"ALERT {i}: [{alert.get('source','?').upper()}] {alert.get('description','')[:80]}")
        print(f"{'='*60}")
        print("[*] Sending to Mistral for triage...")
        verdict = triage_alert(alert)
        print(verdict)
        print()

if __name__ == "__main__":
    run()
