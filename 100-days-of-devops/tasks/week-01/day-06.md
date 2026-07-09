# Day 6: Setup a Cron Job

## Task Overview

Install and configure the cron service on all Nautilus application servers, then create a scheduled job for automated task execution. This establishes the foundation for automated system maintenance, monitoring, and operational tasks across the infrastructure.

**Task Requirements:**
- Install cronie package on all app servers
- Enable and start the crond service
- Create a cron job running every 5 minutes
- Configure job to run as root user
- Write output to `/tmp/cron_text`

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the first application server via SSH

```sh
ssh user@app-server-1
```

Establish an SSH connection to the first application server. You'll need to repeat steps 2-7 for each application server (app-server-1, app-server-2, app-server-3, etc.) in the Stratos Datacenter. This ensures consistent cron job deployment across the entire infrastructure, which is essential for distributed automation workflows.

**Step 2:** Install the cronie package

```sh
sudo yum install cronie -y
```

Install the cronie package, which provides the cron daemon and crontab utilities on RHEL/CentOS systems. The `-y` flag automatically confirms the installation without prompting for user input. Cronie is the modern implementation of cron for Red Hat-based distributions, providing scheduled task execution with improved logging and systemd integration. The installation includes the crond daemon, crontab command-line tools, and necessary configuration files.

**Step 3:** Enable the cron service to start automatically at boot

```sh
sudo systemctl enable crond
```

Configure the crond service to start automatically during system boot using systemd. The `enable` command creates the necessary symbolic links in systemd's configuration that ensure the cron daemon launches whenever the server starts. This is critical for production environments where automated tasks must resume immediately after system reboots, maintenance windows, or unexpected power cycles without manual intervention.

**Step 4:** Start the cron service immediately

```sh
sudo systemctl start crond
```

Start the crond service immediately without waiting for a system reboot. This command launches the cron daemon process which begins monitoring crontab files and executing scheduled jobs according to their schedules. Starting the service now allows you to immediately test and verify your cron job configuration rather than waiting for the next system restart.

**Step 5:** Verify the cron service is running

```sh
sudo systemctl status crond
```

Check the operational status of the crond service to confirm it's running properly. Look for "active (running)" in green text, which indicates the service is operational and processing scheduled jobs. This verification step catches any startup issues, permission problems, or configuration errors before proceeding to add cron jobs. If the status shows "inactive" or "failed", investigate the system logs using `journalctl -u crond` for troubleshooting information.

**Step 6:** Open the root user's crontab for editing

```sh
sudo crontab -e
```

Open the crontab editor for the root user account. The `-e` flag launches your default text editor (usually vi or nano) with root's crontab file. Using `sudo crontab -e` ensures you're editing root's crontab, not your personal user's crontab. The first time you run this command, you may be prompted to select your preferred editor. Each user on the system has their own crontab file, and root's crontab is specifically required for this task.

**Step 7:** Add the scheduled cron job

```
*/5 * * * * echo hello > /tmp/cron_text
```

Add this cron job entry to the crontab file. The schedule format `*/5 * * * *` means "every 5 minutes" (the `*/5` in the minute field divides the hour into 5-minute intervals). The five fields represent: minute (*/5), hour (*), day of month (*), month (*), and day of week (*). Asterisks mean "every" for that time unit. The command `echo hello > /tmp/cron_text` writes the word "hello" to a file, overwriting previous content. In vi, press `i` to enter insert mode, type the cron job line, press `Esc`, then type `:wq` and press Enter to save and exit.

**Step 8:** Verify the cron job was added successfully

```sh
sudo crontab -l
```

List all cron jobs for the root user using the `-l` (list) flag. This displays the contents of root's crontab file, allowing you to confirm your cron job entry was saved correctly and is formatted properly. You should see your `*/5 * * * * echo hello > /tmp/cron_text` entry in the output. This verification ensures the cron daemon will execute your job on schedule.

**Step 9:** Monitor cron job execution (optional verification)

```sh
# Wait 5+ minutes, then check the output file
cat /tmp/cron_text

# Check cron execution logs
sudo tail -f /var/log/cron

# Watch for job execution in real-time
watch -n 30 'ls -lh /tmp/cron_text && cat /tmp/cron_text'
```

After waiting at least 5 minutes, verify the cron job executed successfully by checking the output file at `/tmp/cron_text`. The file should contain "hello" if the job ran correctly. You can also monitor the cron log file at `/var/log/cron` to see when jobs are triggered. The `watch` command continuously displays the file's timestamp and content, updating every 30 seconds, allowing you to observe the job running in real-time.

---

## Understanding Cron Job Scheduling

**Cron Time Format:**

The cron schedule consists of 5 time fields followed by the command:
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, where both 0 and 7 = Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

**Special Characters:**

- `*` (asterisk): Matches all values (every minute, hour, day, etc.)
- `,` (comma): Lists multiple values (1,15,30 = 1st, 15th, and 30th)
- `-` (hyphen): Specifies ranges (1-5 = 1,2,3,4,5)
- `/` (slash): Specifies step values (*/5 = every 5 units)

**Common Cron Schedule Examples:**

```sh
# Every 5 minutes
*/5 * * * * command

# Every hour at minute 0
0 * * * * command

# Every day at 2:30 AM
30 2 * * * command

# Every Monday at 9:00 AM
0 9 * * 1 command

# First day of every month at midnight
0 0 1 * * command

# Every 15 minutes during business hours (9 AM - 5 PM)
*/15 9-17 * * * command

# Twice a day (6 AM and 6 PM)
0 6,18 * * * command
```

**Cron Job Management:**

```sh
# Edit current user's crontab
crontab -e

# Edit root's crontab (requires sudo)
sudo crontab -e

# List current user's cron jobs
crontab -l

# Remove current user's crontab
crontab -r

# Edit specific user's crontab (as root)
sudo crontab -u username -e
```

**Important Cron Considerations:**

- **Environment Variables**: Cron runs with a minimal environment. Set PATH, SHELL, etc., if needed:
  ```
  PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
  SHELL=/bin/bash
  */5 * * * * /path/to/script.sh
  ```

- **Absolute Paths**: Always use full paths for commands and files in cron jobs
- **Output Redirection**: Redirect output to prevent email notifications:
  ```
  */5 * * * * command > /dev/null 2>&1
  ```

- **Logging**: Direct output to log files for debugging:
  ```
  */5 * * * * command >> /var/log/myjob.log 2>&1
  ```

**System vs User Crontabs:**

- User crontabs: `/var/spool/cron/username` (managed via `crontab` command)
- System crontab: `/etc/crontab` (edited directly, includes username field)
- Cron directories: `/etc/cron.d/`, `/etc/cron.daily/`, `/etc/cron.hourly/`, `/etc/cron.weekly/`, `/etc/cron.monthly/`

**Troubleshooting Cron Jobs:**

```sh
# Check cron logs
sudo tail -f /var/log/cron
sudo grep CRON /var/log/syslog

# Verify cron service is running
sudo systemctl status crond

# Test command manually
/path/to/command

# Check crontab syntax
crontab -l | grep -v "^#"
```

**Automation Script (Optional):**

For deploying across multiple servers, you can use this automation script:

```sh
#!/bin/sh
# setup_cron_job.sh - Automate cron job deployment

set -e  # Exit on any error

echo "=== Setting up Cron Job on CentOS ==="

# Install cronie package
echo "Installing cronie package..."
if ! rpm -q cronie &>/dev/null; then
    sudo yum install cronie -y
    echo "✓ cronie package installed"
else
    echo "✓ cronie package already installed"
fi

# Start and enable crond service
sudo systemctl start crond
sudo systemctl enable crond
echo "✓ crond service configured"

# Add cron job for root user
CRON_JOB="*/5 * * * * echo hello > /tmp/cron_text"
if sudo crontab -l 2>/dev/null | grep -q "echo hello > /tmp/cron_text"; then
    echo "✓ Cron job already exists"
else
    (sudo crontab -l 2>/dev/null || true; echo "$CRON_JOB") | sudo crontab -
    echo "✓ Cron job added successfully"
fi

echo "=== Setup Complete ==="
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 5](day-05.md) | [Day 7 →](day-07.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
