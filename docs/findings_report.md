# Phase 5 Red-Team Findings Report

Author: Thanesh Soupramaniane
Date: April 16 2026

## Summary

5 attacks. 46 alerts. 100 percent detection rate.

## Attacks

| # | Attack | Tool | Alerts | MITRE | Severity | Slack |
|---|--------|------|--------|-------|----------|-------|
| 1 | Port scan | nmap | 8 | T1595 | Medium | No |
| 2 | SSH default login | ssh | 12 | T1078 | Medium | No |
| 3 | FTP brute force | Hydra | 9 | T1110 | High | Yes |
| 4 | vsftpd backdoor CVE-2011-2523 | Metasploit | 11 | T1190 | Critical | Yes |
| 5 | /etc/shadow read | cat via shell | 6 | T1003 | Critical | Yes |
| | Total | | 46 | | | 3/5 |

## AI Triage Results

All 5 severity classifications were correct. No hallucinated CVEs.

## Key findings

- vsftpd 2.3.4 backdoor gave root shell in under 5 seconds
- 28 password hashes exfiltrated from /etc/shadow
- Wazuh real-time FIM was essential for detecting scenario 5
- Dual sensor coverage (Suricata + Wazuh) gave best results on scenario 4

## Conclusion

System is validated and ready for v1.0 release.
