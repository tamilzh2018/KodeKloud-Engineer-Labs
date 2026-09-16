## Task: Integrating AWS SQS and SNS for Reliable Messaging
The xfusion DevOps team needs to implement a Lambda function using a CloudFormation stack. Create a CloudFormation template named `/root/xfusion-lambda.yml` on the AWS client host and configure it to create the following components. The stack name must be `xfusion-lambda-app`.
1. Create a Lambda function named `xfusion-lambda`.
2. Use the Runtime `Python`.
3. The function should print the body `Welcome to KKE AWS Labs!`.
4. Ensure the status code is `200`.
5. Create and use the IAM role named `lambda_execution_role`.

---

## Solution

### Step 1: Create the `/root/xfusion-lambda.yml` file on AWS client host:
```bash
vi /root/xfusion-lambda.yml
```
Add the following content
```yml
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation stack to create a basic Lambda function

Resources:

  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: lambda_execution_role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  xfusionLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: xfusion-lambda
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      MemorySize: 128
      Timeout: 10
      Code:
        ZipFile: |
          def lambda_handler(event, context):
              return {
                  "statusCode": 200,
                  "body": "Welcome to KKE AWS Labs!"
              }
```

### Step 2: Create the stack
```bash
aws cloudformation create-stack \
  --stack-name xfusion-lambda-app \
  --template-body file:///root/xfusion-lambda.yml \
  --capabilities CAPABILITY_NAMED_IAM
```
Wait for it to be created
```bash
aws cloudformation wait stack-create-complete \
  --stack-name xfusion-lambda-app
```

### Step 3: Verification
Invoke the function
```bash
aws lambda invoke \
  --function-name xfusion-lambda \
  response.json
```
Check the output - expected output:
aws lambda get-function-configuration \
  --function-name xfusion-lambda

cat response.json

```json
{
  "statusCode": 200,
  "body": "Welcome to KKE AWS Labs!"
}
```
