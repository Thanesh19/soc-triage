# Changelog

## [1.0.0] - Phase 6 release
- Added docs/findings_report.md
- Added docs/architecture.md
- Cleaned up README.md
- 46 alerts, 100 percent detection rate, 5/5 AI triage correct

## [0.5.0] - Phase 5
- Red team validation complete

## [0.4.0] - Phase 4
- AI triage engine with Mistral 7B
- Streamlit dashboard
- Slack notifier

## [0.3.0] - Phase 3
- Suricata NIDS integrated

## [0.2.0] - Phase 2
- Wazuh + Elasticsearch deployed

## [0.1.0] - Phase 1
- Lab setup complete

## [1.1.0] — Phase 7 release

### Added
- docs/phase7_findings.md — false positive testing report

### Phase 7 results
- 4 scenarios tested, 3/4 correctly classified (75%)
- False positive found: sudo whoami classified as Critical
- Root cause: context-free AI lacks user behaviour baseline
- Fix: whitelist rules + alert enrichment recommended
- Wazuh Indexer heap reduced 4GB to 1GB — Mistral 7B runs without RAM issues
