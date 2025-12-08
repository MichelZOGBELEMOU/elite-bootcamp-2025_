# Proxmox Access Control — Homelab Security Documentation  

**Author:** Michel Zogbelemou  
**Mentor:** ChatGPT — Senior DevOps/SRE Engineer

---

##  1. Overview
This document defines the access control model, RBAC configuration, SSH hardening, and administrative policies applied to the **Dell PowerEdge R610 running Proxmox VE 9**.  
It is the authoritative reference for hypervisor security throughout all phases of the Elite Bootcamp.

 Purpose & Security Goals

- Eliminate root-based administration  
- Enforce RBAC using named administrator accounts  
- Require SSH key-only authentication  
- Disable all remote root access (SSH + GUI)  
- Harden Proxmox behind a dual-router boundary  
- Provide secure break-glass access via iDRAC  
- Mirror enterprise DevOps/SRE security standards 

---

## 👤 2. User & Authentication Model
Proxmox supports two principal authentication realms:

- **PVE** (internal)
- **PAM** (Linux system accounts)

### 2.1 Proxmox GUI Users

| User | Realm | Enabled | Purpose |
|------|--------|----------|----------|
| `michel@pve` | Proxmox VE | ✔ | Primary administrator (RBAC) |
| `root@pam` | Linux PAM | ❌ | GUI disabled for security |

### ✔ GUI Access  
Only `michel@pve` may log into the Proxmox Web UI.  
Disabling `root@pam` prevents shared credentials and enhances auditability.

---

##  3. RBAC Structure (Groups & Roles)

### 3.1 Group Created
```
Admins
```

### 3.2 Role Assignment
The `Admins` group is assigned the full **Administrator** role on `/`:

```bash
sudo pveum aclmod / -group Admins -role Administrator
```

### 3.3 User → Group Mapping
```bash
sudo pveum usermod michel@pve -group Admins
```

This gives `michel@pve` complete cluster administration without ever using the root GUI account.

---

##  4. SSH Access Model  
SSH access is performed from the **Debian 12 Desktop (10.10.0.10)**, which is the main Control Node in the lab.

### 4.1 Allowed Authentication Policy 
SSH uses **key-only** authentication:

```
PubkeyAuthentication yes
PasswordAuthentication no
```

### 4.2 Root Login Policy  
**Actual lab configuration:**

```
PermitRootLogin no
```

Meaning:

- Root **cannot** SSH in any form  
- No root password  
- No root key login  
- Root is accessible only locally on the console

This is the strongest possible SSH hardening.

### 4.3 Authorized Keys  
Only michel can perform remote SSH administration:

```
/home/michel/.ssh/authorized_keys
```

The Debian Desktop’s `id_ed25519.pub` was copied here.

Root does **NOT** have remote SSH access.

---

##  5. Disabled Access

| Access Type | Status | Reason |
|-------------|--------|--------|
| Root GUI login | ❌ | RBAC enforcement |
| Root SSH login | ❌ | `PermitRootLogin no` |
| SSH password login | ❌ | Key-only |
| External/WAN access to Proxmox | ❌ | Dual NAT protection (Router B → Router A) |
| PAM root GUI login | ❌ | Security best practice |

The hypervisor is isolated behind **two routers**, with no inbound exposure.

---

##  6. Security Architecture Benefits
This hardening aligns with the actual homelab design:

- **Dual-router architecture** (ISP → Lab) isolates the hypervisor  
- **vmbr0** provides WAN egress through Router A  
- **vmbr1** provides LAN access inside `10.10.0.0/24`  
- **dnsmasq** on `10.10.0.20` resolves `*.lab.local` internally  
- **Debian 12 Desktop** is the central administration node  
- **Named user admin (`michel@pve`)** replaces root GUI login  
- **Root SSH completely disabled** for maximum security  
- **Key-only SSH access** matches cloud provider security  
- **iDRAC 10.10.0.34** acts as break-glass access  
## 7. 🧪 Monthly Security Audit Checklist
### 7.1 User & RBAC Validation
```bash
pveum user list
pveum group list
pveum acl list
```
### 7.2 SSH Hardening Validation
```bash
grep -E "PermitRootLogin|PasswordAuthentication" /etc/ssh/sshd_config
```
### 7.3 Network Boundary Validation

- Confirm Proxmox unreachable from WAN
- Validate dual NAT still enforced
- Confirm iDRAC remains isolated on 10.10.0.34
### 7.4 Log Review
```bash
journalctl -u ssh
journalctl -u pvedaemon
journalctl -u pveproxy
```
### 7.5 Key Review

- Remove unused keys
- Confirm root has zero SSH keys

## 8. 🖥️ Emergency / Break-Glass Procedure

If Proxmox GUI or SSH becomes inaccessible:

> Open iDRAC at 10.10.0.34
> Launch remote console
> Repair networking or SSH configuration
> Validate RBAC/SSH policies remain intact
> Document the incident in observability-and-drills/


 Summary

- This hardened access model delivers:
- Zero-trust security
- Full RBAC control
- No remote root exposure
- Key-only authentication
- Strong network segmentation
- Cloud-aligned best practices

This configuration mirrors real-world SRE/DevOps production clusters.



