# terraform/main.tf

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }

  # Backend configuration for state storage
  # Uncomment after creating S3 bucket for state
  # backend "s3" {
  #   bucket         = "localassist-terraform-state"
  #   key            = "api/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "localassist-terraform-locks"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = merge(
      {
        Project     = var.project_name
        Environment = var.environment
        ManagedBy   = "Terraform"
      },
      var.tags
    )
  }
}

# Local variables
locals {
  function_name = "${var.project_name}-api-${var.environment}"
  api_name      = "${var.project_name}-api-${var.environment}"
  
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}