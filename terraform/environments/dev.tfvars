# terraform/environments/dev.tfvars

environment  = "dev"
aws_region   = "us-east-1"
project_name = "localassist"

# Lambda Configuration
lambda_timeout = 30
lambda_memory  = 512

# CORS - Allow all for development
cors_origins = "*"

# Logging
log_level = "DEBUG"

# Tags
tags = {
  Team        = "Development"
  CostCenter  = "Engineering"
}

# JWT Secret (will be overridden by GitHub Secrets in CI/CD)
jwt_secret_key = "dev-secret-key-change-me"

# GitHub OIDC Configuration
github_repo = "bradenjt/localassist-api"