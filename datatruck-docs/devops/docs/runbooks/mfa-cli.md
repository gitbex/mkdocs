# AWS MFA Authentication Guide

Quick guide for authenticating with AWS using Multi-Factor Authentication (MFA).

## Prerequisites

- AWS CLI installed
- MFA device configured
- `jq` installed (for scripts)

---

## Three Ways to Authenticate

Get MFA device Identifier
```bash
aws iam list-mfa-devices --user-name some-user --profile datatruck
```

### Option 1: Environment Variables (Fastest)

#### Step 1: Get credentials

```bash
aws sts get-session-token \
  --serial-number arn:aws:iam::ACCOUNT_ID:mfa/USERNAME \
  --token-code 123456 \
  --duration-seconds 129600 \
  --profile YOUR_PROFILE
```

#### Step 2: Export to terminal

```bash
export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
```

#### Step 3: Use AWS CLI

```bash
aws lambda list-functions
aws s3 ls
```

!!! note
    Lost when terminal closes

---

### Option 2: Automated Script (Recommended)

**Best for: Daily development work**

#### Create script `~/aws-mfa.sh`

```BASH
#!/bin/bash
# --- Configuration ---
MFA_SERIAL="arn:aws:iam::629070900093:mfa/<DEVICE_NAME_HERE>"
BASE_PROFILE="datatruck"      # Profile with permanent credentials
MFA_PROFILE="default"         # Profile for MFA session credentials
# ---------------------

# Get MFA code from user
read -p "Enter MFA code: " MFA_CODE

# Call AWS STS
echo "⏳ Authenticating with AWS..."
JSON_OUTPUT=$(aws sts get-session-token \
  --serial-number "$MFA_SERIAL" \
  --token-code "$MFA_CODE" \
  --duration-seconds 129600 \
  --profile "$BASE_PROFILE" 2>&1)

# Check if the AWS command succeeded
if [ $? -ne 0 ]; then
    echo "❌ AWS Error:"
    echo "$JSON_OUTPUT"
    exit 1
fi

# Extract credentials
ACCESS_KEY=$(echo "$JSON_OUTPUT" | jq -r '.Credentials.AccessKeyId')
SECRET_KEY=$(echo "$JSON_OUTPUT" | jq -r '.Credentials.SecretAccessKey')
SESSION_TOKEN=$(echo "$JSON_OUTPUT" | jq -r '.Credentials.SessionToken')

# Write to default profile
aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$MFA_PROFILE"
aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$MFA_PROFILE"
aws configure set aws_session_token "$SESSION_TOKEN" --profile "$MFA_PROFILE"

# Verify it worked
echo "✅ Success! MFA credentials saved to profile '$MFA_PROFILE'"
echo "   Account: $(aws sts get-caller-identity --profile "$MFA_PROFILE" --query Account --output text)"
echo "   Expires in: 36 hours"
echo ""
echo "💡 Now you can run: aws s3 ls"
```

#### Make executable and use

```bash
chmod +x ~/aws-mfa.sh

# Run with source
source ~/aws-mfa.sh

# Or create alias
echo 'alias aws-mfa="source ~/aws-mfa.sh"' >> ~/.bashrc
```

!!! note
    Need to run in each new terminal

---

### Option 3: Named Profile

**Multiple accounts, persistent credentials**

#### Step 1: Get credentials

```bash
aws sts get-session-token \
  --serial-number arn:aws:iam::ACCOUNT_ID:mfa/USERNAME \
  --token-code 123456 \
  --duration-seconds 129600 \
  --profile YOUR_PROFILE
```

#### Step 2: Add to `~/.aws/credentials`

```ini
[your-profile-mfa]
aws_access_key_id = ASIA...
aws_secret_access_key = ...
aws_session_token = ...
```

#### Step 3: Use with profile flag

```bash
aws lambda list-functions --profile your-profile-mfa
```

!!! note
    Persists across terminals, works with all tools  

---


## Common Issues

#### MultiFactorAuthentication failed

- MFA code expired (try a fresh one)
- Check system time: `date`
- Verify MFA device: `aws iam list-mfa-devices --user-name USERNAME`

#### ExpiredToken error

Your credentials expired. Re-run the authentication with a new MFA code.

#### Find your MFA device ARN

```bash
aws iam list-mfa-devices --user-name USERNAME
```

---

## Security Tips

- Maximum duration: 36 hours (129600 seconds)
- Never commit credentials to git
- Use separate profiles for different accounts
- Credentials auto-expire (safer than permanent keys)

---

## Team Setup

**Recommended profile naming:**

```ini
[datatruck]           # Base credentials
[datatruck-mfa]       # Temporary MFA credentials

[production]          # Base credentials  
[production-mfa]      # Temporary MFA credentials
```