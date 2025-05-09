resource "aws_lambda_function" "update_account" {
  filename         = "update_account.zip"
  function_name    = "dindin-update-account"
  role            = aws_iam_role.lambda_role.arn
  handler         = "update_account.handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 128

  environment {
    variables = {
      ACCOUNTS_BUCKET = "dindin-ofx-files"
    }
  }
}

resource "aws_lambda_permission" "update_account" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_account.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${data.aws_apigatewayv2_api.existing_api.execution_arn}/*/*"
} 