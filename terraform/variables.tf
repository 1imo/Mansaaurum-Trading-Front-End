variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "api_gateway_name" {
  description = "Name of the API Gateway"
  type        = string
  default     = "mansaaurum-contact-api"
}

variable "rate_limit" {
  description = "Rate limit (requests per second)"
  type        = number
  default     = 10
}

variable "burst_limit" {
  description = "Burst limit (maximum requests)"
  type        = number
  default     = 20
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "mansaaurum-contact-handler"
}

variable "webhook_url" {
  description = "Webhook URL to send form data to"
  type        = string
  sensitive   = true
}

variable "allowed_origin_domain" {
  description = "Allowed origin domain for CORS (e.g., mansaaurumcapital.com)"
  type        = string
  default     = "mansaaurumcapital.com"
}
