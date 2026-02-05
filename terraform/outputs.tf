output "api_gateway_url" {
  description = "API Gateway endpoint URL"
  value       = "${aws_api_gateway_stage.contact_api_stage.invoke_url}/contact"
}

output "api_gateway_id" {
  description = "API Gateway ID"
  value       = aws_api_gateway_rest_api.contact_api.id
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.contact_handler.function_name
}

output "api_key" {
  description = "API Gateway API Key (for rate limiting)"
  value       = aws_api_gateway_api_key.contact_api_key.value
  sensitive   = true
}
