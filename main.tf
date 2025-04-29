provider "aws" {
  region = var.aws_region
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::dindin-ofx-files",
          "arn:aws:s3:::dindin-ofx-files/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "dindin_api" {
  function_name = "dindin_api"
  handler       = "hello_world.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/lambda/hello_world.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/hello_world.zip")
}

resource "aws_lambda_function" "accounts_api" {
  function_name = "accounts_api"
  handler       = "accounts.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/lambda/accounts.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/accounts.zip")
}

resource "aws_lambda_function" "transactions_api" {
  function_name = "transactions_api"
  handler       = "transactions.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/lambda/transactions.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/transactions.zip")
  timeout       = 30
  memory_size   = 256
}

resource "aws_lambda_function" "ofx_parser_api" {
  function_name = "ofx_parser_api"
  handler       = "ofx_parser.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/lambda/ofx_parser.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/ofx_parser.zip")
}

resource "aws_lambda_function" "investment_detail_api" {
  function_name = "investment_detail_api"
  handler       = "investment_detail.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/lambda/investment_detail.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/investment_detail.zip")
  timeout       = 10
  memory_size   = 128
  environment {
    variables = {
      INVESTMENTS_BUCKET = "dindin-ofx-files"
    }
  }
}

resource "aws_lambda_function" "create_account_api" {
  function_name = "create_account_api"
  handler       = "create_account.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/lambda/create_account.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/create_account.zip")
  timeout       = 10
  memory_size   = 128
  environment {
    variables = {
      ACCOUNTS_BUCKET = "dindin-ofx-files"
    }
  }
}

resource "aws_apigatewayv2_api" "dindin_api" {
  name          = "DindinAPI"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.dindin_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.dindin_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "accounts_integration" {
  api_id           = aws_apigatewayv2_api.dindin_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.accounts_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "transactions_integration" {
  api_id           = aws_apigatewayv2_api.dindin_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.transactions_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "ofx_parser_integration" {
  api_id           = aws_apigatewayv2_api.dindin_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.ofx_parser_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "investment_detail_integration" {
  api_id           = aws_apigatewayv2_api.dindin_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.investment_detail_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "create_account_integration" {
  api_id           = aws_apigatewayv2_api.dindin_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.create_account_api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.dindin_api.id
  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "accounts_route" {
  api_id    = aws_apigatewayv2_api.dindin_api.id
  route_key = "GET /accounts"
  target    = "integrations/${aws_apigatewayv2_integration.accounts_integration.id}"
}

resource "aws_apigatewayv2_route" "transactions_route" {
  api_id    = aws_apigatewayv2_api.dindin_api.id
  route_key = "GET /transactions"
  target    = "integrations/${aws_apigatewayv2_integration.transactions_integration.id}"
}

resource "aws_apigatewayv2_route" "ofx_parser_route" {
  api_id    = aws_apigatewayv2_api.dindin_api.id
  route_key = "POST /ofx-parser"
  target    = "integrations/${aws_apigatewayv2_integration.ofx_parser_integration.id}"
}

resource "aws_apigatewayv2_route" "investment_detail_route" {
  api_id    = aws_apigatewayv2_api.dindin_api.id
  route_key = "GET /investments/{investmentId}"
  target    = "integrations/${aws_apigatewayv2_integration.investment_detail_integration.id}"
}

resource "aws_apigatewayv2_route" "create_account_route" {
  api_id    = aws_apigatewayv2_api.dindin_api.id
  route_key = "POST /accounts"
  target    = "integrations/${aws_apigatewayv2_integration.create_account_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.dindin_api.id
  name        = var.api_stage
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dindin_api.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.dindin_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_accounts_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.accounts_api.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.dindin_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_transactions_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transactions_api.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.dindin_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_ofx_parser_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ofx_parser_api.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.dindin_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_investment_detail_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.investment_detail_api.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.dindin_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "allow_create_account_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_account_api.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.dindin_api.execution_arn}/*/*"
}

data "aws_s3_bucket" "ofx_files" {
  bucket = "dindin-ofx-files"
}

resource "aws_s3_bucket_public_access_block" "ofx_files" {
  bucket = data.aws_s3_bucket.ofx_files.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}