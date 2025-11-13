# Elite DevOps & Automation Engineer Bootcamp ( 2025-2026)
Author: **Michel Zogbelemou**

Mentor: **ChatGPT - Elite DevOps Career Mentor**

This repository documents my complete 12 weeks Devops & Automation Engineer,executed fully on my personal homelab. It includes hands-on labs, network configuration, CI/CD pipelines, Kubernetes deployments, cloud automation, observability, SRE, and portfolio preparation.

---

## 🚀 Program Overview
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
- Debian & Fedora servers (CI/CD agents, app servers)
- PostgreSQL (Debian), MongoDB (Ubuntu), Redis (Alpine)
- k3s Kubernetes: 1 master + 1 worker
- Windows Server 2019/2022 (IIS + PowerShell)
- Monitoring Stack: Prometheus + Grafana + Loki
- Windows 10 VM (on Debian Desktop)
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
- SLOs, error budgets, runbooks  
- Argo CD, Kyverno, OpenTelemetry  
- eBPF analysis  
- CI-green portfolio assembly  

Deliverables: `production-platform/`, `argo-gitops/`, `Portfolio_Summary.pdf`

---

### **Phase 5 — AI-Driven DevOps (Optional)**
- AIOps predictive incident analysis  
- AI-assisted Terraform/Kubernetes  
- AI pipeline risk scoring  

Deliverables: `aiops-labs/`

---

## 📁 Repository Structure

elite-bootcamp/
│
├── homelab/
├── network-plan.md
├── dnsmasq.conf
├── subnet-exercise.md
│
├── linux-fundamentals-labs/
├── fedora-labs/
├── py-cli-tool/
├── yaml-labs/
│
├── py-sysinfo-service/
├── service-cicd/
├── db-labs/
├── nosql-labs/
├── k8s-service-ops/
├── helm-chart/
│
├── aws-tf-service/
├── observability-and-drills/
│
├── production-platform/
├── argo-gitops/
│
└── Portfolio_Summary.pdf

---

## ✅ Success Criteria
- Functional Proxmox lab (10.10.0.x)
- SQL + NoSQL labs completed
- End-to-end CI/CD and k3s deployment
- AWS/Terraform automation
- Observability dashboards + security scans
- Portfolio ready for DevOps/SRE remote roles
