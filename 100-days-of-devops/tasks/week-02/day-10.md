# Day 10: Create a BASH Script

## Task Overview

The production support team of xFusionCorp Industries is working on developing bash scripts to automate different day-to-day tasks. One requirement is to create a bash script for taking website backups. They have a static website running on App Server 3 in Stratos Datacenter, and they need to create a bash script named `beta_backup.sh` to accomplish the following tasks:

**Objectives:**
1. Create a zip archive named `xfusioncorp_beta.zip` of the `/var/www/html/beta` directory
2. Save the archive in `/backup/` on App Server 3 (temporary storage, cleaned weekly)
3. Copy the created archive to the Nautilus Backup Server in the `/backup/` location
4. Ensure the script doesn't ask for a password when copying the archive file
5. The respective server user must be able to run the script

**Script Requirements:**
- Script location: `/scripts/beta_backup.sh` on App Server 3
- Must be executable by the server user
- Automated execution without user intervention

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Setup SSH Key-Based Authentication

Configure passwordless SSH authentication between App Server 3 and the Backup Server.

**On App Server 3, generate an SSH key pair:**
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

**Explanation:** This command generates a 4096-bit RSA key pair for secure authentication. The `-t rsa` flag specifies the RSA algorithm, `-b 4096` sets a strong 4096-bit key size, `-f ~/.ssh/id_rsa` specifies the output file location, and `-N ""` creates the key without a passphrase (required for automated scripts). The command creates two files: `id_rsa` (private key, kept secret) and `id_rsa.pub` (public key, copied to remote servers).

**Copy the public key to the Backup Server:**
```bash
ssh-copy-id clint@stbkp01
```

**Explanation:** This command copies your public SSH key to the backup server's `~/.ssh/authorized_keys` file, enabling passwordless authentication. The command prompts for the remote user's password once during setup, then subsequent connections work without passwords. The `clint` user is the account on the backup server (`stbkp01`) that will receive file transfers. This step is critical for automated backup scripts that cannot handle interactive password prompts.

**Alternative manual method:**
```bash
cat ~/.ssh/id_rsa.pub | ssh clint@stbkp01 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
```

**Explanation:** This one-liner manually accomplishes what `ssh-copy-id` does: reads the public key, connects to the remote server, creates the `.ssh` directory if needed, appends the key to `authorized_keys`, and sets correct permissions (700 for directory, 600 for authorized_keys file). Proper permissions are essential for SSH to accept the key-based authentication.

**Refer to Day 7 for detailed SSH key setup instructions.**

### Step 2: Create the Backup Script Directory

Ensure the scripts directory exists with appropriate permissions.

```bash
sudo mkdir -p /scripts
```

**Explanation:** The `mkdir -p` command creates the `/scripts` directory if it doesn't exist. The `-p` flag (parents) creates parent directories as needed and doesn't error if the directory already exists, making the command idempotent. Using `sudo` provides the necessary privileges to create directories in the root filesystem. This directory will store operational scripts for system administration tasks.

### Step 3: Create the Backup Script

Write the backup automation script with proper shebang and commands.

```bash
sudo vi /scripts/beta_backup.sh
```

**Script content:**
```bash
#!/bin/sh

zip -r /backup/xfusioncorp_beta.zip /var/www/html/beta
scp /backup/xfusioncorp_beta.zip clint@stbkp01:/backup/
```

**Explanation:** This script automates the backup process with two key operations:

**Line 1 - Shebang (`#!/bin/sh`):** Specifies the interpreter for executing the script. The `#!/bin/sh` shebang tells the system to use the Bourne shell (or a compatible shell like dash) to run the script. Always include a shebang as the first line of scripts to ensure consistent execution across different environments.

**Line 3 - Create Archive:** The `zip -r` command recursively compresses the `/var/www/html/beta` directory and all its contents into a single archive file. The `-r` flag (recursive) includes all subdirectories and files. The output file `/backup/xfusioncorp_beta.zip` is created in the local backup directory. Zip format is chosen for broad compatibility and efficient compression of web content.

**Line 4 - Copy to Remote Server:** The `scp` (secure copy) command transfers the archive file to the backup server over SSH. It uses the previously configured SSH key for authentication, eliminating password prompts. The file is copied to `clint@stbkp01:/backup/`, specifying the remote user (clint), server (stbkp01), and destination path (/backup/). SCP provides encrypted transfer, ensuring backup data security during transmission.

### Step 4: Make the Script Executable

Set execute permissions to allow the script to run.

```bash
sudo chmod +x /scripts/beta_backup.sh
```

**Explanation:** The `chmod +x` command adds execute permission to the script file for all users (owner, group, others). The `+x` flag is shorthand for adding execute permission without modifying other permissions. Without execute permission, attempting to run the script would result in "Permission denied" errors. After this command, the script can be executed directly as `/scripts/beta_backup.sh` rather than requiring explicit interpreter invocation like `sh /scripts/beta_backup.sh`.

**Verify permissions:**
```bash
ls -l /scripts/beta_backup.sh
```

**Expected output:**
```bash
-rwxr-xr-x 1 root root 123 Nov 17 10:30 /scripts/beta_backup.sh
```

**Explanation:** The leading `-rwxr-xr-x` shows file permissions where `x` indicates execute permission for owner, group, and others. This confirms all users can execute the script.

### Step 5: Test the Backup Script

Execute the script to verify it works correctly without errors.

```bash
sudo /scripts/beta_backup.sh
```

**Explanation:** This command runs the backup script with root privileges, which may be necessary for reading web server files and writing to system directories. The script execution performs the archive creation and remote copy operations. Monitor the output for any error messages. Successful execution produces no output (silent success) or displays progress messages from zip and scp commands.

**Verify the backup was created locally:**
```bash
ls -lh /backup/xfusioncorp_beta.zip
```

**Explanation:** This command lists the backup archive with human-readable file sizes (`-lh` flags). Verify the file exists, has a reasonable size, and was created with a current timestamp.

**Verify the backup was copied to the remote server:**
```bash
ssh clint@stbkp01 "ls -lh /backup/xfusioncorp_beta.zip"
```

**Explanation:** This command connects to the backup server via SSH and lists the backup file to confirm successful transfer. The remote command is enclosed in quotes to execute on the remote server. Verification ensures the end-to-end backup process completed successfully.

### Step 6: Test Non-Root User Execution

Confirm the script can be run by the designated server user.

```bash
/scripts/beta_backup.sh
```

**Explanation:** Execute the script as the regular server user (without sudo) to ensure it has the necessary permissions to read source files, create archives, and write to backup directories. If this fails with permission errors, adjust file ownership or permissions on relevant directories, or configure sudo to allow specific operations without password prompts for this user.

---

## Understanding Bash Scripting

### Bash Script Fundamentals

**What is a Bash Script?**
A bash script is a text file containing a series of commands executed sequentially by the bash shell. Scripts automate repetitive tasks, reducing human error and saving time. They're essential for system administration, application deployment, backup operations, and DevOps workflows.

**Script Components:**
- **Shebang**: First line specifying the interpreter (e.g., `#!/bin/bash`, `#!/bin/sh`)
- **Comments**: Lines beginning with `#` for documentation (ignored during execution)
- **Commands**: Shell commands, built-in functions, and external programs
- **Variables**: Store data for reuse throughout the script
- **Control Structures**: Conditionals (if/else), loops (for, while), functions

### Bash Scripting Best Practices

**1. Always Use a Shebang:**
```bash
#!/bin/bash
```
The shebang (`#!`) followed by the interpreter path ensures the script runs with the correct shell, preventing unexpected behavior when executed from different environments or by automation systems.

**2. Enable Error Handling:**
```bash
set -e  # Exit immediately if any command fails
set -u  # Treat unset variables as errors
set -o pipefail  # Fail if any command in a pipeline fails
```
These options make scripts more robust by preventing silent failures and cascading errors.

**3. Quote Variables:**
```bash
backup_dir="/backup"
zip -r "$backup_dir/archive.zip" /source
```
Always quote variables (`"$variable"`) to prevent word splitting and glob expansion, especially when values might contain spaces or special characters.

**4. Use Functions for Reusability:**
```bash
create_backup() {
    local source_dir="$1"
    local backup_file="$2"
    zip -r "$backup_file" "$source_dir"
}

create_backup "/var/www/html/beta" "/backup/beta.zip"
```
Functions break complex scripts into manageable, testable, and reusable components.

**5. Add Logging and Error Messages:**
```bash
echo "Starting backup at $(date)"
if ! zip -r "$backup_file" "$source_dir"; then
    echo "ERROR: Failed to create backup archive" >&2
    exit 1
fi
echo "Backup completed successfully"
```
Logging provides visibility into script execution, essential for troubleshooting automated tasks.

**6. Validate Preconditions:**
```bash
if [ ! -d "/var/www/html/beta" ]; then
    echo "ERROR: Source directory does not exist" >&2
    exit 1
fi
```
Check that required directories, files, and commands exist before proceeding to avoid partial failures.

### Backup Strategies

**Full Backup:**
Complete copy of all data in the source directory. Simple to implement and restore, but requires significant storage space and time for large datasets. Best for small datasets or baseline backups.

**Incremental Backup:**
Only backs up files changed since the last backup (of any type). Requires minimal storage and time but complicates restoration (need base backup plus all incremental backups in sequence). Tools like `rsync` excel at incremental backups.

**Differential Backup:**
Backs up files changed since the last full backup. Balances storage efficiency with restoration simplicity—only need the last full backup and the last differential backup.

**Compression:**
Using `zip` or `tar.gz` reduces backup size, saving storage space and network transfer time. The trade-off is CPU time for compression/decompression and inability to perform incremental updates on compressed archives.

### Archive Command Comparison

**zip - Cross-Platform Archive Format:**
```bash
zip -r archive.zip directory/
```
- **Pros**: Universal compatibility (Windows, Linux, macOS), selective extraction, built-in compression
- **Cons**: Less efficient compression than tar.gz, not standard on all Unix systems
- **Use Case**: When compatibility with non-Unix systems is required

**tar - Unix Standard Archive Tool:**
```bash
tar -czf archive.tar.gz directory/
```
- **Pros**: Native Unix tool, excellent for preserving permissions and metadata, efficient with large files
- **Cons**: Requires separate compression tool (gzip, bzip2, xz), less common on Windows
- **Use Case**: Unix-to-Unix backups, system administration tasks

**tar with bzip2 Compression:**
```bash
tar -cjf archive.tar.bz2 directory/
```
- **Pros**: Better compression ratio than gzip, preserves Unix attributes
- **Cons**: Slower compression, larger CPU usage
- **Use Case**: When storage space is critical and compression time is acceptable

**Exclusions:**
```bash
tar -czf backup.tar.gz --exclude='*.log' --exclude='tmp/*' /var/www/html
```
Skip temporary files, logs, caches, and other non-essential data to reduce backup size and time.

**Verification:**
```bash
zip -T archive.zip  # Test zip archive integrity
tar -tzf archive.tar.gz  # List contents of tar.gz without extracting
```
Always test archives before relying on them for disaster recovery.

### Remote Copy Methods

**scp - Secure Copy Protocol:**
```bash
scp source.file user@remote:/destination/
```
- **Characteristics**: Simple syntax, encrypts data in transit, uses SSH for authentication
- **Best For**: Single file transfers, scripts requiring straightforward copying
- **Limitations**: No bandwidth limiting, full file transfer (no delta sync)

**rsync - Remote Synchronization:**
```bash
rsync -avz /source/ user@remote:/destination/
```
- **Characteristics**: Delta transfer (only copies changes), preserves metadata, compression, bandwidth control
- **Best For**: Large directories, repeated backups, synchronizing file systems
- **Flags**: `-a` (archive mode), `-v` (verbose), `-z` (compression), `--delete` (remove files not in source)

**sftp - SSH File Transfer Protocol:**
```bash
sftp user@remote
put source.file destination/
```
- **Characteristics**: Interactive file transfer, resume capability, directory operations
- **Best For**: Manual file transfers, interactive sessions
- **Scripting**: Can be scripted with batch files using `sftp -b batch.txt`

**Authentication:**
SSH key-based authentication is essential for automated scripts. Password-based authentication requires interactive input, breaking automation. Key-based authentication provides:
- **Non-Interactive**: Scripts run without human intervention
- **More Secure**: Keys can be longer than passwords, immune to brute force attacks
- **Auditable**: Each key can be tracked to specific users or applications
- **Revocable**: Keys can be removed without changing passwords

---

## Key Concepts

### Why Automate Backups?

**Consistency:** Automated scripts execute tasks exactly the same way every time, eliminating human error from forgotten steps or incorrect parameters.

**Reliability:** Scheduled backups run automatically even when staff is unavailable, ensuring business continuity and compliance with retention policies.

**Efficiency:** Free staff from repetitive manual tasks to focus on higher-value activities. A 10-minute manual backup becomes a zero-effort automated task.

**Scalability:** Once written, a backup script can be deployed across dozens or hundreds of servers, managed centrally, and executed in parallel.

### Script Security Considerations

**Password Handling:** Never hardcode passwords in scripts or store them in plaintext. Use SSH keys, secret management tools (HashiCorp Vault, AWS Secrets Manager), or environment variables with restricted permissions.

**File Permissions:** Scripts containing sensitive logic should have restrictive permissions (700 or 750) to prevent unauthorized viewing or modification.

**Secure Communication:** Always use encrypted protocols (SSH/SCP, HTTPS, TLS) for transferring backup data, especially over untrusted networks.

**Logging Sensitivity:** Don't log sensitive data (passwords, API keys, personal information) in script output or log files.

**Validation:** Validate input parameters and file paths to prevent command injection or path traversal attacks.

### Backup Best Practices

**3-2-1 Rule:**
- **3** copies of data (original + 2 backups)
- **2** different media types (local disk + cloud storage)
- **1** off-site backup (different physical location)

This strategy protects against hardware failure, site disasters, and ransomware attacks.

**Test Restores:** Regular restore testing (monthly or quarterly) ensures backups are valid and complete. Untested backups are liabilities, not assets.

**Retention Policies:** Define how long to keep backups (daily for 7 days, weekly for 4 weeks, monthly for 12 months). Balance compliance requirements, storage costs, and recovery needs.

**Monitoring:** Implement alerts for backup failures, missing backups, or unusual file sizes. Silent backup failures can go unnoticed until disaster strikes.

**Documentation:** Document backup procedures, restoration steps, storage locations, and responsible personnel. Ensure multiple people can execute disaster recovery.

### Scheduling with Cron

**Automate script execution using cron:**
```bash
crontab -e
```

**Daily backup at 2 AM:**
```bash
0 2 * * * /scripts/beta_backup.sh >> /var/log/beta_backup.log 2>&1
```

**Explanation:** The cron expression `0 2 * * *` means "at minute 0 of hour 2 (2:00 AM), every day, every month, every day of the week." Output is appended to a log file for troubleshooting. The `2>&1` redirects stderr to stdout, capturing both output streams in the log.

**Weekly backup on Sundays at 3 AM:**
```bash
0 3 * * 0 /scripts/beta_backup.sh
```

---

## Validation

Test your solution using KodeKloud's automated validation system. The validation checks:
- Script exists at `/scripts/beta_backup.sh`
- Script has execute permissions
- Script successfully creates local backup archive
- Script copies backup to remote server without password prompt
- Script can be executed by the designated server user

---

[← Day 9](day-09.md) | [Day 11 →](day-11.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
