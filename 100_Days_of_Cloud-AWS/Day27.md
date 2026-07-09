## Task: Configuring a Public VPC with an EC2 Instance for Internet Access
The Nautilus DevOps Team has received a request from the Networking Team to set up a new public VPC to support a set of public-facing services. This VPC will host various resources that need to be accessible over the internet. As part of this setup, you need to ensure the VPC has public subnets with automatic IP assignment for resources. Additionally, a new EC2 instance will be launched within this VPC to host public applications that require SSH access. This setup will enable the Networking Team to deploy and manage public-facing applications.

Create a public VPC named `devops-pub-vpc`, and a subnet named `devops-pub-subnet` under the same, make sure public IP is being auto assigned to resources under this subnet. Further, create an EC2 instance named `devops-pub-ec2` under this VPC. Make sure SSH port `22` is open for this instance and accessible over the internet.

---

## Solution

### Step 1: Set variables
```bash
VPC_NAME="devops-pub-vpc"
SUBNET_NAME="devops-pub-subnet"
EC2_NAME="devops-pub-ec2"
REGION="us-east-1"
CIDR_VPC="10.0.0.0/16"
CIDR_SUBNET="10.0.1.0/24"
```

### Step 2: Create VPC
```bash
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block "$CIDR_VPC" \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$VPC_NAME}]" \
  --query "Vpc.VpcId" \
  --output text)

echo "VPC ID: $VPC_ID"
```
Enable DNS hostnames
```bash
aws ec2 modify-vpc-attribute \
  --vpc-id "$VPC_ID" \
  --enable-dns-hostnames
```

### Step 3: Create Public Subnet (with Auto-assign Public IP)
```bash
SUBNET_ID=$(aws ec2 create-subnet \
  --vpc-id "$VPC_ID" \
  --cidr-block "$CIDR_SUBNET" \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$SUBNET_NAME}]" \
  --query "Subnet.SubnetId" \
  --output text)

echo "Subnet ID: $SUBNET_ID"
```
Enable auto-assign public IP
```bash
aws ec2 modify-subnet-attribute \
  --subnet-id "$SUBNET_ID" \
  --map-public-ip-on-launch
```

### Step 4: Create an Internet Gateway
```bash
IGW_ID=$(aws ec2 create-internet-gateway \
  --query "InternetGateway.InternetGatewayId" \
  --output text)

# Attach internet gateway to VPC
aws ec2 attach-internet-gateway \
  --internet-gateway-id "$IGW_ID" \
  --vpc-id "$VPC_ID"

echo "IGW ID: $IGW_ID"
```

### Step 5: Create Route Table + Route to Internet
```bash
RT_ID=$(aws ec2 create-route-table \
  --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${VPC_NAME}-rt}]" \
  --query "RouteTable.RouteTableId" \
  --output text)

# Associate route table
aws ec2 associate-route-table \
  --route-table-id "$RT_ID" \
  --subnet-id "$SUBNET_ID"

# Create route rule to internet via internet gateway
aws ec2 create-route \
  --route-table-id "$RT_ID" \
  --destination-cidr-block "0.0.0.0/0" \
  --gateway-id "$IGW_ID"
```

### Step 6: Create Security Group with SSH Open
```bash
SG_ID=$(aws ec2 create-security-group \
  --group-name "devops-pub-sg" \
  --description "Public EC2 SG with SSH access" \
  --vpc-id "$VPC_ID" \
  --query "GroupId" --output text)

aws ec2 authorize-security-group-ingress \
  --group-id "$SG_ID" \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

echo "Security Group: $SG_ID"
```

### Step 7: Fetch AMI ID
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

### Step 8: Launch EC2 Instance in the Public Subnet
```bash
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type t2.micro \
  --subnet-id "$SUBNET_ID" \
  --security-group-ids "$SG_ID" \
  --associate-public-ip-address \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$EC2_NAME}]" \
  --query "Instances[0].InstanceId" \
  --output text)

echo "EC2 Instance ID: $INSTANCE_ID"
```

### Step 9: Verfication - Check if the instance is assigned a public IP
```bash
aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --output text
```