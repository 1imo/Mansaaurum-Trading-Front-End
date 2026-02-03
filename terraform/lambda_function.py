import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def lambda_handler(event, context):
    """
    Lambda function to handle contact form submissions and send to Postfix server
    """
    try:
        # Parse the request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Extract form fields
        first_name = body.get('firstName', '')
        last_name = body.get('lastName', '')
        email = body.get('email', '')
        country_code = body.get('countryCode', '')
        phone_number = body.get('phoneNumber', '')
        message = body.get('message', '')
        
        # Get environment variables
        postfix_host = os.environ.get('POSTFIX_HOST', 'localhost')
        postfix_port = int(os.environ.get('POSTFIX_PORT', '25'))
        smtp_from_email = os.environ.get('SMTP_FROM_EMAIL', 'noreply@mansaaurum.capital')
        smtp_to_email = os.environ.get('SMTP_TO_EMAIL', 'contact@mansaaurum.capital')
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        smtp_use_tls = os.environ.get('SMTP_USE_TLS', 'true').lower() == 'true'
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = smtp_from_email
        msg['To'] = smtp_to_email
        msg['Subject'] = f'New Contact Form Submission from {first_name} {last_name}'
        
        # Create email body
        email_body = f"""
New contact form submission received:

Name: {first_name} {last_name}
Email: {email}
Phone: {country_code} {phone_number}
Message:
{message}
"""
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Send email via Postfix server
        try:
            if smtp_use_tls:
                # Use SMTP with TLS
                with smtplib.SMTP(postfix_host, postfix_port) as server:
                    server.starttls()
                    if smtp_username and smtp_password:
                        server.login(smtp_username, smtp_password)
                    server.send_message(msg)
            else:
                # Use plain SMTP (no TLS)
                with smtplib.SMTP(postfix_host, postfix_port) as server:
                    if smtp_username and smtp_password:
                        server.login(smtp_username, smtp_password)
                    server.send_message(msg)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': True,
                    'message': 'Form submitted successfully'
                })
            }
        except Exception as smtp_error:
            print(f"SMTP Error: {str(smtp_error)}")
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'message': 'Failed to send email'
                })
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': 'Internal server error'
            })
        }
