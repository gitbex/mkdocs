# **Blue-Green Deployment Documentation**

## Overview

This documentation covers the Blue-Green deployment strategy integrated into our Django backend project. We maintain two parallel environments to alternate deployments:

- **Green** environment (Branch: `green`)
- **Blue** environment (Branch: currently `production`, soon to be renamed to `blue`)

### Goals

- Ensure zero-downtime deployments.
- Minimize deployment risks through alternating deployments.
- Allow rapid rollback in case of deployment issues.

## Branch Structure

- **Green branch** (`green`):
    - Alternately used with Blue for deploying and testing new versions.
    - New deployments are validated here before switching live traffic.
- **Blue branch** (currently `production`, to be renamed `blue`):
    - Alternately used with Green for deploying and testing new versions.
    - Initially stable environment handling live traffic, also used for alternating deployments.

## Current Deployment Color

You can check the currently active deployment color by visiting:

```
https://api.datatruck.io/deployment/color/

```

The response will be in JSON format, indicating the active color:

```json
{
  "color": "green"
}

```

## Deployment Workflow

### Step-by-Step Deployment Process

### 1. Develop and Test

- Develop and test features/fixes in dedicated feature branches.
- Merge validated features/fixes alternately into the `green` or `production` (`blue`) branch based on the current active environment.

### 2. Deploy to the Inactive Environment

- Trigger deployment manually from GitHub Actions:
    - Identify the current inactive environment (`green` or `production`/`blue`).
    - Navigate to GitHub repository > Actions > Workflow: **Deployment to Green** or **Deployment to Blue** accordingly.
    - Run the workflow and wait for successful deployment and testing.

### 3. Verification in the Inactive Environment

- Perform thorough automated tests and manual QA checks in the inactive environment.

### 4. Switch Traffic

- Once verified, manually switch DNS traffic to the newly validated environment:
    - Navigate to GitHub repository > Actions > Workflow: **DNS Update**
    - Choose the verified environment (`green` or `blue`) and execute the workflow.

### 5. Post-switch Monitoring

- Monitor application closely for performance, errors, and unexpected behavior under real traffic.

### 6. Sync Environments

- After successful monitoring, optionally synchronize the inactive environment to reflect the stable state for future deployments.

### Rollback Procedure

- If issues arise in the newly active environment:
    1. Immediately switch DNS traffic back to the previous stable environment:
        - Navigate to GitHub Actions > Workflow: **DNS Update**
        - Select the previously stable environment (`green` or `blue`) and execute.
    2. Diagnose and fix issues in the inactive environment without impacting users.

## GitHub Actions Workflows

- **Deployment to Green**:
    - Deploys code from `green` branch to Green environment.
- **Deployment to Blue**:
    - Deploys code from `production` branch (soon `blue`) to Blue environment.
- **DNS Update**:
    - Manually triggered to switch live traffic between Blue and Green environments.

## Best Practices

- Always conduct thorough testing in the inactive environment before switching traffic.
- Maintain regular synchronization between environments.
- Document all deployments and monitor closely post-deployment.

## Future Updates

- Rename `production` branch to `blue` to reflect its role clearly.
- Update all documentation and CI/CD configurations accordingly.