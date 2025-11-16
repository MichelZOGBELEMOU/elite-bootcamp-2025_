# Subnetting Exercises — Homelab Network  
This document contains explanations and practice problems to help reinforce subnetting skills used in the 10.10.0.0/24 lab network.

---

## 1. Core Concepts (Short & Clear)

### What is a subnet?
A subnet divides an IP network into smaller, organized segments.

### CIDR Notation
CIDR: `10.10.0.0/24`

- **10.10.0.0** → network address  
- **/24** → subnet mask (255.255.255.0)  
- 24 bits for network, 8 bits for hosts  

### Host Capacity
`/24` supports:
- **256 total addresses**
- **254 usable hosts**
- 1 network address (`10.10.0.0`)
- 1 broadcast (`10.10.0.255`)

---

## 2. Homelab Subnet Overview

10.10.0.0/24
Assignments:
- **10.10.0.1** → Router B (gateway)  
- **10.10.0.2** → Proxmox vmbr1  
- **10.10.0.10** → Debian Control Node  
- **10.10.0.20–60** → Static IPs for DNS, DB, CI/CD, K3s  
- **10.10.0.50–199** → DHCP Pool  
- **10.10.0.200–254** → Reserved  

---

## 3. Subnetting Examples

### Example 1 — Find network address
**IP:** 10.10.0.51  
**CIDR:** /24  

Network = **10.10.0.0**

### Example 2 — Find broadcast
**Network:** 10.10.0.0/24  
Broadcast = **10.10.0.255**

### Example 3 — Usable range
Usable hosts = **10.10.0.1 → 10.10.0.254**

---

## 4. Practice Exercises

### **Exercise 3 — Create Sub-Subnets (Optional Challenge)**  
Split `10.10.0.0/24` into two equal-sized networks.

1. What would the new subnets be?  10.10.0.0/25 - 10.10.0.128
2. How many hosts per subnet? 126 hosts