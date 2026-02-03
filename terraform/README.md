# Terraform Infrastructure for Mansaaurum Contact Form

This Terraform configuration sets up:
- API Gateway with rate limiting (10 requests/second, burst of 20)
- Lambda function to process form submissions
- Integration between API Gateway and Lambda
- IAM roles and permissions

## Prerequisites

### 1. Install Terraform

**On macOS:**
```bash
brew install terraform
```

**On Linux:**
```bash
# Download from https://www.terraform.io/downloads
# Or use package manager:
sudo apt-get update && sudo apt-get install terraform  # Ubuntu/Debian
sudo yum install terraform  # CentOS/RHEL
```

**On Windows:**
- Download from: https://www.terraform.io/downloads
- Extract and add to your PATH

**Verify installation:**
```bash
terraform version
```

### 2. Install AWS CLI

**On macOS:**
```bash
brew install awscli
```

**On Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**On Windows:**
- Download from: https://aws.amazon.com/cli/
- Run the installer

**Verify installation:**
```bash
aws --version
```

### 3. Configure AWS Credentials

You need an AWS account and credentials to deploy infrastructure.

#### Option A: AWS Access Keys (Recommended for beginners)

1. **Log in to AWS Console:**
   - Go to https://console.aws.amazon.com/
   - Sign in with your AWS account

2. **Create an IAM User:**
   - Go to IAM (Identity and Access Management) in AWS Console
   - Click "Users" → "Create user"
   - Enter a username (e.g., "terraform-user")
   - Click "Next"

3. **Set Permissions:**
   - Select "Attach policies directly"
   - Search for and select:
     - `AmazonAPIGatewayAdministrator`
     - `AWSLambda_FullAccess`
     - `IAMFullAccess` (or create a more restricted policy)
   - Click "Next" → "Create user"

4. **Get Access Keys:**
   - Click on the user you just created
   - Go to "Security credentials" tab
   - Click "Create access key"
   - Select "Command Line Interface (CLI)"
   - Click "Next" → "Create access key"
   - **IMPORTANT:** Copy both the Access Key ID and Secret Access Key (you won't see the secret again!)

5. **Configure AWS CLI:**
   ```bash
   aws configure
   ```
   
   You'll be prompted for:
   - **AWS Access Key ID:** Paste your Access Key ID
   - **AWS Secret Access Key:** Paste your Secret Access Key
   - **Default region name:** `eu-west-2` (London)
   - **Default output format:** `json` (just press Enter)

   This creates credentials in `~/.aws/credentials` and `~/.aws/config`

#### Option B: Environment Variables

```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="eu-west-2"
```

#### Option C: AWS SSO (Advanced)

If your organization uses AWS SSO, configure it separately.

**Verify AWS connection:**
```bash
aws sts get-caller-identity
```

This should return your AWS account ID and user ARN.

## Configuration

### Set SMTP Credentials

Create a file called `terraform.tfvars` in the `terraform` directory:

```hcl
smtp_username = "your-smtp-username"
smtp_password = "your-smtp-password"
```

**Important:** The `terraform.tfvars` file is in `.gitignore` to keep your credentials safe. Never commit this file!

You can also override other variables here:
```hcl
region = "eu-west-2"
postfix_host = "172.245.43.43"
postfix_port = 25
smtp_use_tls = true
smtp_from_email = "noreply@mansaaurum.capital"
smtp_to_email = "contact@mansaaurum.capital"
```

## Deployment

### Step 1: Navigate to Terraform Directory

```bash
cd terraform
```

### Step 2: Initialize Terraform

This downloads the AWS provider and sets up Terraform:

```bash
terraform init
```

You should see:
```
Initializing the backend...
Initializing provider plugins...
Terraform has been successfully initialized!
```

### Step 3: Review What Will Be Created

This shows you what Terraform will create without actually creating it:

```bash
terraform plan
```

Review the output carefully. It will show:
- Resources that will be created
- Any variables that need values
- Estimated costs (if applicable)

### Step 4: Apply the Configuration

This actually creates the AWS resources:

```bash
terraform apply
```

Terraform will:
1. Show you the plan again
2. Ask for confirmation: `Do you want to perform these actions?`
3. Type `yes` and press Enter

**This will take a few minutes** as it creates:
- API Gateway
- Lambda function
- IAM roles
- All integrations

### Step 5: Get Your API Gateway URL

After deployment completes, get the API Gateway URL:

```bash
terraform output api_gateway_url
```

This will output something like:
```
api_gateway_url = "https://abc123xyz.execute-api.eu-west-2.amazonaws.com/prod/contact"
```

### Step 6: Update Your Frontend

1. Copy the API Gateway URL from step 5
2. Open `scripts.js` in the root directory
3. Replace `YOUR_API_GATEWAY_URL_HERE` with the actual URL:

```javascript
const API_GATEWAY_URL = 'https://abc123xyz.execute-api.eu-west-2.amazonaws.com/prod/contact';
```

## Testing

Test your form submission:
1. Open `index.html` in a browser
2. Fill out the contact form
3. Submit it
4. Check CloudWatch Logs for the Lambda function to see if it worked

**View Lambda logs:**
```bash
aws logs tail /aws/lambda/mansaaurum-contact-handler --follow
```

## Updating Infrastructure

If you make changes to the Terraform files:

```bash
terraform plan    # Review changes
terraform apply   # Apply changes
```

## Destroying Infrastructure

To remove all AWS resources (this will delete everything!):

```bash
terraform destroy
```

Type `yes` when prompted. This is useful for:
- Cleaning up test environments
- Removing resources you no longer need
- Starting fresh

## Troubleshooting

### "Error: No valid credential sources found"
- Make sure you've run `aws configure` or set environment variables
- Verify with: `aws sts get-caller-identity`

### "Error: Access Denied"
- Your IAM user needs the permissions listed above
- Check IAM policies in AWS Console

### "Error: Region not available"
- Make sure you're using `eu-west-2` (London)
- Verify region in `variables.tf` or `terraform.tfvars`

### Lambda function fails
- Check CloudWatch Logs: AWS Console → Lambda → Your function → Monitor → View logs
- Verify SMTP credentials are correct
- Check Postfix server is accessible from AWS

### API Gateway returns 500
- Check Lambda function logs
- Verify Lambda has correct permissions
- Check API Gateway → Your API → Stages → prod → Logs

## Cost Estimation

This setup uses AWS Free Tier eligible services:
- **API Gateway:** First 1 million requests/month free
- **Lambda:** 1 million free requests/month, 400,000 GB-seconds free
- **CloudWatch Logs:** 5 GB free ingestion/month

For typical usage, this should be **free or very low cost** (< $1/month).

## Rate Limiting

The API Gateway is configured with:
- Rate limit: 10 requests per second
- Burst limit: 20 requests

Adjust in `variables.tf` if needed.

## Postfix Configuration

The Lambda expects a Postfix server accessible at:
- Host: `172.245.43.43` (configured in variables)
- Port: `25` (default)
- TLS: Enabled by default
- Authentication: Uses `smtp_username` and `smtp_password` from `terraform.tfvars`

Make sure your Postfix server:
- Is accessible from AWS Lambda (may need VPC configuration)
- Has the correct port open
- Accepts SMTP authentication with the provided credentials

## Next Steps

1. ✅ Deploy infrastructure
2. ✅ Get API Gateway URL
3. ✅ Update `scripts.js` with the URL
4. ✅ Test form submission
5. ✅ Monitor CloudWatch Logs
6. ✅ Set up custom domain (optional)
7. ✅ Add API key authentication (optional)

## Resources

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS API Gateway Docs](https://docs.aws.amazon.com/apigateway/)
- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)
- [Terraform Learn](https://learn.hashicorp.com/terraform)
