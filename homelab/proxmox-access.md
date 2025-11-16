# Proxmox Access Control — Homelab Security Documentation  

**Author:** Michel Zogbelemou  
**Mentor:** ChatGPT — Senior DevOps/SRE Engineer

---

## 🔐 1. Overview
This document describes the hardened access model used for the **Dell PowerEdge R610 running Proxmox VE 8** inside the dual-router Elite DevOps Homelab.

Goals:

- Remove root-based web administration  
- Enforce RBAC (Role-Based Access Control)  
- Use SSH key authentication only  
- Disable all remote root access (GUI and SSH)  
- Harden the hypervisor inside a dual-NAT network  
- Match DevOps/SRE production-grade security  

---

## 👤 2. User & Authentication Model

### 2.1 Proxmox GUI Users

| User | Realm | Enabled | Purpose |
|------|--------|----------|----------|
| `michel@pve` | Proxmox VE | ✔ | Primary administrator (RBAC) |
| `root@pam` | Linux PAM | ❌ | GUI disabled for security |

### ✔ GUI Access  
Only **michel@pve** can log into the Proxmox Web UI.  
Root GUI access is intentionally disabled to enforce RBAC.

---

## 🧩 3. RBAC Structure (Groups & Roles)

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
```
michel@pve → Admins
```

This gives `michel@pve` complete cluster administration without ever using the root GUI account.

---

## 🔐 4. SSH Access Model  
SSH access is performed from the **Debian 12 Desktop (10.10.0.10)**, which is the main Control Node in the lab.

### 4.1 Allowed Authentication  
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
- Root is accessible only locally on the console (or via iDRAC 10.10.0.34)

This is the strongest possible SSH hardening.

### 4.3 Authorized Keys  
Only Michel can perform remote SSH administration:

```
/home/michel/.ssh/authorized_keys
```

The Debian Desktop’s `id_ed25519.pub` was copied here.

Root does **NOT** have remote SSH access.

---

## 🚫 5. Disabled Access

| Access Type | Status | Reason |
|-------------|--------|--------|
| Root GUI login | ❌ | RBAC enforcement |
| Root SSH login | ❌ | `PermitRootLogin no` |
| SSH password login | ❌ | Key-only |
| External/WAN access to Proxmox | ❌ | Dual NAT protection (Router B → Router A) |
| PAM root GUI login | ❌ | Security best practice |

The hypervisor is isolated behind **two routers**, with no inbound exposure.

---

## 🌐 6. Security Architecture Benefits
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

This configuration mirrors real-world SRE/DevOps production clusters.



