# AWS MFA Setup Guide

All users must enable Multi-Factor Authentication (MFA) to access AWS resources.

**Without MFA, you will see "Access Denied" errors** for most AWS services.  
You'll only be able to set up MFA until it's enabled.

---

## Before You Start

**You'll need:**  
- Your AWS username and password  
- A smartphone with one of these apps installed:  
  - Google Authenticator (recommended)  
  - Microsoft Authenticator  
  - Authy

**Time needed:** 5 minutes

---

## Setup Instructions

### Step 1: Click "Add MFA" on the Dashboard

1. Log into AWS Console: `https://629070900093.signin.aws.amazon.com/console`
2. After logging in, you'll see the IAM Dashboard
3. Look for the orange **"Add MFA"** button in the "Security recommendations" section (see Image 1)
4. Click **Add MFA**

<figure markdown="span">
  ![add MFA](../../assets/1.png){ width="600" }
</figure>

> **What you'll see:** The IAM Dashboard will show "Add MFA for" button.

---

### Step 2: Choose Your MFA Device Type

You'll see the "Select MFA device" page with two steps on the left.

**Fill in the form:**

1. **Device name:** Type a name like "My Phone" or "iPhone"
2. **MFA device:** Select **"Authenticator app"** or other option
3. Click **Next**

!!! info "What you'll see"
    Three device options:  
    - Passkey  
    - Authenticator app  
    - Hardware token
---

### Step 3: Scan QR Code with Your Phone

The next screen shows a QR code.

**On your phone:**  
1. Open your authenticator app (Google Authenticator, etc.)  
2. Tap the **+** or "Add account" button  
3. Choose **"Scan QR code"**  
4. Point your camera at the QR code on your computer screen  
5. The app will automatically add "AWS:your-username"  

**Now you'll see a 6-digit code in your app that changes every 30 seconds.**

---

### Step 4: Enter Two MFA Codes

Back on your computer:

1. Look at your authenticator app - copy the 6-digit code
2. Enter it in **"MFA code 1"**
3. **Wait 30 seconds** for the code to change
4. Enter the new code in **"MFA code 2"**
5. Click **Add MFA**

!!! note "Important"
    You must use two different codes.  
    If the code changes while you're typing, start over with the new code

---

### Step 5: Success! MFA is Enabled

You'll see a green banner at the top: **"Passkey MFA device assigned"**

The page will show your security credentials without any "Access Denied" errors.

> **What you'll see:** Green success message at the top and "Console password" section will no longer show access denied errors (see Image 2).

<figure markdown="span">
  ![success](/assets/3.png){ width="600" }
</figure>

**That's it! MFA is now enabled.**

---

### Testing Your MFA

To make sure everything works:

1. Click your username (top right) → **Sign out**
2. Log in again with:
   - Your username
   - Your password  
   - **6-digit code from your authenticator app**
3. You should now have full access without "Access Denied" errors!

---

### Daily Login After MFA is Enabled

From now on, when you log in:

1. Enter your **username**
2. Enter your **password**
3. Open your authenticator app and enter the **6-digit code**
4. Click **Sign In**

The code changes every 30 seconds, so type it quickly!

---

### Troubleshooting

####  Invalid MFA code - error

**Try this:**
- Wait for a new code (they expire every 30 seconds)
- Make sure your phone's time is set to **automatic**
- Don't use the same code twice

####  Lost your phone or got a new one

Contact your AWS administrator to help you remove the old device and set up a new one.

####  Still seeing 'Access Denied' after setup

1. Log out completely
2. Log back in with username + password + MFA code
3. If still blocked, contact your AWS administrator

---

### Need Help?

**Common Questions:**

**Q: Can I use text messages instead of an app?**  
A: No, we require authenticator apps for better security.

**Q: What if I don't set up MFA?**  
A: You'll be locked out of AWS until you complete the setup.

**Q: My code doesn't work!**  
A: Make sure your phone's time is set to automatic and wait for a fresh code.

**Q: I lost my phone, what do I do?**  
A: Contact your AWS administrator immediately to reset your MFA device.

---

**Need help?** Contact your AWS administrator.  

[Link to official workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/18b3622c-5d4c-45c9-9834-6a7091109072/en-US/advanced-modules/10-mfa/1-1)
