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

variable "postfix_host" {
  description = "Postfix server hostname"
  type        = string
  default     = "172.245.43.43"
}

variable "postfix_port" {
  description = "Postfix server port"
  type        = number
  default     = 25
}

variable "smtp_from_email" {
  description = "From email address for SMTP"
  type        = string
  default     = "noreply@mansaaurum.capital"
}

variable "smtp_to_email" {
  description = "To email address for receiving form submissions"
  type        = string
  default     = "contact@mansaaurum.capital"
}

variable "smtp_username" {
  description = "SMTP username for authentication"
  type        = string
  default     = ""
  sensitive   = true
}

variable "smtp_password" {
  description = "SMTP password for authentication"
  type        = string
  default     = ""
  sensitive   = true
}

variable "smtp_use_tls" {
  description = "Use TLS for SMTP connection"
  type        = bool
  default     = false
}
