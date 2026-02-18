# Quick Start - Fix GitHub Actions

## What I Fixed

✅ Converted your GitHub Actions workflow to use **OIDC** (OpenID Connect) instead of long-lived access keys
✅ Added Terraform configuration to create the necessary AWS IAM roles and OIDC provider
✅ Updated environment configurations with your GitHub repo information

## Files Changed

- `.github/workflows/deploy.yml` - Updated to use OIDC authentication
- `terraform/github_oidc.tf` - **NEW** - Creates AWS OIDC provider and IAM role
- `terraform/variables.tf` - Added `github_repo` variable
- `terraform/output.tf` - Added output for GitHub Actions role ARN
- `terraform/environments/dev.tfvars` - Added GitHub repo config
- `terraform/environments/prod.tfvars` - Added GitHub repo config

## Next Steps (Do This Now!)

### 1. Deploy the OIDC Infrastructure

```bash
# Make sure you have AWS credentials configured locally
aws configure

# Navigate to terraform
cd terraform

# Initialize and apply
terraform init
terraform apply -var-file="environments/dev.tfvars"

# Copy this ARN - you'll need it!
terraform output github_actions_role_arn
```

### 2. Add GitHub Secret

1. Go to: https://github.com/bradenjt/localassist-api/settings/secrets/actions
2. Click "New repository secret"
3. Name: `AWS_ROLE_ARN`
4. Value: Paste the ARN from step 1
5. Click "Add secret"

### 3. Add JWT Secrets

```bash
# Generate secrets
echo "Dev JWT Secret: $(openssl rand -base64 32)"
echo "Prod JWT Secret: $(openssl rand -base64 32)"
```

Add these as GitHub secrets:
- `JWT_SECRET_KEY_DEV` - First secret
- `JWT_SECRET_KEY_PROD` - Second secret

### 4. Test It

```bash
# Commit these changes
git add .
git commit -m "Setup GitHub Actions with OIDC authentication"
git push origin main
```

Watch the deployment run at:
https://github.com/bradenjt/localassist-api/actions

## If You Get Stuck

See `SETUP_GITHUB_ACTIONS.md` for detailed troubleshooting.

## Why OIDC?

- ✅ No long-lived credentials stored in GitHub
- ✅ Temporary credentials that expire after each run
- ✅ More secure and AWS recommended approach
- ✅ No credential rotation needed
