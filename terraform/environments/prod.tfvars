# terraform/environments/prod.tfvars

environment  = "prod"
aws_region   = "us-east-1"
project_name = "localassist"

# Lambda Configuration
lambda_timeout = 30
lambda_memory  = 1024

# CORS - Restrict in production
cors_origins = "https://yourdomain.com,https://www.yourdomain.com"

# Logging
log_level = "INFO"

# Tags
tags = {
  Team        = "Production"
  CostCenter  = "Operations"
}

# JWT Secret (will be overridden by GitHub Secrets in CI/CD)
jwt_secret_key = "CHANGE_ME_IN_GITHUB_SECRETS"

# GitHub OIDC Configuration
github_repo = "BradenJT/localassist-api"