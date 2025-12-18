# SELinux Management (semanage, restorecon, setseboo)
Author: **Michel Zogbelemou**  
Mentor: **ChatGPT — Elite DevOps Career Mentor**

## Objectives

This day goal is to learn how to *manage* SELinux labels and policies.

- Understand permanent SELinux rules using `semanage fcontext`
- Correct mislabeled files and directories using `restorecon`
- Enable/disable SELinux policy toggles using `setsebool`
- Apply SELinux concepts to a real service (Apache httpd)
- Validate correct labeling through browsers, journald, and AVC logs

By the end of this lab, we will know how RHEL-based production systems enforce web security using SELinux Mandatory Access Control (MAC).

---

## Deep Explanation

### 1. SELinux Enforcement Model
SELinux enforces **type enforcement**
- Every file has a **label**: `user:role:type:level`
- Every process has a **domain** (type)
- Policies govern which domains may interact with which types

For Apache:

- Apache runs in domain: **httpd_t**
- It can only read/write file types explicitly allowed by SELinux policies

This means:
Even if filesystem permissions (chmod) allow access, **SELinux may still deny**
This is crucial for defense-in-depth.

---

### 2. Default Labels vs Custom Directories
- `/var/www/html` --> `httpd_sys_content_t`
- `/var/www/cgi-bin` --> `httpd_sys_script_exec_t`

But custom paths like `/opt/myapp` or `/srv/app` usually receive:

unconfined_u:object_r:var_t:s0

`var_t` is not permitted for Apache --> results in **403 Forbidden** or AVC denials.

To make a custom directory accessible, we must:

1. Assign a correct SELinux **type**
2. Ensure this rule is **persistent**
3. Apply the label on disk

### 3. semanage fcontext (Persistent Rules)

`semanage fcontext` modifies the SELinux **file context database** not the files themselves.

Format:
```bash
semanage fcontext -a -t <type> "<path>(/.*)?"
```
Example for Apache read/write content:

```bash
semanage fcontext -a -t httpd_sys_rw_content_t "/srv/app(/.*)?"
```

This stores a permanent rule inside SELinux policy.

---

### 4. restorecon (Applying the correct lable)

`restorecon ` **relabels** files based on SELinux rules:

```bash
restorecon -Rv /srv/app
```
This updates file labels to match what `semanage fcontext` describes.

---

### 5. SELinux Booleans (Runtime Policy Toggles)

`setsebool` controls optional policy behavior:

```bash
setsebool -P httpd_enable_homedirs on
```
Common httpd booleans

- `httpd_can_network_connect`
- `httpd_enable_homedirs`
- `httpd_can_sendmail`
- `httpd_read_user_content`

Booleans allow quick, controlled exceptions without modifying policy files.

## Hands-on Lab
check the Screenshoots