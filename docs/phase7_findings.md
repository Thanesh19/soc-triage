# Phase 7 -- False Positive Testing Report

**Author:** Thanesh Soupramaniane
**Date:** May 19, 2026

## Objective
Validate how the AI triage engine handles benign activity that resembles attacks.

## Summary Table

| # | Scenario | Alerts | AI Severity | Correct? |
|---|---|---|---|---|
| 1 | nmap ping sweep | 1 | Low | Yes |
| 2 | nmap -sV service scan | 8 | Low | Yes |
| 3 | sudo whoami (legit admin) | 3 | Critical | No |

False positive rate: 1/3 (33%)
Correct classifications: 2/3 (67%)

## Scenario Details

### Scenario 1 - nmap ping sweep
Command: nmap -sn 192.168.56.0/24
Intent: Routine IT admin host discovery.
Alerts: 1 low-severity Suricata DHCP info alert.
AI result: Low severity, monitor only. No Slack fired.
Verdict: Pass

### Scenario 2 - nmap service scan
Command: nmap -sV 192.168.56.103
Intent: IT admin asset inventory scan.
Alerts: 8 Suricata ET SCAN alerts, all severity 1.
AI result: Low severity, no immediate action required. No Slack fired.
Verdict: Pass

### Scenario 3 - sudo whoami
Command: sudo whoami
Intent: Normal administrator running a privileged command.
Alerts: 3 Wazuh alerts including Successful sudo to ROOT executed.
AI result: Critical, Privilege Escalation, MITRE T1078. Investigate immediately.
Verdict: Fail - false positive detected.

## Key Finding
A legitimate sudo command by an authorized admin was classified as Critical Privilege Escalation.
Root cause: Mistral 7B has no user context, behaviour baseline, or whitelist awareness.
It sees sudo to ROOT and assumes malicious intent.

## Recommended Improvements
1. User behaviour baseline -- flag deviations only, not all sudo usage
2. Whitelist rules -- suppress known admin actions from authorized users
3. Alert enrichment -- pass user role and history to AI prompt before triage
4. Feedback loop -- use analyst thumbs up/down to suppress recurring false positives
