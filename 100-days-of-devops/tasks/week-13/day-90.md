# Day 90: Managing ACLs Using Ansible

## Task Overview

Implement fine-grained file permissions using Access Control Lists (ACLs) with Ansible. This task demonstrates creating files with specific ownership and applying ACL entries to grant targeted permissions to individual users and groups beyond traditional Unix file permissions.

**Technical Specifications:**
- Inventory file: /home/thor/ansible/inventory (pre-existing)
- Playbook location: /home/thor/ansible/playbook.yml (to be created)
- Files to create: blog.txt, story.txt, media.txt in /opt/devops/
- File ownership: root:root on all files
- ACL permissions: Different for each server (group tony-r, user steve-rw, group banner-rw)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Ansible directory and examine contents

```sh
cd ~/ansible
ls
```

Change to the Ansible directory where the inventory file is located, then list the directory contents to confirm the inventory file exists. The `ls` command verifies you're in the correct working directory before creating the playbook. This organization helps maintain a clean project structure with all related Ansible files in one location.

**Step 2:** Examine the existing inventory file

```sh
cat inventory
```

Display the inventory file contents to understand which hosts are defined and their connection parameters. The inventory should contain definitions for all three app servers (stapp01, stapp02, stapp03) with their respective SSH credentials. Understanding the inventory structure is crucial because the playbook will use host-specific conditions to apply different ACL configurations to each server.

**Step 3:** Create an empty playbook file

```sh
touch playbook.yml
```

Create an empty playbook file using the `touch` command. This file will contain all the tasks needed to create files in /opt/devops/ and apply ACL permissions. Creating the file first allows you to edit it with your preferred text editor in subsequent steps, whether that's vi, nano, emacs, or any other editor available on the jump host.

**Step 4:** Edit the playbook with file creation and ACL configuration

```yaml
---
- name: Create files with ACL permissions on app servers
  hosts: all
  become: yes
  tasks:
    - name: Create /opt/devops directory
      ansible.builtin.file:
        path: /opt/devops
        state: directory
        mode: '0755'

    - name: Create blog.txt on stapp01
      ansible.builtin.file:
        path: /opt/devops/blog.txt
        state: touch
        owner: root
        group: root
      when: inventory_hostname == 'stapp01'

    - name: Set ACL for group tony on blog.txt (stapp01)
      ansible.posix.acl:
        path: /opt/devops/blog.txt
        entity: tony
        etype: group
        permissions: r
        state: present
      when: inventory_hostname == 'stapp01'

    - name: Create story.txt on stapp02
      ansible.builtin.file:
        path: /opt/devops/story.txt
        state: touch
        owner: root
        group: root
      when: inventory_hostname == 'stapp02'

    - name: Set ACL for user steve on story.txt (stapp02)
      ansible.posix.acl:
        path: /opt/devops/story.txt
        entity: steve
        etype: user
        permissions: rw
        state: present
      when: inventory_hostname == 'stapp02'

    - name: Create media.txt on stapp03
      ansible.builtin.file:
        path: /opt/devops/media.txt
        state: touch
        owner: root
        group: root
      when: inventory_hostname == 'stapp03'

    - name: Set ACL for group banner on media.txt (stapp03)
      ansible.posix.acl:
        path: /opt/devops/media.txt
        entity: banner
        etype: group
        permissions: rw
        state: present
      when: inventory_hostname == 'stapp03'
```

Open the playbook with `vi playbook.yml` (or your editor) and add the content shown above. The playbook first creates the `/opt/devops/` directory on all servers to ensure it exists before creating files. Then, using conditional statements (`when`), it performs server-specific tasks: on stapp01, it creates blog.txt with root ownership and sets an ACL granting read permission to the tony group; on stapp02, it creates story.txt and grants read-write permissions to the steve user; on stapp03, it creates media.txt and grants read-write permissions to the banner group. The `ansible.posix.acl` module manages ACL entries, with `entity` specifying the user or group name, `etype` indicating whether it's a user or group, `permissions` defining the access level (r for read, w for write, rw for both), and `state: present` ensuring the ACL entry exists. The `when` conditionals ensure each file and its ACL are only created on the designated server, using `inventory_hostname` to identify the current host.

**Step 5:** Execute the Ansible playbook

```sh
ansible-playbook -i inventory playbook.yml
```

Run the playbook using the `ansible-playbook` command with the `-i inventory` flag to specify the inventory file. Ansible will execute tasks in sequence, evaluating the `when` conditions to skip tasks not applicable to each host. On stapp01, only the directory creation and blog.txt-related tasks will run; on stapp02, only story.txt tasks; on stapp03, only media.txt tasks. The output shows task execution status for each host, with "skipped" appearing for tasks where the `when` condition evaluated to false. Watch for "changed" status on applicable tasks and "failed" status indicating errors. The playbook's design ensures idempotency - running it multiple times will only make changes when necessary.

**Step 6:** Verify file creation and ownership

```sh
# Verify on stapp01
ansible stapp01 -i inventory -m shell -a "ls -la /opt/devops/blog.txt" --become

# Verify on stapp02
ansible stapp02 -i inventory -m shell -a "ls -la /opt/devops/story.txt" --become

# Verify on stapp03
ansible stapp03 -i inventory -m shell -a "ls -la /opt/devops/media.txt" --become
```

Verify that files were created with correct ownership on each server using Ansible ad-hoc commands. The `ls -la` command displays detailed file information including permissions, ownership, size, and modification time. On each server, you should see the file owned by root:root. The basic permissions shown by `ls -la` don't display ACL information - you'll see a `+` symbol at the end of the permission string (e.g., `-rw-r--r--+`) indicating that ACLs are set on the file.

**Step 7:** View ACL permissions using getfacl

```sh
# View ACLs on stapp01
ansible stapp01 -i inventory -m shell -a "getfacl /opt/devops/blog.txt" --become

# View ACLs on stapp02
ansible stapp02 -i inventory -m shell -a "getfacl /opt/devops/story.txt" --become

# View ACLs on stapp03
ansible stapp03 -i inventory -m shell -a "getfacl /opt/devops/media.txt" --become
```

Display the complete ACL configuration using the `getfacl` command, which shows all ACL entries including user, group, and other permissions. The output will show the file owner and group, plus the specific ACL entries you configured: on stapp01, you should see `group:tony:r--` (group tony has read permission); on stapp02, `user:steve:rw-` (user steve has read-write); on stapp03, `group:banner:rw-` (group banner has read-write). The getfacl output also shows the effective mask, which can limit ACL permissions. This verification confirms that ACLs are correctly applied.

**Step 8:** Test ACL permissions by attempting file access

```sh
# On stapp01, test if tony group can read blog.txt
ssh tony@stapp01 "cat /opt/devops/blog.txt"

# On stapp02, test if steve can read and write story.txt
ssh steve@stapp02 "echo 'test' >> /opt/devops/story.txt && cat /opt/devops/story.txt"

# On stapp03, test if banner group member can read and write media.txt
ssh banner@stapp03 "echo 'test' >> /opt/devops/media.txt && cat /opt/devops/media.txt"
```

Test that the ACL permissions work as expected by attempting to access the files as the users/groups granted permissions. On stapp01, the tony user (or any user in the tony group) should be able to read blog.txt. On stapp02, the steve user should be able to both read and write to story.txt. On stapp03, the banner user (or any user in the banner group) should be able to read and write to media.txt. If ACLs are correctly configured, these operations should succeed. If you try to perform operations not granted by the ACLs (like writing to blog.txt as tony), you should get permission denied errors.

---

## Key Concepts

**Access Control Lists (ACLs):**
- Extended permission system beyond traditional Unix owner/group/other model
- Allow fine-grained permissions for specific users and groups
- Can grant permissions to multiple users/groups on the same file
- Don't replace traditional permissions; they extend them
- Useful when traditional permissions are too restrictive
- Require filesystem support (ext3/ext4, XFS, etc. support ACLs by default)

**ACL Components:**
- **User ACLs**: Grant permissions to specific users (e.g., user:steve:rw-)
- **Group ACLs**: Grant permissions to specific groups (e.g., group:tony:r--)
- **Other**: Default permissions for users not matching any ACL
- **Mask**: Maximum permissions that can be granted via ACLs
- **Default ACLs**: Applied to new files/directories created within a directory

**Ansible ACL Module:**
- Part of `ansible.posix` collection (may need installation: `ansible-galaxy collection install ansible.posix`)
- Module name: `ansible.posix.acl`
- Manages file and directory ACL entries
- Idempotent: Safe to run multiple times
- Requires `acl` package on target systems
- Uses `setfacl` and `getfacl` commands under the hood

**ACL Module Parameters:**
- `path` - File or directory path (required)
- `entity` - User or group name receiving permissions
- `etype` - Entity type: `user`, `group`, `mask`, or `other`
- `permissions` - Permission string: `r` (read), `w` (write), `x` (execute), or combinations like `rw`, `rwx`
- `state` - `present` to add ACL entry, `absent` to remove it
- `default` - Set as default ACL (for directories, inherited by new files)
- `recursive` - Apply ACL recursively to directory contents

**Permission Combinations:**
- `r` - Read only
- `w` - Write only (rarely used alone)
- `x` - Execute only (for directories, allows traversal)
- `rw` - Read and write
- `rx` - Read and execute
- `rwx` - Full permissions
- `-` - No permissions (used in getfacl output)

**ACL vs Traditional Permissions:**
- Traditional: 3 permission sets (owner, group, other)
- ACLs: Unlimited permission sets for specific users/groups
- Traditional permissions are always evaluated first
- ACLs extend traditional permissions, don't replace them
- File owner always has permissions defined by traditional owner permissions
- ACL mask limits maximum permissions granted by ACLs

**Viewing and Setting ACLs Manually:**
```sh
# View ACLs on a file
getfacl filename

# Set user ACL
setfacl -m u:username:rw filename

# Set group ACL
setfacl -m g:groupname:r filename

# Remove specific ACL entry
setfacl -x u:username filename

# Remove all ACLs
setfacl -b filename

# Set default ACL on directory
setfacl -d -m u:username:rw directoryname
```

**ACL Mask:**
- Defines maximum effective permissions for ACL entries
- Automatically calculated when ACLs are set
- Can be explicitly set: `setfacl -m m::rw filename`
- User/group ACL permissions are AND'ed with mask
- Example: If mask is `r--` but user ACL is `rw-`, effective permission is `r--`
- Doesn't affect owner or other permissions

**Common Use Cases:**
- Granting access to specific users without changing group ownership
- Collaborative directories where multiple users need different access levels
- Service accounts needing specific file access
- Multi-tenant environments with complex permission requirements
- Temporary access grants without modifying group memberships

**Best Practices:**
- Use traditional permissions when possible; ACLs for exceptions
- Document why ACLs are used on specific files/directories
- Regularly audit ACL configurations for security
- Test ACLs after setting them to verify correct behavior
- Use default ACLs on directories for consistent permissions on new files
- Remember that `ls -l` shows `+` to indicate ACL presence but doesn't show details

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 89](day-89.md) | [Day 91 →](day-91.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
