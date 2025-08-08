# Detailed Setup Guide

This guide will walk you through setting up the WhatsApp-Driven Google Drive Assistant step by step.

## Prerequisites

Before you begin, ensure you have the following:

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- A Twilio account with WhatsApp Sandbox access
- A Google Cloud Project with Drive API enabled
- An OpenAI API key

## Step 1: Twilio WhatsApp Sandbox Setup

### 1.1 Create Twilio Account

1. Go to [twilio.com](https://twilio.com) and create an account
2. Verify your email and phone number
3. Navigate to the Twilio Console

### 1.2 Set Up WhatsApp Sandbox

1. In the Twilio Console, go to **Messaging** > **Try it out** > **Send a WhatsApp message**
2. Follow the instructions to join your WhatsApp Sandbox:
   - Send the provided code to the WhatsApp number
   - You'll receive a confirmation message
3. Note your:
   - Account SID (found in the Console dashboard)
   - Auth Token (found in the Console dashboard)
   - WhatsApp number (format: `whatsapp:+14155238886`)

## Step 2: Google Drive API Setup

### 2.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing for the project

### 2.2 Enable Google Drive API

1. In the Google Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Google Drive API"
3. Click on it and press **Enable**

### 2.3 Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth 2.0 Client IDs**
3. Configure the OAuth consent screen:
   - User Type: External
   - App name: WhatsApp Drive Assistant
   - User support email: your email
   - Developer contact information: your email
4. Create OAuth 2.0 Client ID:
   - Application type: Web application
   - Name: WhatsApp Drive Assistant
   - Authorized redirect URIs: `http://localhost:5678/callback`
5. Download the JSON credentials file

### 2.4 Get Refresh Token

1. Install the Google OAuth 2.0 Playground:
   - Go to [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
   - Click the settings icon (⚙️) in the top right
   - Check "Use your own OAuth credentials"
   - Enter your OAuth 2.0 Client ID and Client Secret
2. In the playground:
   - Select "Drive API v3" from the left panel
   - Select the scopes you need (e.g., `https://www.googleapis.com/auth/drive`)
   - Click "Authorize APIs"
   - Sign in with your Google account
   - Click "Exchange authorization code for tokens"
   - Copy the Refresh Token

## Step 3: OpenAI API Setup

### 3.1 Create OpenAI Account

1. Go to [openai.com](https://openai.com) and create an account
2. Verify your email and phone number
3. Add payment method (required for API access)

### 3.2 Generate API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Give it a name (e.g., "WhatsApp Drive Assistant")
4. Copy the API key (you won't be able to see it again)

## Step 4: Environment Configuration

### 4.1 Copy Environment Template

```bash
cp .env-sample .env
```

### 4.2 Edit Environment Variables

Open the `.env` file and update the following variables:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_actual_account_sid
TWILIO_AUTH_TOKEN=your_actual_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Google Drive Configuration
GOOGLE_DRIVE_CLIENT_ID=your_actual_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_actual_client_secret
GOOGLE_DRIVE_REFRESH_TOKEN=your_actual_refresh_token
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id

# OpenAI Configuration
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4o

# Webhook Configuration
WEBHOOK_URL=https://your-n8n-instance.com/webhook/whatsapp-drive-assistant
```

### 4.3 Get Google Drive Folder ID

1. Open Google Drive in your browser
2. Navigate to the folder you want to use
3. The folder ID is in the URL: `https://drive.google.com/drive/folders/FOLDER_ID`
4. Copy the FOLDER_ID and add it to your `.env` file

## Step 5: Deploy with Docker

### 5.1 Run Setup Script

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 5.2 Start Services

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

Or manually:

```bash
docker-compose up -d
```

### 5.3 Verify Installation

1. Open your browser and go to `http://localhost:5678`
2. You should see the n8n interface
3. If prompted, create an admin account

## Step 6: Import and Configure Workflow

### 6.1 Import Workflow

1. In n8n, click **Import from file**
2. Select the `workflow.json` file from this project
3. Click **Import**

### 6.2 Configure Credentials

1. In the workflow, you'll need to configure these credentials:
   - **Google Drive OAuth2**: Use the credentials from Step 2
   - **Twilio API**: Use your Account SID and Auth Token
   - **OpenAI API**: Use your API key

### 6.3 Configure Webhook

1. In the workflow, find the **Webhook Trigger** node
2. Copy the webhook URL
3. In Twilio Console, go to **Messaging** > **Settings** > **WhatsApp Sandbox Settings**
4. Paste the webhook URL in the **When a message comes in** field
5. Set the HTTP method to **POST**
6. Save the configuration

## Step 7: Test the Workflow

### 7.1 Activate the Workflow

1. In n8n, click the **Activate** button on your workflow
2. The workflow should now be listening for webhook requests

### 7.2 Test Commands

Send these test messages to your WhatsApp Sandbox:

- `HELP` - Should return help information
- `LIST /` - Should list files in the root folder
- `SUMMARY /` - Should summarize documents (if any exist)

## Troubleshooting

### Common Issues

1. **Webhook not receiving messages**
   - Check if n8n is accessible from the internet
   - Verify the webhook URL in Twilio settings
   - Check n8n logs for errors

2. **Google Drive permission errors**
   - Ensure the folder is shared with your Google account
   - Check if the OAuth scopes are correct
   - Verify the refresh token is valid

3. **OpenAI API errors**
   - Check if the API key is correct
   - Verify your OpenAI account has credits
   - Check rate limiting

### Logs

View n8n logs:

```bash
docker-compose logs -f n8n
```

### Reset Everything

To start fresh:

```bash
docker-compose down -v
rm -rf data/
./scripts/setup.sh
./scripts/deploy.sh
```

## Security Considerations

1. **Environment Variables**: Never commit your `.env` file to version control
2. **API Keys**: Rotate your API keys regularly
3. **Webhook Security**: Consider adding webhook signature verification
4. **Access Control**: Limit who can access your n8n instance
5. **Audit Logging**: Monitor the audit logs for suspicious activity

## Next Steps

Once your setup is complete:

1. Test all commands thoroughly
2. Set up monitoring and alerting
3. Configure backup strategies
4. Document your specific use cases
5. Train your team on the system

For additional support, check the main README.md file or open an issue on GitHub.
