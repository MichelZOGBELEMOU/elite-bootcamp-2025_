# Linux Processes & Signals 
Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**

## Overview 

This documentation covers the **Linux process model**, **signal handling**, **niceness**, and **kernel-level analysis**.
This module buils the foundation required for advanced troubleshooting, service operations, and Kubernetes process/container analysis.

---

## 1. Understanding Linux Processes

A **process** is a running program with its own:

- **PID** unique identifier
- **PPID** parent process
- **UID/GID** owner/user
- **State** running, sleeping, stopped, zombie.
- **Priority & niceness** CPU scheduling weight\
- **Cgroup** used heavily by systemd, Docker, and Kubernetes

Processes are created through:

fork(): creates a child process
exec(): replaces the process with a new program

### Process Inspection Tools

| Tool | Description |
|------|-------------|
| `ps` | Lists processes (snapshot) |
| `top` | Dynamic process view |
| `htop` | Enhanced interactive viewer |
| `pgrep` | Find processes by name |
| `pkill` | Kill processes by name |
| `pidof` | Return PID of a running program |

Examples:
```bash
ps -ef | head
ps aux --sort=-%cpu | head
top
htop
```
## 2. Linux Signals
| Signal       | Meaning                      | Typical Use                          |
|--------------|-------------------------------|----------------------------------------|
| SIGTERM (15) | Graceful shutdown             | systemd stop, polite termination       |
| SIGKILL (9)  | Forced kill; cannot be trapped| Last resort                            |
| SIGINT (2)   | Keyboard interrupt            | Ctrl-C                                 |
| SIGHUP (1)   | Reload configuration          | Daemons                                |
| SIGSTOP (19) | Pause process                 | Debugging                              |
| SIGCONT (18) | Resume paused process         | Debugging                              |
| SIGUSR1/2    | Application-defined           | Custom actions                         |

### Sending signals
```bash
kill -15 <PID>      # Graceful terminate
kill -9 <PID>       # Force kill
kill -STOP <PID>    # Pause
kill -CONT <PID>    # Resume
killall nginx       # Kill by name
```
## 3. Scheduling & Niceness

Linux uses the completely Fair Scheduler (CFS)
Niceness levels:
- -20 --> Highest priority
- 0 --> Default priority
- +19 --> Lowest priority

Example
```bash
nice -n -5 yes > /dev/null &
renice -n 10 <PID>
```

### Key Concept:
Niceness adjusts CPU priority - but does not override cgroups (important when analyzing systemd services and kubernetes pods later in program).
