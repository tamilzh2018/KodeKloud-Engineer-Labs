## Task: Building and Managing NoSQL Databases with AWS DynamoDB
The Nautilus DevOps team is developing a simple 'To-Do' application using DynamoDB to store and manage tasks efficiently. The team needs to create a DynamoDB table to hold tasks, each identified by a unique task ID. Each task will have a description and a status, which indicates the progress of the task (e.g., 'completed' or 'in-progress').

Your task is to:
1. Create a DynamoDB table named `nautilus-tasks` with a primary key called `taskId` (string).
2. Insert the following tasks into the table:
    - **Task 1**: `taskId`: '1', `description`: 'Learn DynamoDB', `status`: 'completed'
    - **Task 2**: `taskId`: '2', `description`: 'Build To-Do App', `status`: 'in-progress'
3. Verify that **Task 1** has a status of **'completed'** and **Task 2** has a status of **'in-progress'**.

Ensure the DynamoDB table is created successfully and that both tasks are inserted correctly with the appropriate statuses.

---

## Solution

### Step 1: Set Variables
```bash
TABLE_NAME="nautilus-tasks"
PRIMARY_KEY="taskId"
```


### Step 2: Create the DynamoDB table
```bash
aws dynamodb create-table \
    --table-name $TABLE_NAME \
    --attribute-definitions AttributeName=$PRIMARY_KEY,AttributeType=S \
    --key-schema AttributeName=$PRIMARY_KEY,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

### Step 3: Insert tasks into the table
Insert **Task 1**
```bash
aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{"taskId": {"S": "1"}, "description": {"S": "Learn DynamoDB"}, "status": {"S": "completed"}}'
```
Insert **Task 2**
```bash
aws dynamodb put-item \
    --table-name $TABLE_NAME \
    --item '{"taskId": {"S": "2"}, "description": {"S": "Build To-Do App"}, "status": {"S": "in-progress"}}'
```

### Step 4: Verify the inserted tasks
**Task 1** - status should be **'completed'**
```bash
aws dynamodb get-item \
    --table-name $TABLE_NAME \
    --key '{"taskId": {"S": "1"}}' \
    --query 'Item.status.S' \
    --output text
```
**Task 2** - status should be **'in-progress'**
```bash
aws dynamodb get-item \
    --table-name $TABLE_NAME \
    --key '{"taskId": {"S": "2"}}' \
    --query 'Item.status.S' \
    --output text
```