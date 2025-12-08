# Logrotate & Filesystem Basics
Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**

___

# 1. Overview

This lab covers two essentisal linux fundamentals:

- Understanding the Linux filesystem layout
- Managing log files using logrotate

The goal is to have production-ready skills for maintaining logs, preventing disk exhaustion, and integrating log rotation with systemd-based services.

---
# 2. Learning Objectives
By completing this lab, I will:

- Understand how Linux organizes configuration, binaries and logs.
- Inspect and analyze `/etc/logrotate.conf`
- Create custom log rotation rules under `/etc/logrotaste.d/`\
- Perform dry-run and real manual rotations.
- Integrate logrotate with a custom systemd service.
- Validate rotation behavior across multiple cycles.

---

# 3. Filesystem Essentials for DevOps

## 3.1 /etc - Configuration Files

Contains system-wide configuration:
- `/etc/systemd/system` --> custom unit files
- `/etc/logrotate.conf` --> global rotation policy
- `/etc/logrotate.d` --> per-service rotation rules

Changes here directly influence system behavior.

---
## 3.2 /var - Dynamic Data

Contains frequently modified data:

- `/var/log` --> system & app logs
- `/var/lib` --> state for services like Docker, DBs, Prometheus

Logs grow continuously, making `/var/log` a critical directory to monitor.

---

## 3.3 /usr - System Applications

contains binaries and libraries provided by the OS:
- `/usr/bin/` --> essential executables
- `/usr/lib/systemd/` --> default unit files shipped with systemd

These should rarely be modified directly

---

## 3.4 /opt - Optional Software

Used for manually installed applications:

- Jenkins
- Prometheus / Grafana
- Custom Python tools

Helps keep the system organized by separting custom services from OS binaries.

# 4. Logrotate Fundamentals

Logrotate prevents log files from growing indefinitely.

## What logrotate does:

- Rotates logs based on size or time intervals.
- Compresses old logs using gzip.
- Keeps a configurable number of historical logs.
- Runs post-rotation commands
- Ensures logs never fill disk space.

---

# 5. Inspectiong Logrotate Configuration

## 5.1 Global Configuration

Open and read:
```bash
/etc/logrotate.conf
```
Typical directives include:

- `weekly`
- `rotate 4`
- `create`
- `compress`
- `include /etc/logrotate.d`

---

## 5.2 Per-service Configuration
```bash
/etc/logrotate.d
```
Here we find rotation rules for:
- apt
- rsyslog
- nginx
- Custom services
