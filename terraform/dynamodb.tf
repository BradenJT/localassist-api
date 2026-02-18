# terraform/dynamodb.tf

# Leads Table
resource "aws_dynamodb_table" "leads" {
  name           = "${var.project_name}-leads-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"  # On-demand pricing
  hash_key       = "id"
  range_key      = "business_id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "business_id"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }

  # Global Secondary Index for querying by business_id
  global_secondary_index {
    name            = "business_id-created_at-index"
    hash_key        = "business_id"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  # Enable point-in-time recovery for production
  point_in_time_recovery {
    enabled = var.environment == "prod" ? true : false
  }

  # Server-side encryption
  server_side_encryption {
    enabled = true
  }

  tags = {
    Name = "${var.project_name}-leads-${var.environment}"
  }
}

# Users Table
resource "aws_dynamodb_table" "users" {
  name           = "${var.project_name}-users-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  # Global Secondary Index for email lookup
  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod" ? true : false
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Name = "${var.project_name}-users-${var.environment}"
  }
}