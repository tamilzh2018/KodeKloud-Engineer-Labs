# Day 2: Temporary User Setup with Expiry Date

## Task Overview

Establish a time-limited user account with automatic expiration. This approach supports temporary project assignments by ensuring accounts become inactive after a specified date without manual intervention.

**Account Requirements:**
- Username: specific user (as per task)
- Expiration date: set to future date (YYYY-MM-DD format)
- Home directory: standard creation
- Automatic deactivation: triggered on expiry date

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server via SSH

```sh
ssh user@app-server-ip
```

Establish an SSH connection to the target application server where you need to create the temporary user account. Use the credentials provided in your KodeKloud lab environment. This step is the same as Day 1 - you're remotely accessing the server to perform administrative tasks.

**Step 2:** Create user account with automatic expiration date

```sh
sudo useradd -m -e 2024-01-28 yousuf
```

Create a new user account with a built-in expiration date using the `useradd` command. The `-m` flag creates a home directory at `/home/yousuf` for the user. The `-e 2024-01-28` flag sets the account expiration date in YYYY-MM-DD format, after which the account will be automatically locked and the user cannot login. This is invaluable for managing temporary contractors, interns, or project-based staff, as it eliminates the need to manually remember to disable accounts when access should end. Replace the date with the specific expiration date from your task requirements.

**Step 3:** Verify user account creation

```sh
cat /etc/passwd
```

Display the contents of the `/etc/passwd` file to confirm the new user account has been created successfully. Look for an entry like: `yousuf:x:1003:1004::/home/yousuf:/bin/bash`. This confirms the user exists in the system database with a home directory and default shell. Note that the expiration date is not stored in `/etc/passwd` but rather in the shadow password file.

**Step 4:** Test user account access and check expiration details

```sh
sudo su yousuf
```

Switch to the newly created user account to verify it's currently active and accessible. This command should succeed if you're testing before the expiration date. After successful login, you can type `exit` to return to your original user session.

**Step 5:** Verify account expiration configuration

```sh
sudo chage -l yousuf
```

Display the password aging and account expiration information for the user using the `chage` (change age) command. The `-l` flag lists the account's aging details including the account expiration date. You should see "Account expires" showing your configured date (e.g., Jan 28, 2024). This provides definitive confirmation that the automatic expiration is properly configured and will be enforced by the system.

---

## Key Concepts

**Account Expiration vs Password Expiration:**
- Account expiration (`-e` flag): The entire account becomes locked on the specified date
- Password expiration (managed by `chage`): Only the password expires, requiring the user to change it
- Account expiration is permanent until manually changed by an administrator

**Date Format:**
- Must use YYYY-MM-DD (ISO 8601 format) for the `-e` flag
- Example: 2024-12-31 for December 31st, 2024
- Invalid formats will cause the useradd command to fail

**Managing Temporary Accounts:**
- `chage -E 2024-12-31 username`: Change expiration date for existing user
- `chage -E -1 username`: Remove expiration date (make permanent)
- `chage -l username`: View current expiration settings
- Expired accounts remain in the system but cannot login

**Best Practices:**
- Always set expiration dates for temporary staff, contractors, and consultants
- Review and audit account expiration dates regularly
- Use automation tools to generate reports of expiring accounts
- Document the reason for temporary access in user description field

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 1](day-01.md) | [Day 3 →](day-03.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
