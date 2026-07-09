## Task: Setting Up an EC2 Instance with an Elastic IP for Application Hosting
The Nautilus DevOps Team has received a new request from the Development Team to set up a new EC2 instance. This instance will be used to host a new application that requires a stable IP address. To ensure that the instance has a consistent public IP, an Elastic IP address needs to be associated with it. The instance will be named `datacenter-ec2`, and the Elastic IP will be named `datacenter-eip`. This setup will help the Development Team to have a reliable and consistent access point for their application.

Create an EC2 instance named `datacenter-ec2` using any linux AMI like ubuntu, the Instance type must be `t2.micro` and associate an `Elastic IP` address with this instance, name it as `datacenter-eip`.

---

## Solution

We'll be performing the task using AWS CLI

### Step 1: Set variables
```bash
EC2_NAME="datacenter-ec2"
EC2_TYPE="t2.micro"
EIP_NAME="datacenter-eip"
REGION="us-east-1"
```

### Step 2: Fetch AMI ID
Get AMI ID of `Ubuntu 22.04` image in `us-east-1` region
```bash
AMI_ID=$(aws ec2 describe-images \
  --region $REGION \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" "Name=state,Values=available" \
  --query "sort_by(Images, &CreationDate)[-1].ImageId" \
  --output text
)
```

### Step 3: Launch the EC2 Instance
```bash
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type "$EC2_TYPE" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$EC2_NAME}]" \
  --query "Instances[0].InstanceId" \
  --output text)

echo "Instance ID: $INSTANCE_ID"
```

### Step 4: Allocate a New Elastic IP
```bash
ALLOC_ID=$(aws ec2 allocate-address \
  --domain vpc \
  --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=Name,Value=$EIP_NAME}]" \
  --query "AllocationId" \
  --output text)

echo "Elastic IP Allocation ID: $ALLOC_ID"
```

### Step 5: Associate the Elastic IP with the Instance
```bash
aws ec2 associate-address \
  --instance-id "$INSTANCE_ID" \
  --allocation-id "$ALLOC_ID"
```

### Step 6: Verify if instance public IP matches with EIP
Fetch instance public IP
```bash
aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --output text
```

Fetch EIP
```bash
aws ec2 describe-addresses \
  --allocation-ids "$ALLOC_ID" \
  --query "Addresses[0].PublicIp" \
  --output text
```
![verify](assets/day21_01.png)