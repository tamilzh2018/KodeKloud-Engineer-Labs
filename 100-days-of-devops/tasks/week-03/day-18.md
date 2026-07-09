# Day 18: Configure LAMP Server (LAMP Stack)

## Task Overview

Deploy a complete LAMP (Linux, Apache, MySQL/MariaDB, PHP) stack for hosting dynamic web applications. Configure Apache web server on a custom port, install PHP with database connectivity, set up MariaDB database server, and establish database users with appropriate permissions.

**LAMP Stack Components:**
- Install Apache HTTP Server with PHP
- Configure custom Apache port
- Install and configure MariaDB database
- Create database and user accounts
- Grant database privileges for application access

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Configure Application Servers

### Step 1: Install Apache, PHP, and MySQL Extension

Install the core LAMP stack packages on all application servers.

```sh
sudo yum install -y httpd php php-mysqli
```

This command installs three essential packages: Apache HTTP Server (httpd), PHP interpreter, and the PHP MySQL/MariaDB extension (php-mysqli). The `-y` flag automatically confirms installation. The php-mysqli extension enables PHP scripts to communicate with MySQL/MariaDB databases using the improved MySQL extension. These packages form the foundation of the LAMP stack, enabling dynamic web application hosting with database connectivity.

### Step 2: Configure Apache Port and Start Service

Back up the Apache configuration, change the default port to 3003, and start the service.

```sh
sudo cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo sed -i 's/\<80\>/3003/g' /etc/httpd/conf/httpd.conf
sudo systemctl enable --now httpd
```

The first command creates a backup of the Apache configuration file before making changes, following best practices for configuration management. The `sed` command uses a regular expression to replace all occurrences of port 80 (as a whole word) with 3003 throughout the configuration file. The word boundaries `\<` and `\>` ensure only standalone "80" is replaced, not numbers like "8080". The `systemctl enable --now` command both enables Apache to start on boot and starts it immediately in one operation. Repeat these steps on all application servers.

### Configure Database Server

### Step 3: Install and Start MariaDB Server

Install MariaDB database server on the dedicated database server and verify it's running.

```sh
sudo yum install -y mariadb-server
sudo systemctl enable --now mariadb
sudo systemctl status mariadb | grep "running"
```

MariaDB is a community-developed fork of MySQL that maintains compatibility while providing additional features and performance improvements. The `systemctl enable --now` command configures MariaDB to start automatically on system boot and starts it immediately. The `status` command piped through `grep` filters the output to show only the running status, providing quick verification that the database server is operational.

### Step 4: Create Database, User, and Grant Privileges

Set up the application database and user with full privileges.

```sh
mysql -u root -e "CREATE DATABASE kodekloud_db2;"
mysql -u root -e "CREATE USER 'kodekloud_cap'@'%' IDENTIFIED BY 'your-pass';"
mysql -u root -e "GRANT ALL ON kodekloud_db2.* TO 'kodekloud_cap'@'%';"
mysql -u root -e "FLUSH PRIVILEGES;"
```

These commands execute SQL statements directly from the command line using the `-e` flag. The `CREATE DATABASE` statement creates a new database named kodekloud_db2. The `CREATE USER` statement creates a user 'kodekloud_cap' that can connect from any host ('%' wildcard), with password authentication. The `GRANT ALL` statement provides complete privileges (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, etc.) on all tables in the kodekloud_db2 database. The `FLUSH PRIVILEGES` command reloads the grant tables, ensuring privilege changes take effect immediately without restarting MySQL.

---

## MySQL Command Reference

### MySQL Installation Paths

**Mac**: `/usr/local/mysql/bin`
**Windows**: `/Program Files/MySQL/MySQL version/bin`
**Xampp**: `/xampp/mysql/bin`

### Add MySQL to PATH

```bash
# Current Session Only
export PATH=${PATH}:/usr/local/mysql/bin

# Permanent Configuration
echo 'export PATH="/usr/local/mysql/bin:$PATH"' >> ~/.bash_profile
```

The `export` command adds MySQL binaries to your PATH environment variable for the current shell session. Adding the export statement to `~/.bash_profile` makes the change permanent by executing it automatically on login. This allows running `mysql` commands without specifying the full path.

### Authentication and User Management

#### Login to MySQL

```bash
mysql -u root -p
```

Connects to MySQL as the root user. The `-p` flag prompts for password entry securely. After successful authentication, you'll see the `mysql>` prompt.

#### Show All Users

```sql
SELECT User, Host FROM mysql.user;
```

Queries the mysql.user table to display all database users and their allowed connection hosts. The mysql database stores system tables including user accounts and privileges.

#### Create User

```sql
CREATE USER 'someuser'@'localhost' IDENTIFIED BY 'somepassword';
```

Creates a new user account that can only connect from localhost. The `IDENTIFIED BY` clause sets the password. For remote access, replace 'localhost' with a hostname, IP address, or '%' for any host.

#### Grant All Privileges

```sql
GRANT ALL PRIVILEGES ON * . * TO 'someuser'@'localhost';
FLUSH PRIVILEGES;
```

The `*.*` syntax grants privileges on all databases and all tables (first * = databases, second * = tables). This gives complete control over the MySQL server. Always flush privileges after grant changes.

#### Show User Grants

```sql
SHOW GRANTS FOR 'someuser'@'localhost';
```

Displays all privileges granted to a specific user, useful for auditing permissions and troubleshooting access issues.

#### Revoke Privileges

```sql
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'someuser'@'localhost';
```

Removes all privileges from a user, including the ability to grant privileges to others. The user account still exists but has no permissions.

#### Delete User

```sql
DROP USER 'someuser'@'localhost';
```

Permanently removes a user account from the system. This also removes all privileges associated with the account.

#### Exit MySQL

```sql
exit;
```

Closes the MySQL client connection and returns to the shell prompt. You can also use `quit;` or `Ctrl+D`.

### Database Operations

#### Show All Databases

```sql
SHOW DATABASES;
```

Lists all databases the current user has permission to see. System databases include mysql, information_schema, and performance_schema.

#### Create Database

```sql
CREATE DATABASE acme;
```

Creates a new empty database with default character set and collation. Database names are case-sensitive on Linux but not on Windows.

#### Delete Database

```sql
DROP DATABASE acme;
```

Permanently deletes a database and all its tables and data. This operation cannot be undone, so use with extreme caution.

#### Select/Use Database

```sql
USE acme;
```

Switches context to the specified database. All subsequent table operations apply to this database until you switch to another.

### Table Operations

#### Create Table

```sql
CREATE TABLE users(
    id INT AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(50),
    password VARCHAR(20),
    location VARCHAR(100),
    dept VARCHAR(100),
    is_admin TINYINT(1),
    register_date DATETIME,
    PRIMARY KEY(id)
);
```

Defines a table schema with various column types. `AUTO_INCREMENT` automatically generates unique IDs. `VARCHAR(n)` stores variable-length strings up to n characters. `TINYINT(1)` commonly represents boolean values (0/1). `DATETIME` stores date and time. `PRIMARY KEY` uniquely identifies each row and creates an index.

#### Drop Table

```sql
DROP TABLE tablename;
```

Permanently deletes a table and all its data. The table structure and contents are completely removed.

#### Show Tables

```sql
SHOW TABLES;
```

Lists all tables in the currently selected database. Use after `USE database_name` to see available tables.

### Data Manipulation

#### Insert Single Row

```sql
INSERT INTO users (first_name, last_name, email, password, location, dept, is_admin, register_date)
VALUES ('Brad', 'Traversy', 'brad@gmail.com', '123456','Massachusetts', 'development', 1, now());
```

Inserts one record into the users table. The `now()` function inserts the current timestamp. Column order in the INSERT clause must match the VALUES clause order.

#### Insert Multiple Rows

```sql
INSERT INTO users (first_name, last_name, email, password, location, dept, is_admin, register_date)
VALUES
    ('Fred', 'Smith', 'fred@gmail.com', '123456', 'New York', 'design', 0, now()),
    ('Sara', 'Watson', 'sara@gmail.com', '123456', 'New York', 'design', 0, now()),
    ('Will', 'Jackson', 'will@yahoo.com', '123456', 'Rhode Island', 'development', 1, now()),
    ('Paula', 'Johnson', 'paula@yahoo.com', '123456', 'Massachusetts', 'sales', 0, now()),
    ('Tom', 'Spears', 'tom@yahoo.com', '123456', 'Massachusetts', 'sales', 0, now());
```

Inserts multiple rows in a single statement, which is more efficient than individual INSERT statements. Each set of values is separated by commas.

### Query Operations

#### Select Data

```sql
SELECT * FROM users;
SELECT first_name, last_name FROM users;
```

The first query retrieves all columns from all rows. The second selects only specific columns, reducing data transfer when you don't need all fields.

#### Where Clause Filtering

```sql
SELECT * FROM users WHERE location='Massachusetts';
SELECT * FROM users WHERE location='Massachusetts' AND dept='sales';
SELECT * FROM users WHERE is_admin = 1;
SELECT * FROM users WHERE is_admin > 0;
```

The WHERE clause filters rows based on conditions. Multiple conditions can be combined with AND/OR operators. Comparison operators include =, >, <, >=, <=, and != (not equal).

#### Delete Row

```sql
DELETE FROM users WHERE id = 6;
```

Removes rows matching the WHERE condition. Always include a WHERE clause to avoid deleting all rows. Without WHERE, this would delete every row in the table.

#### Update Row

```sql
UPDATE users SET email = 'freddy@gmail.com' WHERE id = 2;
```

Modifies existing data in rows matching the WHERE condition. You can update multiple columns by separating them with commas: `SET col1='val1', col2='val2'`.

### Table Schema Modifications

#### Add Column

```sql
ALTER TABLE users ADD age VARCHAR(3);
```

Adds a new column to an existing table. The column is added to all rows with NULL values (unless DEFAULT is specified).

#### Modify Column

```sql
ALTER TABLE users MODIFY COLUMN age INT(3);
```

Changes a column's data type or attributes. This can be risky if existing data isn't compatible with the new type.

### Advanced Queries

#### Order By (Sorting)

```sql
SELECT * FROM users ORDER BY last_name ASC;
SELECT * FROM users ORDER BY last_name DESC;
```

Sorts results in ascending (ASC) or descending (DESC) order. You can sort by multiple columns by separating them with commas.

#### Concatenate Columns

```sql
SELECT CONCAT(first_name, ' ', last_name) AS 'Name', dept FROM users;
```

Combines multiple columns into one output column. The AS keyword creates an alias for the result column.

#### Select Distinct Values

```sql
SELECT DISTINCT location FROM users;
```

Returns only unique values, eliminating duplicates. Useful for finding all unique entries in a column.

#### Between Range

```sql
SELECT * FROM users WHERE age BETWEEN 20 AND 25;
```

Filters rows where a value falls within a range (inclusive). Equivalent to `age >= 20 AND age <= 25`.

#### Like Pattern Matching

```sql
SELECT * FROM users WHERE dept LIKE 'd%';      -- Starts with 'd'
SELECT * FROM users WHERE dept LIKE 'dev%';    -- Starts with 'dev'
SELECT * FROM users WHERE dept LIKE '%t';      -- Ends with 't'
SELECT * FROM users WHERE dept LIKE '%e%';     -- Contains 'e'
```

The LIKE operator performs pattern matching. `%` wildcard matches any sequence of characters. `_` wildcard matches a single character.

#### Not Like

```sql
SELECT * FROM users WHERE dept NOT LIKE 'd%';
```

Inverts the LIKE condition, returning rows that don't match the pattern.

#### In List

```sql
SELECT * FROM users WHERE dept IN ('design', 'sales');
```

Filters rows where the column value matches any value in the provided list. More concise than multiple OR conditions.

### Indexes

#### Create and Drop Index

```sql
CREATE INDEX LIndex ON users(location);
DROP INDEX LIndex ON users;
```

Indexes speed up queries on indexed columns but slow down INSERT/UPDATE/DELETE operations. Primary keys automatically have indexes.

### Foreign Keys and Relationships

#### Create Table with Foreign Key

```sql
CREATE TABLE posts(
    id INT AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(100),
    body TEXT,
    publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

Foreign keys enforce referential integrity, ensuring user_id values in posts match existing id values in users. `DEFAULT CURRENT_TIMESTAMP` automatically sets the publish date to the current time.

#### Insert Related Data

```sql
INSERT INTO posts(user_id, title, body) VALUES
    (1, 'Post One', 'This is post one'),
    (3, 'Post Two', 'This is post two'),
    (1, 'Post Three', 'This is post three'),
    (2, 'Post Four', 'This is post four'),
    (5, 'Post Five', 'This is post five'),
    (4, 'Post Six', 'This is post six'),
    (2, 'Post Seven', 'This is post seven'),
    (1, 'Post Eight', 'This is post eight'),
    (3, 'Post Nine', 'This is post none'),
    (4, 'Post Ten', 'This is post ten');
```

Inserts posts associated with specific users via user_id. The foreign key constraint ensures all user_id values exist in the users table.

### Joins

#### Inner Join

```sql
SELECT
    users.first_name,
    users.last_name,
    posts.title,
    posts.publish_date
FROM users
INNER JOIN posts ON users.id = posts.user_id
ORDER BY posts.title;
```

INNER JOIN returns only rows where matching records exist in both tables. This excludes users without posts and posts without valid users.

#### Left Join

```sql
SELECT
    comments.body,
    posts.title
FROM comments
LEFT JOIN posts ON posts.id = comments.post_id
ORDER BY posts.title;
```

LEFT JOIN returns all rows from the left table (comments) and matching rows from the right table (posts). If no match exists, NULL values appear for posts columns.

#### Multiple Table Join

```sql
CREATE TABLE comments(
    id INT AUTO_INCREMENT,
    post_id INT,
    user_id INT,
    body TEXT,
    publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(post_id) REFERENCES posts(id)
);

INSERT INTO comments(post_id, user_id, body) VALUES
    (1, 3, 'This is comment one'),
    (2, 1, 'This is comment two'),
    (5, 3, 'This is comment three'),
    (2, 4, 'This is comment four'),
    (1, 2, 'This is comment five'),
    (3, 1, 'This is comment six'),
    (3, 2, 'This is comment six'),
    (5, 4, 'This is comment seven'),
    (2, 3, 'This is comment seven');

SELECT
    comments.body,
    posts.title,
    users.first_name,
    users.last_name
FROM comments
INNER JOIN posts ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id
ORDER BY posts.title;
```

Multiple joins connect three tables, showing comment text with the associated post title and commenter's name. Each JOIN condition specifies how tables relate to each other.

### Aggregate Functions

```sql
SELECT COUNT(id) FROM users;                              -- Count rows
SELECT MAX(age) FROM users;                               -- Maximum value
SELECT MIN(age) FROM users;                               -- Minimum value
SELECT SUM(age) FROM users;                               -- Sum of values
SELECT UCASE(first_name), LCASE(last_name) FROM users;   -- Text case conversion
```

Aggregate functions perform calculations across multiple rows. COUNT, MAX, MIN, and SUM operate on numeric values. UCASE and LCASE transform text case.

### Group By

```sql
SELECT age, COUNT(age) FROM users GROUP BY age;
SELECT age, COUNT(age) FROM users WHERE age > 20 GROUP BY age;
SELECT age, COUNT(age) FROM users GROUP BY age HAVING COUNT(age) >= 2;
```

GROUP BY combines rows with identical values in specified columns. HAVING filters groups after aggregation (whereas WHERE filters before aggregation). These queries count how many users have each age value.

---

## Key Concepts

### LAMP Stack Architecture

**Linux Foundation**: The operating system layer provides stability, security, and process management. Linux's open-source nature and strong networking capabilities make it ideal for web servers.

**Apache Web Server**: Handles HTTP/HTTPS requests, serves static content, and passes dynamic content to PHP. Apache's modular architecture allows customization through modules like mod_rewrite and mod_ssl.

**MySQL/MariaDB Database**: Stores and manages relational data. MariaDB maintains MySQL compatibility while offering enhanced performance, additional storage engines, and active community development.

**PHP Interpreter**: Server-side scripting language that generates dynamic content. PHP scripts can query databases, process forms, and generate HTML based on business logic.

### Request Flow in LAMP

**Client Request**: Browser sends HTTP request to Apache on port 3003 (or configured port). Apache receives and parses the request.

**Apache Processing**: Apache determines if the requested resource is static (HTML, CSS, images) or dynamic (PHP script). Static files are served directly.

**PHP Execution**: For PHP files, Apache passes the request to the PHP interpreter. PHP executes the script, which may include database queries.

**Database Interaction**: PHP connects to MariaDB using mysqli extension, executes queries, and receives results. Connection pooling and persistent connections improve performance.

**Response Generation**: PHP generates HTML output based on database results and business logic. Apache receives the generated content and sends it to the client.

### Database Security

**Remote Access Control**: The `'user'@'%'` syntax allows connections from any host, necessary for applications on separate servers. For improved security, replace '%' with specific IP addresses or hostnames.

**Localhost Restriction**: `'user'@'localhost'` restricts connections to the database server itself, providing stronger security for applications co-located with the database.

**Network Security**: Use `'user'@'192.168.1.%'` to allow connections from a specific subnet, balancing security with flexibility for multiple application servers.

**SSL/TLS Encryption**: Configure MySQL to require encrypted connections for remote access, protecting credentials and data from network sniffing: `REQUIRE SSL` in GRANT statements.

### Performance Optimization

**Connection Pooling**: Applications should reuse database connections rather than opening new connections for each request. PHP's mysqli persistent connections (mysqli_connect with 'p:' prefix) enable this.

**Query Optimization**: Use indexes on frequently queried columns, avoid SELECT *, and optimize WHERE clauses. Use EXPLAIN to analyze query execution plans.

**Caching Strategies**: Implement Redis or Memcached to cache frequently accessed data, reducing database load. Apache's mod_cache can cache generated pages.

**Load Balancing**: Distribute traffic across multiple Apache servers using a load balancer (like NGINX). Database replication allows read queries to be distributed across replica servers.

### Port Configuration

**Default Ports**: Apache typically uses port 80 (HTTP) and 443 (HTTPS). Custom ports like 3003 are used when multiple web servers run on the same host or when standard ports are blocked.

**Port Changes**: Modify the `Listen` directive in httpd.conf. Also update any VirtualHost declarations to match. Firewall rules must allow traffic on the custom port.

**SELinux Considerations**: On SELinux-enabled systems, use `semanage port -a -t http_port_t -p tcp 3003` to allow Apache to bind to non-standard ports.

**Testing**: After changing ports, test with `curl http://localhost:3003` from the server and from remote clients to verify accessibility.

### MariaDB vs MySQL

**Compatibility**: MariaDB is a drop-in replacement for MySQL, maintaining protocol and API compatibility. Most MySQL applications work without modification.

**Performance**: MariaDB includes optimizations like Aria storage engine, thread pool, and improved query optimizer for better performance under high load.

**Storage Engines**: MariaDB supports additional storage engines including ColumnStore for analytics, Spider for sharding, and MyRocks for write-intensive workloads.

**Development**: MariaDB has faster feature release cycles and more transparent development. MySQL is owned by Oracle, while MariaDB is community-driven.

---

## Validation

Test your solution using KodeKloud's automated validation. Verify the application can connect to the database by accessing the web interface through the load balancer.

---

[← Day 17](day-17.md) | [Day 19 →](day-19.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
