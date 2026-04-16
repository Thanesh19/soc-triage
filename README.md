# SOC Triage — AI-Powered Security Operations Center

A local AI-powered SOC triage tool that automatically analyzes security alerts and produces human-readable verdicts mapped to MITRE ATT&CK techniques.

## Stack
- **Detection**: Wazuh (HIDS) + Suricata (NIDS)
- **Storage**: Elasticsearch + Docker
- **AI**: Mistral 7B via Ollama + LangChain
- **Dashboard**: Streamlit
- **Notifications**: Slack webhook

## Status
- [x] Phase 1 — Detection layer (Wazuh + Suricata)
- [x] Phase 2 — Storage + pipeline
- [x] Phase 3 — AI triage layer
- [x] Phase 4 — Dashboard + notifications
- [x] Phase 5 — Red team + metrics (46 alerts, 100% detection rate)
- [ ] Phase 6 — Polish + publish

## Red Team Results
- Target: Metasploitable2 (192.168.56.103)
- Attacks: nmap scan, SSH login, FTP brute force, vsftpd CVE-2011-2523 exploit, credential theft
- Total alerts: 46
- Detection rate: 5/5 attacks detected (100%)
- MITRE coverage: T1595, T1110, T1190, T1078, T1003
