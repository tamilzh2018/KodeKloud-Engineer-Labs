## Task: Managing Secrets with Azure Key Vault
The Nautilus DevOps team is focusing on improving their data security by using Azure Key Vault. Your task is to create a Key Vault with a key and manage the encryption and decryption of a pre-existing sensitive file using this key.

**Specific Requirements:**

1. Create a Key Vault:
    - Name the Key Vault `datacenter-22709`.
    - Set access policies to allow encryption and decryption operations.
    - Set Soft Delete retention to 7 days.
2. Create a Key:
    - Create a symmetric key named `datacenter-key` within the Key Vault for encryption and decryption operations.
3. Encrypt the Sensitive Data:
    - Use the key to encrypt the provided `SensitiveData.txt` file (located in `/root/`) on the `azure-client` host.
    - Base64 encode the ciphertext and save the encrypted version as `EncryptedData.bin` in the `/root/` directory.
4. Verify Decryption:
    - Attempt to decrypt `EncryptedData.bin` and verify that the decrypted data matches the original `SensitiveData.txt` file.

---

## Solution

We'll be performing this task using Azure CLI.

### **Step 1: Login to Azure CLI**
```bash
az login
```
Follow the instructions and ensure that you are logged in.

### **Step 2: Set Variables**
Define variables for easier management:
```bash
RESOURCE_GROUP=$(az group list --query "[0].name" -o tsv)
USER_NAME=$(az account show --query user.name -o tsv)
KEY_VAULT="datacenter-22709"
KEY_NAME="datacenter-key"
```

### **Step 3: Create the Key Vault**
```bash
az keyvault create \
  --name $KEY_VAULT \
  --resource-group $RESOURCE_GROUP \
  --location "East US" \
  --retention-days 7 \
  --enable-rbac-authorization false
```

### **Step 4: Set Access Policies**
```bash
az keyvault set-policy \
  --name $KEY_VAULT \
  --upn $USER_NAME \
  --key-permissions all
```

### **Step 5: Create Key**
```bash
az keyvault key create \
  --vault-name $KEY_VAULT \
  --name $KEY_NAME \
  --kty RSA \
  --size 2048
```

### **Step 6: Encrypt and save file**
Base64 encode the file
```bash
base64 /root/SensitiveData.txt > /root/plain.b64
```
Encrypt using key generated in Step 4
```bash
az keyvault key encrypt \
  --vault-name $KEY_VAULT \
  --name $KEY_NAME \
  --algorithm RSA-OAEP \
  --value "$(cat /root/plain.b64)" \
  --query result -o tsv \
  > /root/EncryptedData.b64
```
Save the encrypted version
```bash
base64 -d /root/EncryptedData.b64 > /root/EncryptedData.bin
```

### **Step 7: Decrypt File**
Decrypt using key generated in Step 4
```bash
az keyvault key decrypt \
  --vault-name $KEY_VAULT \
  --name $KEY_NAME \
  --algorithm RSA-OAEP \
  --value "$(cat /root/EncryptedData.b64)" \
  --query result -o tsv \
  > /root/DecryptedData.b64
```
Save the decrypted version
```bash
base64 -d /root/DecryptedData.b64 > /root/DecryptedData.txt
```

### **Step 8: Verify Decrypted Data Matches Original**
Compare the original and decrypted files:
```bash
diff /root/SensitiveData.txt /root/DecryptedData.txt
# If no output, files are identical

echo "Files comparison result: $?"
# 0 means identical, non-zero means different

# Compare using checksums
echo "Original file MD5:"
md5sum /root/SensitiveData.txt

echo "Decrypted file MD5:"
md5sum /root/DecryptedData.txt
```
