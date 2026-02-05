import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    """
    Lambda function to handle contact form submissions and send to webhook
    """
    try:
        # Parse the request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Extract form fields
        form_data = {
            'firstName': body.get('firstName', ''),
            'lastName': body.get('lastName', ''),
            'email': body.get('email', ''),
            'countryCode': body.get('countryCode', ''),
            'phoneNumber': body.get('phoneNumber', ''),
            'message': body.get('message', '')
        }
        
        # Get environment variables
        webhook_url = os.environ.get('WEBHOOK_URL', '')
        allowed_origin = os.environ.get('ALLOWED_ORIGIN', '*')
        
        # Get Origin header from request to validate
        request_origin = event.get('headers', {}).get('Origin') or event.get('headers', {}).get('origin', '')
        
        # Validate origin (optional additional check)
        cors_origin = allowed_origin
        if request_origin and allowed_origin != '*':
            # Check if request origin matches allowed origin
            if request_origin.startswith('https://') and request_origin.replace('https://', '').replace('www.', '') == allowed_origin.replace('https://', '').replace('www.', ''):
                cors_origin = request_origin
            elif request_origin.startswith('http://') and request_origin.replace('http://', '').replace('www.', '') == allowed_origin.replace('https://', '').replace('www.', ''):
                cors_origin = request_origin
        
        if not webhook_url:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': cors_origin,
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'message': 'Webhook URL not configured'
                })
            }
        
        # Validate webhook URL format (basic check)
        if not webhook_url.startswith('https://'):
            print(f"Warning: Webhook URL doesn't start with https://")
        
        # Log webhook URL (masked for security)
        webhook_domain = webhook_url.split('/')[2] if '/' in webhook_url else 'unknown'
        print(f"Calling webhook at domain: {webhook_domain}")
        
        # Prepare webhook request - format for Discord webhook
        # Discord webhooks expect a specific format with content or embeds
        # Don't include None values - Discord rejects them
        discord_payload = {
            'embeds': [{
                'title': 'New Contact Form Submission',
                'color': 0x00ff00,  # Green color
                'fields': [
                    {
                        'name': 'First Name',
                        'value': form_data.get('firstName', 'N/A') or 'N/A',
                        'inline': True
                    },
                    {
                        'name': 'Last Name',
                        'value': form_data.get('lastName', 'N/A') or 'N/A',
                        'inline': True
                    },
                    {
                        'name': 'Email',
                        'value': form_data.get('email', 'N/A') or 'N/A',
                        'inline': False
                    },
                    {
                        'name': 'Phone',
                        'value': f"{form_data.get('countryCode', '')} {form_data.get('phoneNumber', '')}".strip() or 'N/A',
                        'inline': False
                    },
                    {
                        'name': 'Message',
                        'value': (form_data.get('message', 'N/A') or 'N/A')[:1024],  # Discord limit
                        'inline': False
                    }
                ]
            }]
        }
        
        webhook_data = json.dumps(discord_payload).encode('utf-8')
        print(f"Payload size: {len(webhook_data)} bytes")
        print(f"Payload preview: {json.dumps(discord_payload)[:200]}...")
        
        request = urllib.request.Request(
            webhook_url,
            data=webhook_data,
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mansaaurum-Contact-Form/1.0'}
        )
        
        # Call webhook
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                response_code = response.getcode()
                response_body = response.read().decode('utf-8')
                
                if response_code >= 200 and response_code < 300:
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Origin': cors_origin,
                            'Content-Type': 'application/json'
                        },
                        'body': json.dumps({
                            'success': True,
                            'message': 'Form submitted successfully'
                        })
                    }
                else:
                    print(f"Webhook returned status {response_code}: {response_body}")
                    return {
                        'statusCode': 500,
                        'headers': {
                            'Access-Control-Allow-Origin': cors_origin,
                            'Content-Type': 'application/json'
                        },
                        'body': json.dumps({
                            'success': False,
                            'message': 'Webhook request failed'
                        })
                    }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e.reason)
            print(f"HTTP Error: {e.code} - {e.reason}")
            print(f"Error response body: {error_body}")
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': cors_origin,
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'message': f'Webhook returned error {e.code}: {e.reason}'
                })
            }
        except urllib.error.URLError as e:
            print(f"URL Error: {str(e)}")
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': cors_origin,
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'message': 'Failed to connect to webhook'
                })
            }
        except Exception as webhook_error:
            print(f"Webhook Error: {str(webhook_error)}")
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': cors_origin,
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'message': 'Failed to send form data to webhook'
                })
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # Get allowed origin for error response
        allowed_origin = os.environ.get('ALLOWED_ORIGIN', '*')
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': allowed_origin,
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': 'Internal server error'
            })
        }
