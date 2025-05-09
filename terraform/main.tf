provider "aws" {
  region = "sa-east-1"
}

# API Gateway - Usando o gateway HTTP existente
data "aws_apigatewayv2_api" "existing_api" {
  api_id = "50917j6yoa"
}

# IAM Role para as Lambdas
resource "aws_iam_role" "lambda_role" {
  name = "dindin_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Política para acesso ao S3
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "dindin_lambda_s3_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect = "Allow"
        Resource = [
          "arn:aws:s3:::dindin-ofx-files",
          "arn:aws:s3:::dindin-ofx-files/*"
        ]
      }
    ]
  })
}

# Política para logs do CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Integrações Lambda necessárias para as novas rotas
resource "aws_apigatewayv2_integration" "update_account" {
  api_id                 = data.aws_apigatewayv2_api.existing_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.update_account.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "delete_account" {
  api_id                 = data.aws_apigatewayv2_api.existing_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.delete_account.invoke_arn
  payload_format_version = "2.0"
}

# Rotas para as novas integrações
resource "aws_apigatewayv2_route" "put_account" {
  api_id    = data.aws_apigatewayv2_api.existing_api.id
  route_key = "PUT /accounts/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.update_account.id}"
}

resource "aws_apigatewayv2_route" "delete_account" {
  api_id    = data.aws_apigatewayv2_api.existing_api.id
  route_key = "DELETE /accounts/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.delete_account.id}"
} 