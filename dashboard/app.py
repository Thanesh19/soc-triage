import streamlit as st
import pandas as pd
from elasticsearch import Elasticsearch
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import sqlite3

ES_HOST = "http://localhost:9200"
ES_INDEX = "soc-alerts"
DB_PATH = "feedback.db"

es = Elasticsearch(ES_HOST)
llm = OllamaLLM(model="mistral")

PROMPT_TEMPLATE = """You are a SOC analyst. Analyze this security alert and respond in exactly this format:

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

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT, verdict TEXT, feedback TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

def save_feedback(alert_id, verdict, feedback):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO feedback (alert_id, verdict, feedback) VALUES (?, ?, ?)",
                 (alert_id, verdict, feedback))
    conn.commit()
    conn.close()

def get_alerts(size=50):
    try:
        result = es.search(index=ES_INDEX, body={
            "query": {"match_all": {}},
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": size})
        alerts = []
        for hit in result["hits"]["hits"]:
            src = hit["_source"]
            src["_id"] = hit["_id"]
            alerts.append(src)
        return alerts
    except Exception as e:
        st.error(f"Elasticsearch error: {e}")
        return []

def triage_alert(alert):
    prompt = PROMPT_TEMPLATE.format(
        source=alert.get("source", "unknown"),
        severity=alert.get("severity", 0),
        description=alert.get("description", ""),
        category=alert.get("category", []),
        mitre=alert.get("mitre", []))
    return llm.invoke(prompt)

def severity_color(level):
    if level >= 10: return "🔴"
    elif level >= 7: return "🟠"
    elif level >= 4: return "🟡"
    else: return "🟢"

init_db()
st.set_page_config(page_title="SOC Triage Dashboard", layout="wide")
st.title("🛡️ SOC Triage Dashboard")
st.caption("AI-powered alert triage using Mistral 7B + Wazuh + Suricata")

alerts = get_alerts(50)
wazuh_count = sum(1 for a in alerts if a.get("source") == "wazuh")
suricata_count = sum(1 for a in alerts if a.get("source") == "suricata")

col1, col2, col3 = st.columns(3)
col1.metric("Total Alerts", len(alerts))
col2.metric("Wazuh Alerts", wazuh_count)
col3.metric("Suricata Alerts", suricata_count)
st.divider()

if not alerts:
    st.warning("No alerts found in Elasticsearch.")
else:
    for i, alert in enumerate(alerts):
        source = alert.get("source", "unknown").upper()
        description = alert.get("description", "No description")
        severity = alert.get("severity", 0)
        category = alert.get("category", [])
        mitre = alert.get("mitre", [])
        alert_id = alert.get("_id", str(i))

        with st.expander(f"{severity_color(severity)} [{source}] {description[:80]}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Severity Score:** {severity}")
                st.write(f"**Category:** {', '.join(category) if category else 'N/A'}")
            with col_b:
                st.write(f"**MITRE Tags:** {', '.join(mitre) if mitre else 'N/A'}")
                st.write(f"**Timestamp:** {alert.get('timestamp', 'N/A')[:19]}")

            if st.button(f"🤖 Triage with AI", key=f"triage_{i}"):
                with st.spinner("Mistral is analyzing..."):
                    verdict = triage_alert(alert)
                st.session_state[f"verdict_{i}"] = verdict

            if f"verdict_{i}" in st.session_state:
                st.code(st.session_state[f"verdict_{i}"], language="text")
                col_fb1, col_fb2 = st.columns(2)
                with col_fb1:
                    if st.button("👍 Correct", key=f"up_{i}"):
                        save_feedback(alert_id, st.session_state[f"verdict_{i}"], "correct")
                        st.success("Feedback saved!")
                with col_fb2:
                    if st.button("👎 Incorrect", key=f"down_{i}"):
                        save_feedback(alert_id, st.session_state[f"verdict_{i}"], "incorrect")
                        st.warning("Feedback saved!")

st.divider()
st.subheader("📊 Feedback Stats")
try:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT feedback, COUNT(*) as count FROM feedback GROUP BY feedback", conn)
    conn.close()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No feedback yet.")
except:
    st.info("No feedback data yet.")
