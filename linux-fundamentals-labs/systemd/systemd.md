# systemd ARCHITECTURE - Lab Documentation

Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**

---
## Purpose of This Lab
To understand how systemd manage services, dependencies, boot ordering, and overrides. Mastering these concepts is essential for troubleshooting automation, CI/CD pipelines, and reliable production operations.

---

## 1. Learning Objectives
By the end of this lab, I will be able to:

- Explain the role of systemd as PID 1 and how it manages the entire system lifecycle.
- Identify systemd unit types (service, socket, timer, target, mount, path)
- Read and interpret dependency graphs with `systemd-analyze`
- Inspect unit definitions and analyze startup ordering
- create and validate  service overrides using `systemctl edit`
- Understand how dependency and ordering rules impact boot speed and reliability

--- 

## 2. Concept Overview
Systemd is the init system that starts every service after the kernel boots. It organizes everything into "units", each describing how and when a component should run. Instead of a linear startup, systemd uses dependency rules like `Requires=`, `Wants=`, `Before=`, and `After` to start services in parallel while repecting their requirements. This allows fast booting but also means failures propagate through dependency chains. Overrides let me modify service behavior safely without touching system files.

## 3. Hands-on Experiments

### Experiment 1 - Explore Unit Types
Commands executed:
```bash
systemctl  list-units --type=service
systemctl list-units --type=socket
systemctl list-units --type=timer
systemctl list-units --type=target
```
Goal: Identify active services, timers, and sockets, and understand systemd's srurcture.
### Experiment 2 - Inspect a Service
Service inspected: **ssh.service"

Commands:
```bash
systemctl status ssh.service
systemctl show ssh.sevice | less
```
Key details observed
- ExecStart path
- Required and wanted dependencies
- Restart policy
- Logs sourced from journald

### Experiment 3 - Boot Performance Analysis
commands:
```bash
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
systemd-analyze plot > boot.svg
```

### Experiment 4 - Create a Safe Override
```bash
sudo systemctl edit ssh.service

[Service]
Restart=always
RestartSec=2
```
Reloaded and verified:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.service
sudo systemctl cat ssh.service
sudo systemctl revert ssh.service
```
### Experiment 5 - Analyze Dependency Chains
commands:
```bash
systemd-analyze critical-chain ssh.service
systemd-analyze critical-chain network-online.targert
```
Outcome: Understood how dependency ordering influences service startup reliability.

# 4. Observations
- systemd provides a structured and predictable boot workflow.
- Most delays originate from network and  filesystem units.
- Overrides are powerful and must be used carefully.
- Understanding dependencies allows identifying root causes instead of symptoms.