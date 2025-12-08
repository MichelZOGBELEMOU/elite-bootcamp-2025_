# Journald Deep Dive

Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**

---
## Objective

This lab provides hands-on experience with **systemd-journald**, including

- How journald collects, stores, and indexes logs
- Volatile vs persistent log modes
- Enabling persistent logging
- Advanced filtering with `journalctl`
- Configuring log retention
- Using journald to troubleshoot service failures

---

## 1. Journald Architecture overview

### What journald captures
- Kernel logs
- User-space service logs
- Syslog messages
- Structured metadata: `_PID`, `_UID`, `_SYSTEMD_UNIT`

### Storage locations

| Mode | Directory | Description |
|------|-----------|-------------|
| **Volatile** | `/run/log/journal` | Logs stored in RAM; lost on reboot |
| **Persistent** | `/var/log/journal` | Logs stored on disk; survive reboot |

Journald switches to persistent mode when `/var/log/journal` exists.

---

## 2. Lab 1 - Enable Persistent Journald

### Step 1 - Create the directory
```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
```

### Step 2 - Restart journald
```bash
sudo systemctl restart systemd-journald
```
## 3. Lab 2 - journalctl Filters

### Boot-level filters
```bash
journalctl -b
journalctl -b -1
```
### Unit-level filters

```bash
journactl -u ssh
journalctl -xeu ssh
```
### Real-time streaming
```bash
journalctl -fu nginx
```
### Severity filters
```bash
journalctl -p err
journalctl -p warning..err
```
### Time filters
```bash
journalctl --since "10 minutes ago"
journalctl --since yesterday --until now
```

### Metadata filters

```bash
journalctl _PID=1234
journalctl _UID=1002
journalctl _COMM=sshd
journalctl _SYSTEMD_UNIT=nginx.service
```
### Disk usage
```bash
journalctl --disk-usage
```

## 4. Lab 3 - Configure Log Retention

Open:
```bash
sudo nano /etc/systemd/journald.conf
```
set:
```bash
SystemMaxUse=500M
SystemKeepFree=200M
SystemMaxFileSize=50M
SystemMaxFiles=5
```
Restart:
```bash
sudo systemctl restart systemd-journald
```