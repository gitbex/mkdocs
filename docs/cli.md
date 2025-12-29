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

# Configuration
MFA_SERIAL="arn:aws:iam::ACCOUNT_ID:mfa/USERNAME"
BASE_PROFILE="your-profile"

# Get MFA code
read -p "Enter MFA code: " MFA_CODE

# Get credentials
echo "Getting credentials..."
OUTPUT=$(aws sts get-session-token \
  --serial-number $MFA_SERIAL \
  --token-code $MFA_CODE \
  --duration-seconds 129600 \
  --profile $BASE_PROFILE)

# Export to environment
export AWS_ACCESS_KEY_ID=$(echo $OUTPUT | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo $OUTPUT | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo $OUTPUT | jq -r '.Credentials.SessionToken')

echo "✅ Done! Credentials valid for 36 hours"
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