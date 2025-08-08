# WhatsApp-Driven Google Drive Assistant

A n8n workflow that listens to WhatsApp messages and performs Google Drive actions such as listing files, deleting, moving, and summarizing documents in a folder.

## Features

- **WhatsApp Integration**: Uses Twilio Sandbox for WhatsApp as the entry point
- **Google Drive Operations**: List, delete, move files and folders
- **AI Summarization**: Automatic document summarization using OpenAI GPT-4
- **Audit Logging**: Maintains an audit spreadsheet for all operations
- **Safety Features**: Guards against accidental mass deletion

## Command Syntax

The assistant accepts the following commands via WhatsApp:

- `LIST /ProjectX` - List all files in /ProjectX folder
- `DELETE /ProjectX/report.pdf` - Delete a specific file
- `MOVE /ProjectX/report.pdf /Archive` - Move a file to another folder
- `SUMMARY /ProjectX` - Generate summaries of all documents in the folder
- `HELP` - Show available commands

## Prerequisites

- n8n instance (can be run via Docker)
- Twilio account with WhatsApp Sandbox
- Google Cloud Project with Drive API enabled
- OpenAI API key
- Google Service Account credentials

## Quick Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/WhatsApp-Driven-Google-Drive-Assistant.git
   cd WhatsApp-Driven-Google-Drive-Assistant
   ```

2. **Set up environment variables**
   ```bash
   cp .env-sample .env
   # Edit .env with your credentials
   ```

3. **Run n8n with Docker**
   ```bash
   docker-compose up -d
   ```

4. **Import the workflow**
   - Open n8n at `http://localhost:5678`
   - Import `workflow.json`
   - Configure the webhook URL and credentials

## Detailed Setup Instructions

### 1. Twilio WhatsApp Sandbox Setup

1. Create a Twilio account at [twilio.com](https://twilio.com)
2. Navigate to WhatsApp Sandbox in the Twilio Console
3. Follow the instructions to join your sandbox
4. Note your Account SID, Auth Token, and WhatsApp number

### 2. Google Drive API Setup

1. Create a Google Cloud Project
2. Enable the Google Drive API
3. Create a Service Account
4. Download the JSON credentials file
5. Share your Google Drive folder with the service account email

### 3. OpenAI API Setup

1. Create an OpenAI account at [openai.com](https://openai.com)
2. Generate an API key
3. Add the key to your environment variables

### 4. n8n Configuration

1. Install n8n via Docker:
   ```bash
   docker run -it --rm \
     --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     n8nio/n8n
   ```

2. Import the workflow from `workflow.json`
3. Configure the webhook URL for Twilio
4. Set up the Google Drive and OpenAI credentials

## Project Structure

```
WhatsApp-Driven-Google-Drive-Assistant/
├── README.md                 # This file
├── workflow.json            # n8n workflow definition
├── .env-sample              # Environment variables template
├── docker-compose.yml       # Docker setup for n8n
├── scripts/
│   ├── setup.sh            # Setup script
│   └── deploy.sh           # Deployment script
└── docs/
    ├── setup-guide.md      # Detailed setup instructions
    └── api-reference.md    # API documentation
```

## Security Considerations

- All API keys are stored as environment variables
- Google Drive operations are scoped to specific folders
- Audit logging tracks all operations
- Confirmation required for deletion operations
- Webhook signature verification for Twilio

## Troubleshooting

### Common Issues

1. **Webhook not receiving messages**
   - Check if n8n is accessible from the internet
   - Verify Twilio webhook URL configuration
   - Check n8n logs for errors

2. **Google Drive permission errors**
   - Ensure service account has access to the folder
   - Check if the folder is shared with the service account email
   - Verify Google Drive API is enabled

3. **OpenAI API errors**
   - Check if API key is correct
   - Verify OpenAI account has credits
   - Check rate limiting

### Logs

Check n8n logs for detailed error information:
```bash
docker logs n8n
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the documentation in `/docs`
3. Open an issue on GitHub
