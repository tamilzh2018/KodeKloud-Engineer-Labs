# Day 17: Install and Configure PostgreSQL

## Task Overview

Deploy and configure PostgreSQL database server for application data management. Create databases, configure user authentication, and grant appropriate permissions for application access.

**PostgreSQL Setup:**
- Connect to the database server
- Create PostgreSQL database
- Configure database roles and users
- Grant database privileges
- Set database ownership

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Connect to Database Server

Establish SSH connection to the database server where PostgreSQL is installed.

```sh
ssh user@db_host
```

This command initiates a secure shell connection to the database server. Replace `user` with your actual username and `db_host` with the database server's hostname or IP address. SSH provides encrypted communication between your local machine and the remote server. Ensure you have the correct credentials and network access before attempting the connection.

### Step 2: Execute PostgreSQL Commands as Postgres User (Command-Line Method)

Switch to the postgres system user and execute database creation and user configuration commands directly from the shell.

```sh
sudo -i -u postgres
psql -c "CREATE DATABASE kodekloud_db6;"
psql -c "CREATE ROLE kodekloud_aim LOGIN PASSWORD 'your-password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE kodekloud_db6 TO kodekloud_aim;"
psql -c "ALTER DATABASE kodekloud_db6 OWNER TO kodekloud_aim;"
```

The `sudo -i -u postgres` command switches to the postgres user account with a login shell, providing full access to PostgreSQL administration tools. The `-i` flag simulates an initial login, and `-u postgres` specifies the target user. The `psql -c` commands execute SQL statements directly from the command line without entering the interactive PostgreSQL prompt. This approach is efficient for automation and scripting, executing each command individually and returning to the shell after completion.

### Alternative Step 2: Execute Commands in PostgreSQL Interactive Shell

Alternatively, enter the PostgreSQL interactive prompt and execute SQL commands directly.

```sh
sudo psql -U postgres
```

This command launches the PostgreSQL interactive terminal as the postgres superuser. The `-U postgres` flag specifies the database user to connect as. Once inside the psql prompt, you'll see `postgres=#` indicating you're connected as a superuser to the postgres database.

### Step 3: Create Database and Configure User (Interactive Method)

Execute the following SQL commands within the PostgreSQL interactive shell:

```sql
CREATE DATABASE kodekloud_db6;
CREATE ROLE kodekloud_aim LOGIN PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE kodekloud_db6 TO kodekloud_aim;
ALTER DATABASE kodekloud_db6 OWNER TO kodekloud_aim;
```

The `CREATE DATABASE` command creates a new database named kodekloud_db6 with default settings. The `CREATE ROLE` statement creates a new database role with LOGIN privilege, allowing it to connect to the database, and sets a password for authentication. The `GRANT ALL PRIVILEGES` command provides full access rights (CREATE, CONNECT, TEMPORARY) on the database to the specified user. Finally, `ALTER DATABASE` changes the database owner to kodekloud_aim, giving complete administrative control including the ability to drop the database.

---

## Key Concepts

### PostgreSQL Architecture

**Database Cluster**: A PostgreSQL installation manages a collection of databases called a database cluster. All databases in a cluster share the same configuration files, process space, and system catalogs while maintaining separate schemas and data.

**Roles and Users**: PostgreSQL uses a unified concept called "roles" instead of separate users and groups. A role with the LOGIN attribute can connect to the database and is functionally equivalent to a traditional user account.

**Database Ownership**: Every database has an owner (typically the role that created it). The owner has all privileges on the database, including the ability to drop it. Database ownership can be transferred using the ALTER DATABASE command.

**Postgres Superuser**: The postgres role is created during installation as a superuser with unrestricted access to all databases and objects. It bypasses all permission checks and should be used carefully, typically only for administrative tasks.

### Role and User Management

**CREATE ROLE vs CREATE USER**: Historically, `CREATE USER` was equivalent to `CREATE ROLE` with the LOGIN attribute. Modern PostgreSQL treats them identically, but `CREATE ROLE` is preferred for clarity.

**LOGIN Attribute**: Without the LOGIN attribute, a role cannot be used to establish database connections. It can still own objects and be granted to other roles as a group membership.

**Password Authentication**: The `PASSWORD` clause sets the role's password for authentication. PostgreSQL stores passwords encrypted using SCRAM-SHA-256 (in recent versions) or MD5 hashing.

**Role Attributes**: Additional attributes include SUPERUSER, CREATEDB, CREATEROLE, REPLICATION, and BYPASSRLS. These control what administrative actions the role can perform.

### PostgreSQL Privileges

**Database-Level Privileges**: `GRANT ALL PRIVILEGES ON DATABASE` grants CONNECT (ability to connect), CREATE (create schemas), and TEMPORARY (create temporary tables) privileges on the specified database.

**Schema-Level Privileges**: After granting database access, you may need to grant privileges on specific schemas (like public) within the database using `GRANT ALL ON SCHEMA`.

**Table-Level Privileges**: For fine-grained control, grant specific privileges (SELECT, INSERT, UPDATE, DELETE) on individual tables or all tables in a schema.

**Default Privileges**: Use `ALTER DEFAULT PRIVILEGES` to automatically grant permissions on objects created in the future, ensuring new tables inherit the correct permissions.

### Authentication Methods

**Peer Authentication**: On local connections, PostgreSQL can authenticate using the operating system username. The postgres system user can connect as the postgres database role without a password.

**Password Authentication**: Requires a password for connection. Methods include SCRAM-SHA-256 (most secure), MD5 (legacy), and plain password (insecure, not recommended).

**pg_hba.conf Configuration**: This file controls client authentication, specifying which hosts can connect, which databases they can access, which roles they can use, and which authentication method is required.

**Trust Authentication**: Allows connection without authentication (dangerous). Only use on secure, isolated networks or for specific local connections during initial setup.

### Database Ownership and Permissions

**Owner Privileges**: Database owners can modify database settings, create schemas, grant privileges to other roles, and drop the database. Ownership provides comprehensive control beyond what GRANT ALL PRIVILEGES provides.

**Schema Ownership**: Within a database, schemas can have different owners. The schema owner controls objects within that schema and can grant usage permissions to other roles.

**Object Ownership**: Individual tables, views, and functions have owners. Only the owner (or a superuser) can alter or drop these objects.

**Privilege Inheritance**: When a role is granted to another role (group membership), the member role inherits the group's privileges, enabling role-based access control patterns.

### PostgreSQL vs MySQL Differences

**Role System**: PostgreSQL uses a unified role system, while MySQL maintains separate user and privilege concepts. PostgreSQL roles can represent both users and groups.

**Grant Syntax**: PostgreSQL's GRANT syntax is more flexible and granular. MySQL's grant system has different keywords and privilege levels.

**Default Databases**: PostgreSQL installations include postgres, template0, and template1 databases. MySQL includes mysql, information_schema, and performance_schema.

**Connection Methods**: PostgreSQL uses a more sophisticated authentication system with peer, SCRAM, and other methods. MySQL primarily uses password authentication.

### Best Practices

**Principle of Least Privilege**: Grant only the minimum permissions required for an application to function. Avoid using superuser accounts for application connections.

**Separate Roles for Applications**: Create dedicated database roles for each application or service, making it easier to audit access and revoke permissions when needed.

**Strong Passwords**: Use complex, randomly generated passwords for database roles. Store passwords securely using environment variables or secret management systems, never in source code.

**Regular Privilege Audits**: Periodically review granted privileges using `\du` (list roles) and `\z` or `\dp` (show table privileges) in psql to ensure access control remains appropriate.

**Connection Limits**: Set connection limits for non-superuser roles using `CREATE ROLE ... CONNECTION LIMIT 10` to prevent resource exhaustion from too many simultaneous connections.

### Common PostgreSQL Commands

**Connect to Database**: `\c database_name` switches to a different database within the psql session.

**List Databases**: `\l` or `\list` displays all databases in the cluster with their owners and encoding.

**List Roles**: `\du` or `\dg` shows all roles with their attributes and memberships.

**Show Privileges**: `\z tablename` or `\dp tablename` displays access privileges for a table.

**Exit psql**: `\q` or `Ctrl+D` exits the PostgreSQL interactive terminal.

### Security Considerations

**Encrypt Connections**: Configure PostgreSQL to require SSL/TLS connections for remote access, protecting credentials and data in transit.

**Firewall Rules**: Restrict database server access to only necessary IP addresses using firewall rules. PostgreSQL default port is 5432.

**Disable Remote Root Access**: Configure pg_hba.conf to prevent remote superuser connections, requiring local access for administrative tasks.

**Regular Updates**: Keep PostgreSQL updated with security patches. Subscribe to security mailing lists to stay informed about vulnerabilities.

**Audit Logging**: Enable PostgreSQL's logging features to track connection attempts, query execution, and privilege changes for security auditing and compliance.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 16](day-16.md) | [Day 18 →](day-18.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
