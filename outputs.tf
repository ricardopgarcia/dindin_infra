output "api_endpoint" {
  description = "URL do endpoint da API"
  value       = "${aws_apigatewayv2_api.dindin_api.api_endpoint}/${var.api_stage}"
}

output "function_name" {
  description = "Nome da função Lambda"
  value       = aws_lambda_function.dindin_api.function_name
}

output "api_stage" {
  description = "Nome do estágio da API"
  value       = var.api_stage
} 