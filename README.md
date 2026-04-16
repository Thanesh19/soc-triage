# SOC Triage — AI-Powered Security Operations Center

A fully local, AI-powered SOC triage tool that detects real attacks, analyzes alerts using Mistral 7B, and produces MITRE ATT&CK mapped verdicts — no cloud, no paid APIs.

## Architecture
Attack → Wazuh/Suricata → Python Normalizer → Elasticsearch → LangChain + Mistral 7B → Streamlit Dashboard → Slack Alerts

## Stack
| Tool | Version | Purpose |
|------|---------|---------|
| Wazuh | 4.7.5 | Host-based intrusion detection (HIDS) |
| Suricata | 8.0.4 | Network intrusion detection (NIDS) |
| Elasticsearch | 8.13 | Alert storage and search |
| Ollama + Mistral 7B | latest | Local AI triage engine |
| LangChain | latest | Prompt chain connecting alerts to AI |
| Streamlit | latest | SOC analyst dashboard |
| Slack Webhooks | - | Critical alert notifications |

## Red Team Results
- Target: Metasploitable2 (deliberately vulnerable VM)
- Total alerts generated: 46
- Detection rate: 5/5 attacks detected (100%)

| Attack | Tool | MITRE | Detected By |
|--------|------|-------|-------------|
| Port scan | nmap -sS -sV -T4 | T1595 | Suricata |
| SSH login | ssh legacy auth | T1078 | Wazuh |
| FTP brute force | Hydra rockyou.txt | T1110 | Wazuh |
| vsftpd backdoor exploit | Metasploit CVE-2011-2523 | T1190 | Suricata + Wazuh |
| Credential theft | cat /etc/shadow | T1003 | Wazuh |

## How to Run
```bash
# Start Elasticsearch
sudo docker start soc-elasticsearch

# Start Wazuh
sudo systemctl start wazuh-manager

# Start Suricata
sudo systemctl start suricata

# Run normalizer
cd ~/soc-triage && source venv/bin/activate
sudo venv/bin/python pipeline/normalizer.py &

# Run dashboard
streamlit run dashboard/app.py

# Run Slack notifier
SLACK_WEBHOOK_URL=$(grep SLACK_WEBHOOK_URL .env | cut -d= -f2) python dashboard/notifier.py
```

## Phase Status
- [x] Phase 1 — Detection layer (Wazuh + Suricata)
- [x] Phase 2 — Storage + pipeline (Elasticsearch)
- [x] Phase 3 — AI triage layer (Mistral 7B + LangChain)
- [x] Phase 4 — Dashboard + notifications (Streamlit + Slack)
- [x] Phase 5 — Red team + metrics (46 alerts, 100% detection rate)
- [x] Phase 6 — Polish + publish

## Author
Thanesh Soupramaniane — github.com/Thanesh19
