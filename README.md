# SOC Triage — AI-Powered Security Operations Center

A local AI-powered SOC triage tool that automatically analyzes security alerts and produces human-readable verdicts mapped to MITRE ATT&CK techniques.

## Stack
- **Detection**: Wazuh (HIDS) + Suricata (NIDS)
- **Storage**: Elasticsearch + ChromaDB
- **AI**: Mistral 7B via Ollama + LangChain RAG
- **Dashboard**: Streamlit
- **Notifications**: Slack webhook

## Status
- [x] Phase 1 — Detection layer (Wazuh + Suricata)
- [x] Phase 2 — Storage + pipeline
- [x] Phase 3 — AI triage layer
- [x] Phase 4 — Dashboard + notifications
- [ ] Phase 5 — Red team + metrics
- [ ] Phase 6 — Polish + publish
