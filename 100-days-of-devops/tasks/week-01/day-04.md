# Day 4: Script Execute Permissions

## Task Overview

Grant executable permissions to a bash script that was distributed to application servers but lacks the necessary permissions to run. This task demonstrates fundamental Linux file permission management, which is essential for automation, deployment, and security in DevOps workflows.

**Task Requirements:**
- Target file: `/tmp/xfusioncorp.sh` on App Server 1
- Grant execute permissions for all users (owner, group, others)
- Verify permission changes are applied correctly
- Understand different permission notation methods

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server via SSH

```sh
ssh user@app-server-1
```

Establish an SSH connection to App Server 1 where the script is located. Use the credentials provided in your KodeKloud lab environment to access the server. This is the standard first step for any remote server administration task.

**Step 2:** Check the current file permissions

```sh
ls -la /tmp/xfusioncorp.sh
```

List the file with detailed permissions using `ls -la`. The `-l` flag displays long format with permissions, ownership, size, and timestamps, while `-a` shows hidden files (though not strictly needed here). This command reveals the current permission state before making changes, which is crucial for troubleshooting and verification.

**Expected output:**

```txt
---------- 1 root root   40 Jul 30 02:21 xfusioncorp.sh
```

The initial permissions show `----------`, meaning no read, write, or execute permissions for anyone. The file is owned by root but is completely inaccessible. This is an unusual security-restrictive state that needs correction.

**Step 3:** Grant execute permissions using numeric notation

```sh
sudo chmod 755 /tmp/xfusioncorp.sh
```

Change file permissions using the `chmod` (change mode) command with numeric octal notation. The number `755` breaks down as: 7 (owner: read+write+execute), 5 (group: read+execute), 5 (others: read+execute). Since the file is owned by root, we need `sudo` to modify its permissions. This permission set (755) is standard for executable scripts and allows the owner full control while letting all users execute the script.

**Step 4:** Verify the permission changes

```sh
ls -la /tmp/xfusioncorp.sh
```

Re-run the detailed listing command to confirm the permissions were changed successfully. This verification step is critical in production environments to ensure changes took effect before proceeding with script execution or deployment.

**Expected output:**

```txt
-rwxr-xr-x 1 root root   40 Jul 30 02:21 xfusioncorp.sh
```

The permissions now show `-rwxr-xr-x`, confirming: owner has read+write+execute (rwx), group has read+execute (r-x), and others have read+execute (r-x). The leading dash indicates this is a regular file (not a directory or special file).

**Step 5:** Test script execution (optional validation)

```sh
/tmp/xfusioncorp.sh
```

Execute the script to verify it runs successfully now that execute permissions are granted. Depending on the script contents and your user privileges, you may need to use `sudo` if the script performs privileged operations. If the script runs without "Permission denied" errors, the permission change was successful.

---

## Understanding Linux File Permissions

**Permission Basics:**

Linux uses a three-tiered permission system:
- **User (u)**: The file owner
- **Group (g)**: Users in the file's group
- **Others (o)**: All other users on the system

Each tier has three permission types:
- **Read (r)**: View file contents or list directory contents (value: 4)
- **Write (w)**: Modify file contents or create/delete files in directory (value: 2)
- **Execute (x)**: Run file as program or access directory (value: 1)

**Numeric (Octal) Notation:**

Each permission set is a sum of values:
- `7 = 4+2+1` = rwx (read, write, execute)
- `6 = 4+2` = rw- (read, write)
- `5 = 4+1` = r-x (read, execute)
- `4 = 4` = r-- (read only)
- `0` = --- (no permissions)

Example: `chmod 754 file`
- `7` (owner): rwx = full access
- `5` (group): r-x = read and execute
- `4` (others): r-- = read only

**Symbolic Notation:**

Alternative method using letters and operators:

```sh
# Set exact permissions
chmod u=rwx,g=rx,o=r test.sh

# Add permissions
chmod g+w test.sh     # Add write for group
chmod a+x test.sh     # Add execute for all (a=all)

# Remove permissions
chmod o-r test.sh     # Remove read for others
chmod go-w test.sh    # Remove write for group and others
```

**Common Permission Patterns:**

- `755` (rwxr-xr-x): Standard for executables and scripts
- `644` (rw-r--r--): Standard for regular files
- `600` (rw-------): Private files (only owner can access)
- `777` (rwxrwxrwx): Full access for everyone (dangerous, avoid)
- `700` (rwx------): Private executables (only owner)

**Security Considerations:**

- **Principle of Least Privilege**: Grant minimum permissions required
- **Execute Bit Security**: Only grant execute permission to trusted scripts
- **World-writable Danger**: Avoid `777` permissions as they allow anyone to modify files
- **Directory Permissions**: Execute (x) on directories is required to access contents
- **Sticky Bit**: Special permission for shared directories like `/tmp`

**Permission Verification Commands:**

```sh
# Check specific file permissions
ls -l filename

# Check permissions with numeric values displayed
stat -c '%a %n' filename

# Find files with specific permissions
find /path -perm 755

# Find files with excessive permissions (security audit)
find /path -perm -002  # World-writable files
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 3](day-03.md) | [Day 5 →](day-05.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
