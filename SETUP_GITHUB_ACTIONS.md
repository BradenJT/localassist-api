# GitHub Actions AWS Deployment Setup

This guide will help you set up secure AWS deployments using GitHub Actions with OIDC (OpenID Connect).

## What Changed

✅ **Switched from access keys to OIDC** - More secure, no long-lived credentials
✅ **Added Terraform configuration for GitHub OIDC** - Automated IAM setup
✅ **Updated GitHub Actions workflow** - Uses temporary credentials

## Setup Steps

### Step 1: Initial Terraform Setup (One-time, Manual)

For the FIRST deployment, you'll need to use AWS credentials locally to set up the OIDC infrastructure:

```bash
# Configure AWS credentials locally (one-time setup)
aws configure

# Navigate to terraform directory
cd terraform

# Initialize Terraform
terraform init

# Deploy with dev environment
terraform plan -var-file="environments/dev.tfvars"
terraform apply -var-file="environments/dev.tfvars"

# Get the GitHub Actions Role ARN (you'll need this for Step 2)
terraform output github_actions_role_arn
```

### Step 2: Configure GitHub Secrets

Go to your GitHub repository settings:

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

1. **AWS_ROLE_ARN**
   - Value: The ARN from the `terraform output github_actions_role_arn` command
   - Example: `arn:aws:iam::123456789012:role/github-actions-deploy-role`

2. **JWT_SECRET_KEY_DEV**
   - Value: A random secret for JWT tokens in dev
   - Generate with: `openssl rand -base64 32`

3. **JWT_SECRET_KEY_PROD**
   - Value: A different random secret for JWT tokens in prod
   - Generate with: `openssl rand -base64 32`

### Step 3: Configure GitHub Environments (Optional but Recommended)

This adds approval requirements for production deployments:

1. Go to **Settings** → **Environments**
2. Create two environments:
   - **dev** (no protection rules)
   - **prod** (add required reviewers)

### Step 4: Test the Deployment

Now GitHub Actions should work:

```bash
# Commit and push your changes
git add .
git commit -m "Configure GitHub Actions with OIDC"
git push origin main
```

Or manually trigger via GitHub UI:
- Go to **Actions** tab
- Select "Deploy to AWS" workflow
- Click "Run workflow"
- Choose environment (dev/prod)

## How OIDC Works

1. GitHub Actions requests a token from GitHub's OIDC provider
2. GitHub Actions presents this token to AWS STS
3. AWS validates the token against the trust policy
4. AWS provides temporary credentials (valid for the session)
5. Terraform uses these temporary credentials to deploy

## Troubleshooting

### Error: "Credentials could not be loaded"

**Cause:** The `AWS_ROLE_ARN` secret is not set or incorrect.

**Fix:**
1. Run `terraform output github_actions_role_arn` to get the correct ARN
2. Verify the secret in GitHub Settings → Secrets and variables → Actions

### Error: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

**Cause:** The OIDC provider or role trust policy is not set up correctly.

**Fix:**
1. Verify the terraform was applied: `cd terraform && terraform apply -var-file="environments/dev.tfvars"`
2. Check the role exists: `aws iam get-role --role-name github-actions-deploy-role`

### Error: "No such file or directory" for build_lambda.sh

**Cause:** The build script is missing.

**Fix:**
Check if `scripts/build_lambda.sh` exists. If not, create it (see below).

## Alternative: Use Access Keys (Not Recommended)

If you can't use OIDC for some reason, you can revert to access keys:

1. Create an IAM user with appropriate permissions
2. Generate access keys for that user
3. Add secrets to GitHub:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
4. Revert the workflow changes in `.github/workflows/deploy.yml`

## Security Best Practices

✅ Use OIDC (current setup) instead of access keys
✅ Use GitHub Environments with required reviewers for prod
✅ Rotate JWT secrets periodically
✅ Review IAM permissions in `terraform/github_oidc.tf` (principle of least privilege)
✅ Never commit AWS credentials to git

## Next Steps

After deployment succeeds:
1. Test the API: `curl https://your-api-gateway-url/health`
2. Check CloudWatch logs for any issues
3. Set up monitoring and alerts

## Questions?

- Check GitHub Actions logs for detailed error messages
- Review Terraform state: `cd terraform && terraform show`
- Verify AWS resources in the AWS Console
