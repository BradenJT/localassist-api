# terraform/lambda.tf

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = var.environment == "prod" ? 30 : 7

  tags = {
    Name = "${local.function_name}-logs"
  }
}

# Lambda Layer for Dependencies
resource "aws_lambda_layer_version" "dependencies" {
  filename            = "${path.module}/../lambda_layer.zip"
  layer_name          = "${local.function_name}-dependencies"
  compatible_runtimes = ["python3.11"]
  source_code_hash    = filebase64sha256("${path.module}/../lambda_layer.zip")

  description = "Python dependencies for ${local.function_name}"
}

# Lambda Function
resource "aws_lambda_function" "api" {
  filename         = "${path.module}/../lambda_function.zip"
  function_name    = local.function_name
  role            = aws_iam_role.lambda_role.arn
  handler         = "app.main.handler"
  source_code_hash = filebase64sha256("${path.module}/../lambda_function.zip")
  runtime         = "python3.11"
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory

  layers = [aws_lambda_layer_version.dependencies.arn]

  environment {
    variables = {
      ENVIRONMENT        = var.environment
      DEBUG              = var.environment == "dev" ? "true" : "false"
      JWT_SECRET_KEY     = var.jwt_secret_key
      LEADS_TABLE_NAME   = aws_dynamodb_table.leads.name
      USERS_TABLE_NAME   = aws_dynamodb_table.users.name
      AWS_REGION         = var.aws_region
      CORS_ORIGINS       = var.cors_origins
      LOG_LEVEL          = var.log_level
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_logs,
    aws_iam_role_policy.lambda_logs,
    aws_iam_role_policy.lambda_dynamodb
  ]

  tags = {
    Name = local.function_name
  }
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}