# terraform/outputs.tf

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "${aws_api_gateway_stage.api.invoke_url}/"
}

output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_api_gateway_rest_api.api.id
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.api.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.api.arn
}

output "dynamodb_leads_table" {
  description = "Name of the leads DynamoDB table"
  value       = aws_dynamodb_table.leads.name
}

output "dynamodb_users_table" {
  description = "Name of the users DynamoDB table"
  value       = aws_dynamodb_table.users.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "github_actions_role_arn" {
  description = "ARN of the IAM role for GitHub Actions OIDC"
  value       = try(aws_iam_role.github_actions.arn, "Not configured")
}