# SELinux Concepts
Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**

---

# Objectives
- Understand SELinux's Mandatory Acces Control (MAC) model.
- Inspect and compare SELinux contexts
- Learn how SELinux enforces process, file, and port labeling.
- Interpret SELinux modes (Enforcing, Permissive, Disable).
- Prepare for SELinux management and troubleshooting lab.

---

## SELinux Foundations

SELinux adds a powerful security layer on top o standard Linux permissions.

> **"Even if the user or process is compromised, what is this process *allowed* to do?"**

### SELinux Modes
 Mode | Description | Use Case |
|------|-------------|----------|
| **Enforcing** | Violations are blocked | Production default |
| **Permissive** | Violations logged but not blocked | Debugging, testing |
| **Disabled** | SELinux is off | Never used in production |

Check mode:
```bash
getenforce
sestatus
```
___

### SELinux Context Structure

A full SELinux label looks like:
```bash
user:role:type:level
```
Example for Apache:
```bash
system_u:system_r:httpd_t:s0
```
The type (httpd_t) is the most important field.
It defines how a process interacts with files, ports and other resources.
Key idea:
**If the type doesn't match the policy, SELinux denies access, even if file permissions are correct.**

---

### Contexts for files, Processes and ports

- Files: ls -Z
- Processes: ps -Z
- Current user: id -Z
- Ports: semanage port -l

This creates a complete, mandatory access control system the kernel enforces independently of chmod, chown, or ACLs.

This creates a complete, mandatory acces control system the kernel enforces independently of chmod, chown, or ACLs.

---

### Hands-On Lab
check screenshoots.
