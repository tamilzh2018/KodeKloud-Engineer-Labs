# Day 7: Linux SSH Automation

## Task Overview

Configure password-less SSH authentication from the jump host to all application servers in the Stratos Datacenter. This enables automated script execution, deployment workflows, and seamless system administration without manual password entry.

**Task Requirements:**
- Generate SSH key pair on jump host (thor user)
- Distribute public key to all app servers
- Configure password-less access for respective sudo users
- Test automated SSH access without passwords

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Generate SSH key pair on the jump host

```sh
ssh-keygen -t rsa -b 2048
```

On the jump host as the thor user, generate an RSA SSH key pair with 2048-bit encryption. The `ssh-keygen` command creates two files: a private key (`~/.ssh/id_rsa`) that must remain secret and secure on the jump host, and a public key (`~/.ssh/id_rsa.pub`) that will be distributed to remote servers. When prompted for a file location, press Enter to accept the default location (`/home/thor/.ssh/id_rsa`). When asked for a passphrase, you can press Enter twice to create a key without a passphrase (required for unattended automation) or enter a passphrase for additional security (though this requires using ssh-agent for automation).

**Step 2:** Display the generated public key

```sh
cat ~/.ssh/id_rsa.pub
```

View the contents of the public key file that was just generated. The output will be a single long line starting with "ssh-rsa" followed by the encoded key data and ending with a comment (typically user@hostname). Copy this entire line to your clipboard as you'll need to add it to each application server. The public key is safe to share and distribute - it cannot be used to compromise security without the corresponding private key.

**Step 3:** Connect to the first application server

```sh
ssh tony@app-server-1
```

Establish an SSH connection to the first application server using the appropriate sudo user account. For this task, you'll use different sudo users for different servers (tony for app-server-1, steve for app-server-2, banner for app-server-3, etc., as specified in your lab environment). You'll be prompted for the password this time, but after configuration, future connections will be password-less.

**Step 4:** Create the SSH directory on the application server

```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Create the `.ssh` directory in the user's home directory if it doesn't already exist. The `-p` flag prevents errors if the directory already exists. Immediately set the permissions to `700` (rwx------), which gives the owner full access while preventing group and other users from accessing the directory. These restrictive permissions are required by SSH for security - SSH will refuse to use the directory if permissions are too open.

**Step 5:** Add the public key to authorized_keys file

```sh
vi ~/.ssh/authorized_keys
```

Open the `authorized_keys` file for editing (creating it if it doesn't exist). Paste the public key you copied earlier from the jump host into this file. Each public key should be on its own line. If multiple users or systems need access, each of their public keys can be added as separate lines. In vi, press `i` to enter insert mode, paste the key, press Esc, then type `:wq` to save and exit. Alternatively, you can use nano or echo commands to add the key.

**Step 6:** Set correct permissions on authorized_keys file

```sh
chmod 600 ~/.ssh/authorized_keys
```

Set the authorized_keys file permissions to `600` (rw-------), giving the owner read and write access while preventing all access by group and other users. SSH requires these restrictive permissions for security reasons and will refuse to use the file if permissions are too permissive. This ensures only the account owner can modify which keys are authorized for access.

**Step 7:** Exit from the application server

```sh
exit
```

Return to the jump host by exiting your SSH session to the application server. You're now ready to test the password-less authentication from the jump host.

**Step 8:** Test password-less SSH access

```sh
ssh tony@app-server-1
```

Attempt to connect to the application server again from the jump host. This time, you should be logged in immediately without being prompted for a password. SSH uses the private key on the jump host to authenticate against the public key stored on the application server. If you're still prompted for a password, review the file permissions, file locations, and ensure the public key was copied correctly.

**Step 9:** Repeat for all application servers

Repeat steps 3-8 for each application server in your infrastructure, using the appropriate sudo user for each server (e.g., steve@app-server-2, banner@app-server-3). This ensures the thor user on the jump host has password-less access to all application servers.

---

## Automated Approach (Recommended)

**Alternative Method:** Use ssh-copy-id for automated key distribution

```sh
ssh-copy-id tony@app-server-1
```

The `ssh-copy-id` utility automates the entire process of distributing your public key to remote servers. It handles creating the `.ssh` directory if needed, appending your public key to the `authorized_keys` file, and setting proper permissions on both the directory and file. You'll be prompted for the password once during this process, after which password-less access will be configured. This is the preferred method as it eliminates manual steps and potential permission errors.

**For multiple servers:**

```sh
# Copy key to all app servers
ssh-copy-id tony@app-server-1
ssh-copy-id steve@app-server-2
ssh-copy-id banner@app-server-3
```

Run `ssh-copy-id` for each application server with the respective sudo user account. This quickly establishes password-less access across your entire infrastructure, enabling automation workflows and reducing operational overhead.

---

## Understanding SSH Key Authentication

**How SSH Key Authentication Works:**

1. **Key Generation**: A public/private key pair is created on the client (jump host)
2. **Key Distribution**: The public key is added to `~/.ssh/authorized_keys` on the server
3. **Authentication**: When connecting, the server sends a challenge encrypted with the public key
4. **Verification**: The client decrypts the challenge with its private key and responds
5. **Access Granted**: If the response is correct, authentication succeeds without a password

**SSH Key Types:**

- **RSA**: Traditional algorithm, use 2048-bit minimum (4096-bit for higher security)
- **Ed25519**: Modern algorithm, faster and more secure, fixed 256-bit key size
- **ECDSA**: Elliptic curve algorithm, good performance but RSA/Ed25519 preferred
- **DSA**: Deprecated, do not use (considered insecure)

**Recommended key generation:**

```sh
# RSA 4096-bit (widely compatible)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Ed25519 (modern, recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**SSH Directory Structure:**

```
~/.ssh/
├── id_rsa              # Private key (keep secret, never share)
├── id_rsa.pub          # Public key (safe to distribute)
├── authorized_keys     # Public keys allowed to login as this user
├── known_hosts         # Fingerprints of servers you've connected to
└── config             # SSH client configuration (optional)
```

**Required File Permissions:**

```sh
# SSH directory
chmod 700 ~/.ssh

# Private key
chmod 600 ~/.ssh/id_rsa

# Public key
chmod 644 ~/.ssh/id_rsa.pub

# Authorized keys
chmod 600 ~/.ssh/authorized_keys
```

**SSH Configuration for Automation:**

Create `~/.ssh/config` to simplify connections:

```
Host app1
    HostName app-server-1.example.com
    User tony
    IdentityFile ~/.ssh/id_rsa

Host app2
    HostName app-server-2.example.com
    User steve
    IdentityFile ~/.ssh/id_rsa

Host app*
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
```

Now you can connect with just: `ssh app1`

**Security Best Practices:**

- **Passphrase Protection**: Add a passphrase to private keys for additional security
- **SSH Agent**: Use `ssh-agent` to cache passphrase for automated workflows
- **Key Rotation**: Regularly rotate SSH keys (annually recommended)
- **Disable Password Auth**: Once keys are configured, disable password authentication in `/etc/ssh/sshd_config`:
  ```
  PasswordAuthentication no
  PubkeyAuthentication yes
  ```
- **Monitor Access**: Regularly review `~/.ssh/authorized_keys` files
- **Separate Keys**: Use different keys for different purposes/environments

**Troubleshooting SSH Key Authentication:**

```sh
# Test SSH connection with verbose output
ssh -v tony@app-server-1

# Check SSH permissions (common issue)
ls -la ~/.ssh/

# Verify key is being offered
ssh -v tony@app-server-1 2>&1 | grep "Offering public key"

# Check server logs (on the server)
sudo tail -f /var/log/auth.log

# Test key manually
ssh-keygen -y -f ~/.ssh/id_rsa
```

**Common Issues:**

- **Wrong permissions**: SSH is strict about file/directory permissions
- **Incorrect key format**: Ensure complete public key is copied (single line)
- **SELinux restrictions**: May need to run `restorecon -R ~/.ssh` on RHEL/CentOS
- **Home directory permissions**: Home directory should not be world-writable

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 6](day-06.md) | [Day 8 →](../week-02/day-08.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
