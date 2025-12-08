# Elite DevOps & Automation Engineer Bootcamp ( 2025-2026)
Author: **Michel Zogbelemou**

Mentor: **ChatGPT - Elite DevOps Career Mentor**

This repository documents my complete 12 weeks Devops & Automation Engineer,executed fully on my personal homelab. It includes hands-on labs, network configuration, CI/CD pipelines, Kubernetes deployments, cloud automation, observability, SRE, and portfolio preparation.

---
## Why This Project Exists
Modern DevOps roles require ** hands-on skills**, not just theory.
This project is my end-to-end journey to build a **real hybrid infrastructure from scratch**, following industry best practices and the Elite DevOps Roadmap.

 **Goal:**
Become a job-ready DevOps/SRE engineer capable of managing real production infrastructure.

---


##  Program Overview
This bootcamp follows the **Elite DevOps 2026 Roadmap (AI-Integrated Edition)**:

1. **Phase 0 - Homelab & Networking Foundations**
2. **Phase 1 - Linux & Automation Core**
3. **Phase 2 - Containers → CI/CD → SQL + NoSQL → Kubernetes**
4. **Phase 3 - Cloud + Observability + Security**
5. **Phase 4 - SRE · GitOps · Portfolio**
6. **Phase 5- AI-Driven DevOps**

Each phase includes theory, hands-on labs, validation steps, diagrams, and deliverables.

___

## 🏠 Homelab Infrastructure

### **Physical Nodes**
| Node | OS | Purpose |
|------|----|----------|
| **Debian 12 Desktop** | Main Control Node | CI/CD, Terraform, automation, monitoring, GitHub |
| **Fedora 43 Notebook** | Test Node | RHEL labs: SELinux, firewalld, Ansible |
| **Dell PowerEdge R610 — Proxmox VE 8** | Hypervisor | Hosts all VMs, vmbr0/vmbr1 networking |

### **Virtual Machines (Proxmox)**
- Debian , RockyLinux, Fedora (Linux) servers (CI/CD agents, app servers)
- PostgreSQL (Debian), MongoDB (Ubuntu), Redis (Alpine)
- k3s Kubernetes: 1 master + 1 worker
- Windows Server 2022 (IIS + PowerShell)
- Monitoring Stack: Prometheus + Grafana + Loki
- Windows 11 VM (on Debian Desktop)

### **Network Architecture**
**Dual-router setup:**
- **Router A (ISP):** `192.168.45.0/24`  
- **Router B (Lab Router):** `10.10.0.0/24` (NAT + DHCP + UPnP Relay)

**Key IPs**
- Proxmox eno1 → vmbr0 → `192.168.45.x`  
- Proxmox eno2 → vmbr1 → `10.10.0.2`  
- Debian Control Node → `10.10.0.10`  
- iDRAC → `10.10.0.34`

Internal DNS managed with **dnsmasq**.  
Internal domain: **lab.local**

---
##  Weekly Phase Breakdown

### **Phase 0 — Homelab & Networking (Weeks 0–1)**
- Install Proxmox 8  
- Configure vmbr0 (NAT) + vmbr1 (LAN)  
- Static IPs on all lab VMs  
- dnsmasq DNS/DHCP  
- Network validation (ping, curl, ssh)

Deliverables:  
`homelab/README.md`, `network-plan.md`, `dnsmasq.conf`, `subnet-exercise.md`

---

### **Phase 1 — Linux & Automation Core (Weeks 2–4)**
- systemd, journald, logrotate, PAM  
- SELinux, firewalld, package managers  
- Python CLI automation (argparse, logging, pytest)  
- YAML, PyYAML, GitHub Actions 

Deliverables:  
`linux-fundamentals-labs/`, `fedora-labs/`, `py-cli-tool/`, `yaml-labs/`

---

### **Phase 2 — Containers, CI/CD, Databases, Kubernetes (Weeks 5–8)**

#### Week 5 — FastAPI + NGINX (TLS) + IIS HTTPS  
Deliverable: `py-sysinfo-service/`

#### Week 6 — Docker, Compose, Jenkins CI  
Deliverable: `service-cicd/`

#### Week 6.5 — SQL + NoSQL Labs  
- PostgreSQL CRUD, backups, roles  
- MongoDB CRUD, indexes  
- Redis caching, pub/sub, persistence  
Deliverables: `db-labs/`, `nosql-labs/`

#### Week 7 — Kubernetes (k3s)  
- Helm charts  
- Ingress TLS  
- HPA + Canary  
- NetworkPolicies  
Deliverables: `k8s-service-ops/`, `helm-chart/`

---

### **Phase 3 — Cloud + Observability + Security (Weeks 9–10)**
- Terraform AWS (VPC, EC2, ECR, IAM)  
- Prometheus, Grafana, Loki  
- Trivy, Cosign, RBAC, firewall audit  

Deliverables: `aws-tf-service/`, `observability-and-drills/`

---

### **Phase 4 — SRE · GitOps · Portfolio (Weeks 11–12)**
- SLOs, error budgets  
- Runbooks & incident response  
- Argo CD GitOps  
- Kyverno policies  
- OpenTelemetry + eBPF  
- HA PostgreSQL/Mongo/Redis  
- Portfolio creation  

Deliverables: `production-platform/`, `argo-gitops/`, `Portfolio_Summary.pdf`

---

### **Phase 5 — AI-Driven DevOps (Optional)**
- AIOps predictive incident analysis  
- AI-assisted Terraform/Kubernetes  
- AI pipeline risk scoring  

Deliverables: `aiops-labs/`

---

## 📁 Repository Structure

```text

elite-bootcamp/
│
├── README.md                     # Project overview (root)
│
├── homelab/
│   ├── README.md
│   ├── dnsmasq.conf
│   ├── network-plan.md
│   ├── proxmox-access.md
│   ├── proxmox-setup-notes.md
│   ├── ssh-hardening.md
│   ├── subnet-exercises.md
│   └── screenshots/
│       ├── networking/
│       ├── proxmox/
│       ├── dns/
│       └── ssh/
│
├── linux-fundamentals-labs/
│   ├── README.md
│   └── screenshots/
│
├── fedora-labs/
│   ├── README.md
│   └── screenshots/
│
├── py-cli-tool/
│   ├── README.md
│   └── screenshots/
│
├── yaml-labs/
│   ├── README.md
│   └── screenshots/
│
├── py-sysinfo-service/
│   ├── README.md
│   └── screenshots/
│
├── service-cicd/
│   ├── README.md
│   ├── docker/
│   ├── jenkins/
│   ├── github-actions/
│   └── screenshots/
│
├── db-labs/
│   ├── postgres/
│   ├── mongodb/
│   ├── redis/
│   └── screenshots/
│
├── nosql-labs/
│   ├── mongodb/
│   ├── redis/
│   └── screenshots/
│
├── k8s-service-ops/
│   ├── manifests/
│   ├── deployments/
│   ├── ingress/
│   ├── tls/
│   └── screenshots/
│
├── helm-chart/
│   ├── templates/
│   ├── charts/
│   └── screenshots/
│
├── aws-tf-service/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   ├── cloud-diagrams/
│   └── screenshots/
│
├── observability-and-drills/
│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   ├── alerting/
│   └── screenshots/
│
├── production-platform/
│   ├── architecture/
│   ├── manifests/
│   └── screenshots/
│
├── argo-gitops/
│   ├── applications/
│   ├── policies/
│   ├── sources/
│   └── screenshots/
│
├── docs/
│   ├── diagrams/
│   ├── screenshots/
│   │   └── portfolio/
│   ├── weekly-progress/
│   ├── roadmap-v6.1.md
│   └── homelab-architecture.md
│
└── Portfolio_Summary.pdf

```
---

# ✅ Success Criteria  
✔ Fully functional Proxmox homelab  
✔ End-to-end CI/CD pipelines  
✔ SQL + NoSQL labs completed  
✔ Kubernetes (k3s) deployments working  
✔ AWS Terraform automation  
✔ Observability dashboards  
✔ Security practices (Trivy, Cosign, RBAC)  
✔ GitOps with Argo CD  
✔ Final portfolio ready for remote DevOps/SRE roles 