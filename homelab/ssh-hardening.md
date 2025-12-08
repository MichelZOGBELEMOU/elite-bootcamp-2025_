# SSH Hardening — Elite DevOps Homelab

**Author: Michel Zogbelemou**  
**Mentor: ChatGPT — Elite DevOps Career Mentor**  
Environment: Debian 12 Desktop · Proxmox VE 9 (R610) · Debian DNS VM · Fedora Test Node  
Domain: `lab.local`  

---

## 1. Overview

This document defines the standardized SSH security baseline for all nodes in the Elite DevOps Homelab.  
The configuration enforces key-only access, disables root login, and aligns with enterprise DevSecOps standards.

- **Router A → Router B (double NAT)**  
- **Proxmox R610 (10.10.0.2)**  
- **Debian Desktop Control Node (10.10.0.10)**  
- **DNS01 Debian Server (10.10.0.20)**  
- **Fedora Test Node (192.168.45.x)**  

The goal is to secure all SSH endpoints, ensure key-based authentication, block root login, and align security with DevOps production standards.

---

## 2. Security Goals


- Enforce **SSH key-based authentication only**
- Disable **password access** across all nodes
- Disable **all remote root login** (SSH + GUI on Proxmox)
- Standardize user access via `michel + sudo`
- Harden Debian, Fedora, and Proxmox identically
- Restrict SSH exposure to internal LAN subnets only
- Ensure compatibility with Ansible automation and CI pipelines

---

## 3. SSH Key Setup

### 3.1 Generate keypair (Control Node)

```bash
ssh-keygen -t ed25519 -C "michel@lab.local"
```
Generated files:

~/.ssh/id_ed25519

~/.ssh/id_ed25519.pub

Permissions:

### 3.2 Distribute SSH keys
```bash
ssh-copy-id michel@r610.lab.local
ssh-copy-id michel@dns-01.lab.local
ssh-copy-id michel@<any-new-node>
```
All management happens from 10.10.0.10 (Control Node).

## 4. Standardized SSH Configuration
This section applies to all Linux nodes including Proxmox, Debian VMs, and Fedora.

Path:

```bash

/etc/ssh/sshd_config
```
### 4.1 Required hardening directives
 Disable root access (mandatory)
```bash
PermitRootLogin no
```
Key-based login only
```bash
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
```

Keep PAM for account/session handling
```bash
UsePAM yes
```

Connection limits
```bash
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

### 4.2 Restart SSH safely
```bash
sudo systemctl reload ssh
```

---


## 5. User & Root Policy
### 5.1 Linux hosts
**Primary admin user: michel**

Added to sudo:
```bash
usermod -aG sudo michel
```
All administration is done using:

```bash
ssh michel@host
sudo <command>
```
## 5.2 Root login policy
SSH root login is completely disabled:

```bash
PermitRootLogin no
```
GUI root login is also disabled on Proxmox:

```bash
pveum usermod root@pam --enable 0
```
This aligns with industry best practices and SRE compliance rules.

## 6. Proxmox-Specific Hardening (R610)
### 6.1 Create Proxmox admin user
```bash
pveum user add michel@pve
pveum passwd michel@pve
```
### 6.2 Create Admins group
```bash
pveum group add Admins
pveum usermod michel@pve --group Admins
```
### 6.3 Assign full admin role
```bash
pveum aclmod / --group Admins --role PVEAdmin
```
### 6.4 Disable root GUI login
```bash
pveum usermod root@pam --enable 0
```
### 6.5 Login workflow
Web GUI login → https://r610.lab.local:8006

User: michel

Realm: Proxmox VE authentication server

Root via GUI is disabled permanently.

## 7. DNS-01 (Debian DNS Server)
Follows same SSH hardening:

```bash
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
KbdInteractiveAuthentication no
UsePAM yes
```
Admin access:

```bash
ssh michel@dns01.lab.local
sudo nano /etc/dnsmasq.conf
```


## 8. Validation Checklist
### 8.1 Root login blocked
```bash
ssh root@r610.lab.local
```
 **Permission denied (publickey)**

### 8.2 Password login blocked
```bash
ssh michel@dns01.lab.local
```
 **use key**
### 8.3 Key login works
```bash
ssh michel@r610.lab.local
hostnamectl
```
### 8.4 Proxmox GUI policies
root@pam disabled

michel@pve active

Admins group has PVEAdmin role at /

## 9. Summary
SSH hardened across the homelab.

Root SSH login disabled (PermitRootLogin no).

Only key-based access allowed.

Proxmox GUI root login disabled → michel@pve replaces root.

