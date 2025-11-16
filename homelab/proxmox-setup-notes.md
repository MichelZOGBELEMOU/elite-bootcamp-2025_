# Proxmox Setup Notes (Concise & Recruiter-Friendly)
This document summarizes how Proxmox VE 8 is configured on my Dell R610 to support the DevOps homelab.  
It explains the network layout, bridges, VM connectivity, and storage in a clean and practical way.

---

## 1. Host Summary
- **Server:** Dell PowerEdge R610  
- **Hypervisor:** Proxmox VE 8  
- **Specs:** Dual Xeon, 64 GB RAM  
- **Disks:**  
  - 223 GB SSD (Proxmox + VM storage)  
  - 500 GB HDD (planned)  
- **Controller:** Dell PERC H700 (RAID0 for now)

Sufficient for multi-VM DevOps labs (CI/CD, Docker, k3s, databases, monitoring).

---

## 2. Network Overview
The homelab uses a dual-router model:

- **Router A (192.168.45.0/24)** → Internet  
- **Router B (10.10.0.0/24)** → Internal lab network  

Proxmox participates in both networks using two NICs.

### NIC Mapping
| NIC | Purpose | Connected To |
|-----|----------|--------------|
| **eno1** | Internet access | Router A |
| **eno2** | Lab LAN | Router B |
| **mgmt0** | iDRAC | 10.10.0.34 |

---

## 3. Proxmox Bridges (Core Concept)
Proxmox uses Linux bridges like virtual switches.

### vmbr0 — External / Internet
- Uses NIC: **eno1**  
- Gets IP from Router A (DHCP)  
- Used by Proxmox to reach the Internet  
- **VMs do not use vmbr0**

iface vmbr0 inet dhcp


### vmbr1 — Internal LAN (Main VM Network)
- Uses NIC: **eno2**  
- Static IP: **10.10.0.2/24**  
- No gateway (important for routing)  
- All VM communication happens here  

iface vmbr1 inet static
address 10.10.0.2/24

---

## 4. Routing (How Everything Reaches the Internet)
Proxmox itself goes:

Proxmox → vmbr0 → Router A → Internet


VMs go through **double NAT**:

VM → Router B → Router A → Internet

This setup is safe, isolated, and perfect for lab work.

---

## 5. VM Network Settings (Simple & Standardized)
Every VM on Proxmox uses:

| Setting | Value |
|--------|--------|
| Bridge | **vmbr1** |
| Network | 10.10.0.0/24 |
| Gateway | 10.10.0.1 (Router B) |
| DNS | 10.10.0.20 (dnsmasq) |
| Domain | lab.local |

This makes all services predictable and avoids IP conflicts.

---

## 6. Static IP Plan (Core Services)
A shorter list of the most important VMs:

| VM / Role | IP |
|-----------|----|
| dns01 (DNS/DHCP) | 10.10.0.20 |
| mon01 (Monitoring) | 10.10.0.21 |
| pg01 (PostgreSQL) | 10.10.0.30 |
| mongo01 | 10.10.0.31 |
| redis01 | 10.10.0.32 |
| k3s-master01 | 10.10.0.40 |
| k3s-worker01 | 10.10.0.41 |
| jenkins | 10.10.0.50 |
| app01 | 10.10.0.51 |
| registry01 | 10.10.0.52 |
| win-srv01 | 10.10.0.60 |


---

## 7. Storage Overview (Simple)
Proxmox provides two storage pools:

- **local** → `/var/lib/vz` (ISO, templates, backups)  
- **local-lvm** → LVM-thin pool for VM disks  

Future:
- Add 500 GB HDD for backups / secondary VM disks

This covers all needs for the 12-week DevOps roadmap.

---

## 8. Quick Validation Checklist

- vmbr0 has DHCP IP from Router A  
- vmbr1 is `10.10.0.2`  
- Only vmbr0 has a gateway  
- UI reachable at `https://10.10.0.2:8006`

**VM networking OK if:**
- VM can ping `10.10.0.1`  
- VM can reach Internet (`ping 8.8.8.8`)  
- VM resolves `lab.local` names  

---

## Final Summary
This Proxmox configuration mirrors a real-world infrastructure:  
- clean separation of Internet and lab traffic  
- stable VM networking  
- predictable addressing  
- ready for Kubernetes, CI/CD, databases, and observability  

It is simple, reliable, and perfect for a professional DevOps homelab.