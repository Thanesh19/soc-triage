# Architecture

## Pipeline stages

1. Kali Linux attacks Metasploitable 2 (192.168.56.103)
2. Wazuh Agent collects host logs. Suricata inspects network packets.
3. pipeline/normalizer.py reads both and indexes alerts to Elasticsearch.
4. ai/triage.py fetches alerts and sends them to Mistral 7B via Ollama.
5. Mistral returns: severity, attack type, MITRE technique, recommended action.
6. dashboard/app.py shows all alerts and AI verdicts in a browser.
7. dashboard/notifier.py sends Slack messages for severity 5 and above.

## Flow

Attack -> Wazuh/Suricata -> normalizer.py -> Elasticsearch -> triage.py -> Mistral 7B -> dashboard + Slack

## Ports

- Elasticsearch: 9200
- Ollama: 11434
- Streamlit: 8501

## Limitations

- notifier.py is one-shot, no deduplication
- Dashboard has no login/authentication
- No log retention policy on Elasticsearch
