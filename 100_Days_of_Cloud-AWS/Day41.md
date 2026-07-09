## Task: Securing Data with AWS KMS
The Nautilus DevOps team is focusing on improving their data security by using AWS KMS. Your task is to create a KMS key and manage the encryption and decryption of a pre-existing sensitive file using the KMS key.

**Specific Requirements:**
1. Create a symmetric KMS key named `devops-KMS-Key` to manage encryption and decryption.
2. Encrypt the provided `SensitiveData.txt` file (located in `/root/`), base64 encode the ciphertext, and save the encrypted version as `EncryptedData.bin` in the `/root/` directory.
3. Try to decrypt the same and verify that the decrypted data matches the original file.
Make sure that the KMS key is correctly configured. The validation script will test your configuration by decrypting the `EncryptedData.bin` file using the KMS key you created.

---

## Solution

### Step 1: Set Variables
```bash
KMS_KEY="devops-KMS-Key"
```

### Step 2: Create a symmetric KMS key
Create symmetric KMS key
```bash
KEY_ID=$(aws kms create-key \
    --description "KMS key for encryption/decryption" \
    --key-usage ENCRYPT_DECRYPT \
    --origin AWS_KMS \
    --query "KeyMetadata.KeyId" \
    --output text)
```
Create alias for the Key
```bash
aws kms create-alias \
    --alias-name alias/$KMS_KEY \
    --target-key-id $KEY_ID
```

### Step 3: Encrypt the file
```bash
aws kms encrypt \
    --key-id alias/$KMS_KEY \
    --plaintext fileb:///root/SensitiveData.txt \
    --output text \
    --query CiphertextBlob | base64 --decode > /root/EncryptedData.bin
```

### Step 4: Decrypt the file to verify
```bash
aws kms decrypt \
    --key-id alias/$KMS_KEY \
    --ciphertext-blob fileb:///root/EncryptedData.bin \
    --output text \
    --query Plaintext | base64 --decode > /root/DecryptedData.txt
```
Check that the decrypted file matches the original
```bash
# If there is no output, the files match perfectly
diff /root/SensitiveData.txt /root/DecryptedData.txt
```
*OR* use `cat` command to view and verify contents of both the files manually.