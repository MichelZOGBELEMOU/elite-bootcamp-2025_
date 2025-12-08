# Homelab Network Plan
Elite DevOps & Automation Engineer Program (2025–2026)



This document defines the full IP addressing plan, CIDR layout, gateway/DHCP configuration, and VM mapping for my DevOps homelab. It is the reference for all networking-related labs in Phase 0 and the base for later CI/CD, Kubernetes, and cloud work.

---

## 1. Goals

- Provide a **clear, fixed IP scheme** for all physical nodes and VMs.
- Separate **home network** and **lab network** using a dual-router design.
- Standardize **hostnames and addresses** for databases, Kubernetes, monitoring, and Windows services.
- Avoid conflicts with consumer devices on the ISP router.

---

## 2. CIDR Overview

| Network | CIDR | Purpose | Router / GW |
|--------|------|---------|-------------|
| Home / ISP Network | `192.168.45.0/24` | Internet access, uplink for lab router & Proxmox vmbr0 | Router A (`192.168.45.1`) |
| Lab LAN | `10.10.0.0/24` | Internal homelab network for all VMs and control node | Router B (`10.10.0.1`) |

### 2.1 Address Allocation (10.10.0.0/24)

| Range | Usage |
|-------|-------|
| `10.10.0.1` | Lab Router (Router B gateway) |
| `10.10.0.2–10.10.0.49` | Static IPs for Proxmox, control node, core services, management interfaces |
| `10.10.0.50–10.10.0.199` | DHCP pool (dynamic lab clients, temporary VMs) |
| `10.10.0.200–10.10.0.254` | Reserved for future static or special-purpose services |

---

## 3. Routers & Gateways

### 3.1 Router A (ISP Router)

- Network: `192.168.45.0/24`
- Gateway: `192.168.45.1`
- NAT: **ON**
- DHCP: **ON**
- Role:
  - Provides Internet access to:
    - Fedora Test Node (on 192.168.45.x)
    - Proxmox vmbr0 (via `eno1`)
    - Router B WAN (`192.168.45.50`)

### 3.2 Router B (Lab Router)

- WAN: `192.168.45.50` (static on Router A network)
- LAN: `10.10.0.0/24`
- Gateway: `10.10.0.1`
- NAT: **ON**
- DHCP: **ON**, pool `10.10.0.50–10.10.0.199`
- UPnP Relay: **ON**
- DMZ: **OFF**
- Role:
  - Provides **isolated lab network** for all VMs and the Debian Control Node.
  - All lab traffic: `Lab → Router B → Router A → Internet`.

---

## 4. Proxmox Bridges & NIC Mapping

| Physical NIC | Proxmox Bridge | IP / Network | Function |
|--------------|----------------|-------------|----------|
| `eno1` | `vmbr0` | `192.168.45.x` (DHCP from Router A) | Uplink to ISP router, Internet access (NAT) |
| `eno2` | `vmbr1` | `10.10.0.2` (static) | Internal lab LAN, primary network for VMs |
| (optional future) `eno3` | `vmbr2` | TBD | Future monitoring / GitOps isolation |
| (optional future) `eno4` | `vmbr3` | TBD | Future dedicated storage / backup traffic |

Default VM network plan:

- **Management / Services** → `vmbr1` (`10.10.0.0/24`)
- **Internet access for VMs** → via Router B (NAT) → Router A (NAT)

---

## 5. Static IP Assignments

### 5.1 Physical & Core Management

| Host | Role | Interface / Bridge | IP | Notes |
|------|------|--------------------|----|------|
| Router B | Lab gateway | LAN | `10.10.0.1` | Default gateway for all lab hosts |
| Proxmox R610 | Hypervisor | `eno2` → `vmbr1` | `10.10.0.2` | Main Proxmox management on lab LAN |
| Debian Desktop | Control Node | `eth0` | `10.10.0.10` | Main DevOps workstation (Ansible, Terraform, CI/CD) |
| iDRAC | Out-of-band management | `mgmt0` | `10.10.0.34` | Remote management for R610 |
| Fedora Notebook | Test Node | `wlan0` | `192.168.45.x` (DHCP) | External test node on home LAN |

> All core lab services (DNS, databases, Kubernetes, monitoring) must live on `10.10.0.0/24` and be reachable from `10.10.0.10`.

---

## 6. Planned VM IP & Hostname Mapping

> Exact addresses can be adjusted later, but this plan ensures there is **no overlap** and roles are clear.

### 6.1 Infrastructure Services

| Hostname | Role | Bridge | Planned IP | Notes |
|----------|------|--------|------------|-------|
| `dns01.lab.local` | dnsmasq DNS + DHCP | `vmbr1` | `10.10.0.20` | Authoritative for `lab.local`, DNS resolver for lab |
| `mon01.lab.local` | Prometheus + Grafana + Loki | `vmbr1` | `10.10.0.21` | Monitoring stack for all nodes |
| `log01.lab.local` | Central log aggregation (optional if separate from mon01) | `vmbr1` | `10.10.0.22` | Loki / syslog receiver |

### 6.2 Database VMs

| Hostname | DB Type | Bridge | Planned IP | Notes |
|----------|---------|--------|------------|-------|
| `pg01.lab.local` | PostgreSQL | `vmbr1` | `10.10.0.30` | SQL labs, app backends |
| `mongo01.lab.local` | MongoDB | `vmbr1` | `10.10.0.31` | NoSQL labs |
| `redis01.lab.local` | Redis | `vmbr1` | `10.10.0.32` | Caching, sessions, pub/sub |

### 6.3 Kubernetes (k3s) Nodes

| Hostname | Role | Bridge | Planned IP | Notes |
|----------|------|--------|------------|-------|
| `k3s-master01.lab.local` | k3s Server (Master) | `vmbr1` | `10.10.0.40` | Control plane, API server |
| `k3s-worker01.lab.local` | k3s Agent (Worker) | `vmbr1` | `10.10.0.41` | Runs workloads, HPA/Canary tests |

### 6.4 CI/CD & Application Servers

| Hostname | Role | Bridge | Planned IP | Notes |
|----------|------|--------|------------|-------|
| `ci01.lab.local` | Jenkins / CI server | `vmbr1` | `10.10.0.50` | Pipelines for Docker & k8s |
| `app01.lab.local` | FastAPI + Gunicorn + NGINX | `vmbr1` | `10.10.0.51` | Web service for Week 5 labs |
| `registry01.lab.local` | Local Docker registry | `vmbr1` | `10.10.0.52` | Stores container images for CI/CD |

### 6.5 Windows VMs

| Hostname | Role | Bridge | Planned IP | Notes |
|----------|------|--------|------------|-------|
| `win-srv01.lab.local` | Windows Server (IIS + AD/PS labs) | `vmbr1` | `10.10.0.60` | HTTPS + PowerShell automation |
| `win10-client.lab.local` | Windows 10 Client (VM on Debian Desktop) | Bridged to lab LAN if needed | `10.10.0.x` | Cross-platform testing, RDP/SSH |
| `win11-client.lab.local` | Windows 11 Client (VM on Debian Desktop) | Bridged to lab LAN if needed | `10.10.0.x` | Cross-platform testing, RDP/SSH |

---

## 7. Hostname & DNS Conventions

- Internal lab domain: `lab.local`
- Basic pattern:  
  - `<role><index>.lab.local` (e.g., `pg01.lab.local`, `k3s-master01.lab.local`)
- All static hosts should have **A records** in `dnsmasq`:
  - Example:
    ```ini
    address=/pg01.lab.local/10.10.0.30
    address=/k3s-master01.lab.local/10.10.0.40
    ```

---

## 8. Routing & Security Notes

- **Outbound traffic**:  
  Lab hosts → Router B (`10.10.0.1`) → Router A (`192.168.45.1`) → Internet.
- **Inbound traffic (from Internet)**:  
  Blocked by default (double NAT + no port forwarding).
- For cloud labs (AWS, etc.), connections are **initiated from inside** the lab.
- Port forwarding can be temporarily enabled for specific demos, but must be:
  - Documented  
  - Time-limited  
  - Removed after testing

---

## 9. Validation Checklist (Week 0–1)

- [ ] Proxmox reachable at `https://10.10.0.2:8006` from `10.10.0.10`
- [ ] Debian Control Node (`10.10.0.10`) can:
  - [ ] Ping Router B (`10.10.0.1`)
  - [ ] Ping Proxmox (`10.10.0.2`)
  - [ ] Ping `dns01.lab.local`
- [ ] `lab.local` names resolve correctly (e.g., `ping pg01.lab.local`)
- [ ] Outbound Internet works from at least:
  - [ ] Debian Control Node
  - [ ] One VM on `vmbr1`
- [ ] No unexpected devices in `10.10.0.0/24` outside defined ranges

---

This plan remains stable for all phases of the roadmap. Any future changes must be reflected here and in the topology diagrams before new labs are deployed.