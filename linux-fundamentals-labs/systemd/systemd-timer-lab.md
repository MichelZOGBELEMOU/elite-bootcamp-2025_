## Systemctl Operations + Systemd Timers

Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**
---

## 1. Overview
This day focused on mastering **systemctl operation** and understanding how **systemd timers** provide reliable scheduling compared to traditional cron jobs.
The goal is to build strong intuition for how services are controlled, how timers trigger them, and why systemd's architecture provides superior observability and reliability in  production environments.

---

## 2. systemctl Fundamentals
`systemctl` is the command-line interface for interaction with systemd. It manages unit files, service lifecycle, dependencies, and timers.

## 2.1 core Lifecycle Commands
| Command | Purpose |
|--------|---------|
| `systemctl start <unit>` | Immediately start a service |
| `systemctl stop <unit>` | Stop a running service |
| `systemctl restart <unit>` | Stop → start the service |
| `systemctl reload <unit>` | Reload configuration without stopping |
| `systemctl enable <unit>` | Enable service at boot |
| `systemctl disable <unit>` | Remove from boot sequence |
| `systemctl status <unit>` | Show service state and logs |
| `systemctl daemon-reload` | Reload unit definitions after edits |

These operations form the foundation for service management on all modern Linux distributions.

___

## 3. Introduction to Systemd Timers

systemd timers are event-based scheduling units that trigger service units at defined intervals or specific times. They are the systemd-native alternative to cron.

### 3.1 How Timers Work
A timer unit activates a corresponding service unit.

Example pairing:
- `backup.service` --> what runs
- `backup.timer` --> when it runs
Timers support a wide range of scheduling directives:
- `OnCalendar=`
- `OnBootSec=`
- `OnActiveSec=`
- `OnUnitActiveSec=`

### 3.2 Why Timers Replace cron

Timers offer several advantages:

#### **Reliability**
 Respect dependency ordering (`After=`, `Requires=`).
- Do not run before the system is fully ready.
- Can catch up on missed runs when `Persistent=true`.

#### **Observability**
- Every execution is logged in journald.  
- Exit statuses, stdout, stderr, and metadata are preserved.

Logs can be inspect via:

```bash
journalctl -u <service>
```

#### Integration with systemd

Timers integrate directly into the init system, allowing consistent management across the entire OS.

## 4. Timer + Service Architecture

### 4.1 Service Units

A service defines an action to be executed.
For timers, services are typically:

- Type=oneshot
- A single command or script
- Non-daemon tasks

### 4.2 Timer Units

A timer defines when to run the service.

Common fields:

- OnBootSec= — delay after boot
- OnUnitActiveSec= — interval after last activation
- OnCalendar= — cron-like patterns
- Persistent= — prevents missed executions
Example:

```bash
OnBootSec=1min              # Run once, one minute after boot
OnUnitActiveSec=30s         # Run every 30 seconds
OnCalendar=*-*-* 00:00:00   # Run daily at midnight
```

Timers can be enabled and started like any other unit:
```bash 
systemclt enable mytask.timer
```
___

## 5. Inspecting and Troubleshooting Timers

### 5.1 Listing Timers
```bash
systemctl list-timers
```
Shows:
- NEXT run
- LAST run
- UNIT associated service
- ACTIVATES column
### 5.2 Viewing Logs
Because timers trigger services, logs belong to the service unit, not the timer:
```bash
journalctl -u mytask.service
```
### 5.3 Checking Unit Merging
To see all configuration(including overrides):
```bash
systemctl cat mytask.service
```
### 6. Why Systemd Timers Matter in DevOps
Timers are heavily used across real production systems:
- Running backup jobs
- Rotating logs
- Regenerating configs
- Cleaning temporary files
- Re-running queues or workers
- Triggering health checks
- Pre-deployment checks
- Infrastructure housekeeping tasks

Their integration with journald and systemd's dependency model makes them safe, predictable, and debuggable - essential properties in SRE, DevOps, and platform engineering.