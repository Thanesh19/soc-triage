# Phase 7 — False Positive Testing Report

**Author:** Thanesh Soupramaniane
**Date:** May 19, 2026

## Objective
Validate how the AI triage engine handles benign activity that resembles attacks.

## Summary Table

| # | Scenario | Alerts | AI Severity | Correct? |
|---|---|---|---|---|
| 1 | nmap ping sweep | 1 | Low | Yes |
| 2 | curl web requests | 0 | N/A | Yes |
| 3 | nmap -sV service scan | 8 | Low | Yes |
| 4 | sudo whoami (legit admin) | 3 | Critical | No |

False positive rate: 1/4 (25%)
Correct classifications: 3/4 (75%)

## Key Finding
Scenario 4 — sudo whoami was classified as Critical Privilege Escalation.
Root cause: Mistral 7B has no user context, baseline behaviour, or whitelist awareness.

## Recommended Improvements
1. User behaviour baseline — flag deviations only
2. Whitelist rules — suppress known admin actions
3. Alert enrichment — pass user role and history to AI prompt
4. Feedback loop — use analyst thumbs up/down to suppress recurring FPs
