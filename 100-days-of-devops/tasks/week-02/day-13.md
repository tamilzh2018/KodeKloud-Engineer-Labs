# Day 13: IPtables Installation And Configuration

## Task Overview

Configure host-based firewall rules to secure application servers. Implement network filtering using iptables to control incoming traffic and restrict access to specific ports based on source IP addresses.

**Security Requirements:**
- Install iptables firewall on all application hosts
- Block incoming port 6200 for all traffic except from Load Balancer
- Configure IP-based access control lists (whitelisting)
- Ensure firewall rules persist across system reboots

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Install iptables and required dependencies

```sh
sudo yum install -y iptables iptables-services
```

Install the iptables firewall package and its services component using yum package manager. The `-y` flag automatically answers "yes" to all prompts, enabling non-interactive installation. The `iptables` package provides the core firewall functionality, while `iptables-services` includes the systemd service files and init scripts needed to manage iptables as a system service. This installation is required on each application server that needs firewall protection.

**Step 2:** Create an ACCEPT rule for the Load Balancer host

```sh
sudo iptables -A INPUT -p tcp --dport 6200 -s 172.16.238.14 -j ACCEPT
```

Add a firewall rule to explicitly allow incoming TCP traffic on port 6200 from the Load Balancer host (172.16.238.14). The `-A INPUT` flag appends this rule to the INPUT chain (which handles incoming packets), `-p tcp` specifies the TCP protocol, `--dport 6200` matches destination port 6200, `-s 172.16.238.14` restricts the source to the LBR host IP address, and `-j ACCEPT` sets the target action to accept matching packets. This whitelisting approach ensures the Load Balancer can communicate with the application on port 6200 while all other sources will be blocked by the subsequent rule.

**Step 3:** Verify the current iptables rules

```sh
sudo iptables -L INPUT -n -v --line-numbers
```

List all rules in the INPUT chain with detailed information to verify your configuration. The `-L INPUT` flag lists rules for the INPUT chain, `-n` displays IP addresses and ports numerically without DNS resolution (faster and clearer), `-v` enables verbose output showing packet and byte counters, and `--line-numbers` displays rule numbers for easy reference. You should see your ACCEPT rule at the top with source 172.16.238.14 and destination port 6200, showing zero packet counters initially.

**Step 4:** Create a REJECT rule to block all other traffic on port 6200

```sh
sudo iptables -A INPUT -p tcp --dport 6200 -j REJECT
```

Add a firewall rule to reject all other incoming TCP traffic on port 6200 that doesn't match the previous ACCEPT rule. Since iptables processes rules sequentially from top to bottom and stops at the first match, this rule will only apply to traffic from sources other than 172.16.238.14. The `-j REJECT` target actively rejects connections by sending back an ICMP port unreachable message, which is more explicit than DROP and helps with troubleshooting. This creates a secure default-deny policy for port 6200 while allowing only authorized traffic.

**Step 5:** Verify the complete ruleset

```sh
sudo iptables -L INPUT -n -v --line-numbers
```

Display the complete INPUT chain rules again to confirm both rules are in the correct order. You should see two entries: rule 1 accepting TCP traffic to port 6200 from 172.16.238.14, followed by rule 2 rejecting all other TCP traffic to port 6200. The order is critical because iptables uses a first-match-wins policy. If these rules were reversed, all traffic would be rejected before the ACCEPT rule could be evaluated.

**Step 6:** Save the iptables rules for persistence

```sh
sudo service iptables save
```

Persist the current iptables rules to disk so they survive system reboots. This command writes the active ruleset to `/etc/sysconfig/iptables` (on RHEL/CentOS systems), which is automatically loaded by the iptables service during system startup. Without this step, all firewall rules would be lost after a reboot, leaving the server unprotected. The output should confirm "iptables: Saving firewall rules to /etc/sysconfig/iptables" indicating successful persistence.

**Step 7:** Enable iptables service to start at boot

```sh
sudo systemctl enable iptables
sudo systemctl start iptables
```

Configure the iptables service to automatically start during system boot and ensure it's currently running. The `enable` command creates the necessary systemd symlinks so the service starts on boot, while `start` initiates the service immediately if not already running. This two-step process ensures both immediate protection and persistent firewall activation across reboots. You can verify with `systemctl status iptables` which should show "active (exited)" and "enabled" status.

**Step 8:** Test the firewall configuration from the Load Balancer

```sh
# From the Load Balancer host (172.16.238.14)
curl http://app-server:6200
# Should successfully connect
```

Validate that traffic from the authorized Load Balancer host can successfully reach port 6200 on the application server. Execute this curl command from the LBR host, which should establish a connection and receive a response (even if it's an error page, the connection itself proves the firewall rule works). A successful connection confirms the ACCEPT rule is functioning correctly and the source IP whitelist is properly configured.

**Step 9:** Test that unauthorized access is blocked

```sh
# From any other host (not 172.16.238.14)
curl http://app-server:6200
# Should be rejected
```

Verify that traffic from unauthorized sources is properly blocked by the firewall. When attempting to connect from any host other than the Load Balancer, you should receive a connection refused error or timeout, confirming that the REJECT rule is working as intended. This validates that your security policy is enforced and only the designated Load Balancer can access the application on port 6200.

**Step 10:** Additional verification commands

```bash
# View saved iptables rules file
sudo cat /etc/sysconfig/iptables

# Check iptables service status
sudo systemctl status iptables

# View all chains and rules
sudo iptables -L -n -v

# Show rules with packet statistics
watch -n 1 'sudo iptables -L INPUT -n -v --line-numbers'
```

These supplementary commands provide comprehensive visibility into your firewall configuration. The first command displays the persistent rules file to confirm your rules are saved correctly. The systemctl status command verifies the service is active and enabled. The third command shows all chains (INPUT, OUTPUT, FORWARD) with their complete rulesets. The watch command creates a live-updating view of the INPUT chain with packet counters, allowing you to observe real-time traffic patterns and rule matches during testing.

---

## Key Concepts

**IPtables Architecture:**
- Tables: filter (packet filtering), nat (network address translation), mangle (packet alteration), raw (connection tracking)
- Chains: INPUT (incoming to local), OUTPUT (outgoing from local), FORWARD (routed through), PREROUTING, POSTROUTING
- Targets: ACCEPT (allow packet), REJECT (deny with notification), DROP (silently discard), LOG (record packet info)
- Rule processing: Sequential evaluation from top to bottom, first match determines action

**Firewall Rule Components:**
- Protocol specification: `-p tcp`, `-p udp`, `-p icmp` define which protocol to match
- Port matching: `--dport` (destination port), `--sport` (source port) for TCP/UDP
- IP filtering: `-s` (source IP/network), `-d` (destination IP/network) with CIDR notation support
- Actions: `-j ACCEPT`, `-j REJECT`, `-j DROP` determine packet fate

**Security Best Practices:**
- Default deny policy: Block all traffic except explicitly allowed (whitelist approach)
- Rule ordering: Place specific ACCEPT rules before general DENY/REJECT rules
- Source IP filtering: Restrict access to known, trusted IP addresses
- Minimal exposure: Only open ports that are absolutely necessary for service operation
- Regular audits: Review firewall rules periodically to remove obsolete entries

**Persistence Mechanisms:**
- CentOS/RHEL: `/etc/sysconfig/iptables` loaded by iptables.service
- Ubuntu/Debian: Use `iptables-persistent` package with `netfilter-persistent save`
- Manual approach: `iptables-save > /etc/iptables/rules.v4` and restore at boot
- Verification: Always test that rules survive a system reboot

**Common Iptables Operations:**
- Insert rule at position: `iptables -I INPUT 1 [rule]` (inserts at line 1)
- Delete by number: `iptables -D INPUT 2` (removes second rule)
- Delete by specification: `iptables -D INPUT -p tcp --dport 80 -j ACCEPT`
- Flush all rules: `iptables -F` (removes all rules but keeps chains)
- Reset counters: `iptables -Z` (clears packet/byte statistics)

**Troubleshooting Tips:**
- Connection issues: Use `-j LOG` target before REJECT/DROP to log rejected packets
- Log location: Check `/var/log/messages` or `/var/log/syslog` for iptables logs
- Testing: Use `telnet` or `nc` (netcat) to test port connectivity
- Packet tracing: `iptables -t raw -A PREROUTING -p tcp --dport 6200 -j TRACE`
- Temporarily disable: `systemctl stop iptables` (for testing only)

---

## Validation

Test your solution using KodeKloud's automated validation.

**Manual Validation Checklist:**
- [ ] iptables and iptables-services packages installed on all app servers
- [ ] ACCEPT rule exists for LBR host (172.16.238.14) on port 6200
- [ ] REJECT rule exists for all other sources on port 6200
- [ ] Rules are saved to /etc/sysconfig/iptables
- [ ] iptables service is enabled and active
- [ ] Successful connection test from Load Balancer host
- [ ] Blocked connection test from unauthorized host
- [ ] Rules persist after system reboot

---

[← Day 12](day-12.md) | [Day 14 →](day-14.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
