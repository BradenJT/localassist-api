# terraform/variables.tf

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "localassist"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "jwt_secret_key" {
  description = "Secret key for JWT token generation"
  type        = string
  sensitive   = true
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30
}

variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

variable "cors_origins" {
  description = "Allowed CORS origins"
  type        = string
  default     = "*"
}

variable "log_level" {
  description = "Application log level"
  type        = string
  default     = "INFO"
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}