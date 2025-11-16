# Homelab — Elite DevOps & Automation Engineer Program (2025–2026)

**Author: Michel Zogbelemou**  
**Mentor: ChatGPT — Elite DevOps Career Mentor**

This directory documents the full technical setup of my DevOps homelab.  
It serves as the foundation for all networking, virtualization, automation, CI/CD, container, Kubernetes, and cloud labs completed throughout the Elite 12-Week DevOps & Automation Engineer Roadmap (SQL + NoSQL Integrated Edition, v6).


---

# 🖥️ 1. Homelab Overview

My homelab is built to simulate a real-world hybrid environment with:

- A dedicated hypervisor host (Proxmox VE 8)
- A Debian 12 Control Node for automation, CI/CD, and Terraform
- A Fedora 43 Test Node for RHEL-based exercises
- A dual-router architecture separating WAN and lab LAN
- Internal DNS/DHCP with dnsmasq
- Multiple VMs for databases, Kubernetes, monitoring, and Windows-based DevOps tasks

This architecture stays consistent across all phases of the roadmap.

---

# 🧱 2. Physical Nodes

| Role | Hardware | OS | Purpose |
|------|----------|----|---------|
| **Control Node** | Samsung Desktop | Debian 12 | Main automation workstation: Python, CI/CD, Terraform, monitoring |
| **Test Node** | LG Gram Notebook | Fedora 43 | RHEL-family labs: SELinux, firewalld, DNF, Ansible |
| **Hypervisor** | Dell PowerEdge R610 | Proxmox VE 8 | Runs all VMs, dual-bridge networking (vmbr0/vmbr1) |

---

# 🖧 3. Network Architecture (Dual-Router)

The homelab uses a dual-router design to isolate lab traffic from home internet while allowing outbound access.

### **Router A (ISP Router)**
- `192.168.45.0/24`
- Gateway: `192.168.45.1`
- NAT: ON  
- DHCP: ON

### **Router B (Lab Router)**
- WAN: `192.168.45.50` (static)
- LAN: `10.10.0.0/24`  
- Gateway: `10.10.0.1`
- DHCP: `10.10.0.50–199`
- NAT: ON  
- DHCP: ON

---

# 🔌 4. Proxmox Network Bridges

| Interface | Bridge | IP | Role |
|-----------|--------|----|------|
| `eno1` | `vmbr0` | `192.168.45.x` | Outbound Internet via Router A (NAT) |
| `eno2` | `vmbr1` | `10.10.0.2` | Internal LAN for VMs (Router B) |

---

# 🖥️ 5. Virtual Machines

## **5.1 Application & CI/CD Servers**
- Debian 12 / Fedora
- GitHub Actions runners  
- Jenkins agents  
- FastAPI + NGINX deployments

## **5.2 Databases**
- PostgreSQL (Debian)  
- MongoDB (Ubuntu)  
- Redis (Alpine)  

Includes:
- CRUD labs  
- Backups  
- Monitoring  
- Security hardening  

## **5.3 Kubernetes Cluster (k3s)**
- 1 master (Alpine/Ubuntu Minimal)
- 1 worker  
- Helm charts, TLS, HPA, Canary, NetworkPolicies

## **5.4 Monitoring Stack**
- Prometheus  
- Grafana  
- Loki  
- Node Exporters

## **5.5 Windows Systems**
- **Windows Server 2019/2022** for IIS HTTPS + PowerShell automation  
- **Windows 10 VM** on Debian Desktop for cross-platform testing
- **Windows 11 VM** on Debian Desktop for cross-platform testing

---

# 🌐 6. Internal DNS & DHCP (dnsmasq)

The lab uses a private internal DNS domain:
lab.local


Responsibilities of dnsmasq:
- Static DNS entries for all VMs  
- DHCP for 10.10.0.x dynamic hosts  
- DNS caching for faster lab usage  

---

# 🔍 7. Connectivity & Validation (Week 0 Deliverables)

### Verified:
- Proxmox reachable from Debian Control Node  
- All VMs receive static IPs  
- `lab.local` resolves internally  
- SSH, ping, curl fully functional  
- NAT working for all outbound traffic  
- no inbound exposure (double NAT)  

---

# 📁 8. Repository Deliverables (Homelab Section)

This folder contains:

```text
homelab/
├── README.md                 # Main homelab documentation (architecture, goals, validation)
├── network-plan.md           # CIDR ranges, gateways, bridges, and VM IP mapping
├── dnsmasq.conf              # DNS + DHCP configuration for lab.local
├── subnet-exercise.md        # Manual subnetting practice (CIDR, masks, calculations)
├── topology-diagram.png      # Visual diagram of dual-router + vmbr0/vmbr1 architecture
└── proxmox-setup-notes.md    # Notes on NIC mapping, bridge setup, and VM networking
```



---

# 🧩 9. Purpose of the Homelab
This homelab enables all future training in:

- Linux fundamentals  
- Automation (Python + Bash + Ansible)  
- CI/CD pipelines  
- Docker & containerization  
- SQL + NoSQL databases  
- Kubernetes (k3s)  
- Terraform + AWS  
- Observability & security  
- SRE + GitOps  
- AI-assisted DevOps (Phase 5)

---

# 🏁 Final Notes
This homelab is intentionally designed to mirror real-world enterprise hybrid infrastructure.  
It demonstrates production-level thinking in network segmentation, virtualization, automation, and system design — all essential skills for DevOps/SRE roles in 2026.
