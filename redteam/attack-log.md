# Red Team Attack Log — Phase 5

## Environment
- Attacker: Kali Linux 2026.1 (192.168.56.104)
- Target: Metasploitable2 (192.168.56.103)
- Date: April 16, 2026

## Attacks Performed

### 1. Reconnaissance — Port Scan
- Tool: nmap -sS -sV -T4
- Result: 23 open ports discovered including vsftpd 2.3.4, SSH 4.7, MySQL, VNC
- Detected by: Suricata (ET SCAN Nmap User-Agent — 8 alerts)

### 2. Initial Access — SSH Login
- Tool: ssh with legacy key algorithms
- Credentials: msfadmin/msfadmin (default)
- Result: Successful login
- Detected by: Wazuh (PAM login session alerts)

### 3. Credential Attack — FTP Brute Force
- Tool: Hydra rockyou.txt wordlist
- Target: ftp://192.168.56.103
- Result: Attack launched (14M password attempts)
- Detected by: Wazuh (authentication failure alerts)

### 4. Exploitation — vsftpd 2.3.4 Backdoor
- Tool: Metasploit exploit/unix/ftp/vsftpd_234_backdoor
- CVE: CVE-2011-2523
- Result: Meterpreter root shell obtained
- Detected by: Suricata (GPL ATTACK_RESPONSE id check returned root) + Wazuh

### 5. Credential Theft — /etc/shadow Exfiltration
- Tool: cat /etc/shadow via Meterpreter shell
- Result: All 28 password hashes exfiltrated
- Detected by: Wazuh (process activity)

## Final Metrics
- Total alerts generated: 46
- Suricata detections: 12
- Wazuh detections: 34
- Detection rate: 5/5 attacks detected (100%)
- MITRE ATT&CK coverage: T1595, T1110, T1190, T1078, T1003
