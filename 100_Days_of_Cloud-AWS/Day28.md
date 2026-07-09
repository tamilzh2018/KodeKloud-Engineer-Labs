## Task: Creating a Private ECR Repository
The Nautilus DevOps team has been tasked with setting up a containerized application. They need to create a private Amazon Elastic Container Registry (ECR) repository to store their Docker images. Once the repository is created, they will build a Docker image from a Dockerfile located on the `aws-client` host and push this image to the ECR repository. This process is essential for maintaining and deploying containerized applications in a streamlined manner.

Create a private ECR repository named `xfusion-ecr`. There is a Dockerfile under `/root/pyapp` directory on `aws-client` host, build a docker image using this Dockerfile and push the same to the newly created ECR repo, the image tag must be `latest`.

---

## Solution

### Step 1: Set Variables
```bash
ECR_REPO="xfusion-ecr"
```

### Step 2: Create the private ECR repository
```bash
aws ecr create-repository --repository-name $ECR_REPO
```
Capture your AWS account ID and region
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
REGION=$(aws configure get region)
```

### Step 3: Authenticate Docker to ECR
```bash
aws ecr get-login-password --region $REGION \
  | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

### Step 4: Build the Docker image
```bash
# Go to the directory containing the Dockerfile
cd /root/pyapp
# Build image
docker build -t $ECR_REPO:latest .
```

### Step 5: Tag the image for ECR
```bash
docker tag $ECR_REPO:latest \
  $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO:latest
```

### Step 6: Push the image to ECR
```bash
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO:latest
```