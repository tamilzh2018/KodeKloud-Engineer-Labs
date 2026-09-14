# Day 45: Configure NAT Gateway for Internet Access in a Private VPC
The Nautilus DevOps team is tasked with enabling internet access for an EC2 instance running in a private subnet. This instance should be able to upload a test file to a public S3 bucket once it can access the internet. To achieve this, the team must set up a NAT Gateway in a public subnet within the same VPC.

1) A VPC named xfusion-priv-vpc and a private subnet xfusion-priv-subnet have already been created.
2) An EC2 instance named xfusion-priv-ec2 is already running in the private subnet.
3) The EC2 instance is configured with a cron job that uploads a test file to a bucket xfusion-nat-429519121 once internet is accessible.

Your task is to:

Create a public subnet named xfusion-pub-subnet in the same VPC.
Create an Internet Gateway and attach it to the VPC.
Create a route table xfusion-pub-rt and associate it with the public subnet.
Allocate an Elastic IP and create a NAT Gateway named xfusion-natgw.
Create a new, dedicated private route table named xfusion-priv-rt (do not reuse or edit the VPC's Main route table), explicitly associate it with the private subnet xfusion-priv-subnet, and add a route for 0.0.0.0/0 via the NAT Gateway.
Once complete, verify that the EC2 instance can reach the internet by confirming the presence of the test file in the S3 bucket xfusion-nat-429519121. After completing all the configuration, please wait a few minutes for the test file to appear in the bucket, as it may take 2–3 minutes.

# Solution:

# 1. Retrieve the VPC ID
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=xfusion-priv-vpc" --query "Vpcs[0].VpcId" --output text)

# 2. Create the Public Subnet
PUB_SUBNET_ID=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.1.2.0/24 --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=xfusion-pub-subnet}]' --query "Subnet.SubnetId" --output text)

# 3. Create and Attach the Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=xfusion-igw}]' --query "InternetGateway.InternetGatewayId" --output text)
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID

# 4. Create Public Route Table, Add Route to IGW, and Associate with Public Subnet
PUB_RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=xfusion-pub-rt}]' --query "RouteTable.RouteTableId" --output text)
aws ec2 create-route --route-table-id $PUB_RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
aws ec2 associate-route-table --subnet-id $PUB_SUBNET_ID --route-table-id $PUB_RT_ID

# 5. Allocate Elastic IP and Create NAT Gateway
EIP_ALLOC_ID=$(aws ec2 allocate-address --domain vpc --query "AllocationId" --output text)
NATGW_ID=$(aws ec2 create-nat-gateway --subnet-id $PUB_SUBNET_ID --allocation-id $EIP_ALLOC_ID --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=xfusion-natgw}]' --query "NatGateway.NatGatewayId" --output text)

# Wait for NAT Gateway to become active
aws ec2 wait nat-gateway-available --nat-gateway-ids $NATGW_ID

# 6. Retrieve Private Subnet ID
PRIV_SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=tag:Name,Values=xfusion-priv-subnet" --query "Subnets[0].SubnetId" --output text)

# 7. Create Private Route Table, Add Route to NAT Gateway, and Associate with Private Subnet
PRIV_RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=xfusion-priv-rt}]' --query "RouteTable.RouteTableId" --output text)
aws ec2 create-route --route-table-id $PRIV_RT_ID --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NATGW_ID
aws ec2 associate-route-table --subnet-id $PRIV_SUBNET_ID --route-table-id $PRIV_RT_ID