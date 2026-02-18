# terraform/backend.tf
# Remote state backend configuration

terraform {
  backend "s3" {
    bucket         = "localassist-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "localassist-terraform-locks"
  }
}
