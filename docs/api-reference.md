# API Reference

This document provides detailed information about the WhatsApp-Driven Google Drive Assistant API and workflow structure.

## Workflow Overview

The WhatsApp-Driven Google Drive Assistant is built using n8n and consists of the following main components:

1. **Webhook Trigger** - Receives WhatsApp messages from Twilio
2. **Command Parser** - Parses and validates incoming commands
3. **Command Router** - Routes commands to appropriate handlers
4. **Action Handlers** - Execute specific Google Drive operations
5. **Response Formatter** - Formats responses for WhatsApp
6. **Audit Logger** - Logs all operations for audit purposes

## Command Syntax

### General Format

All commands follow this general format:
```
COMMAND [path] [additional_parameters]
```

### Available Commands

#### 1. LIST Command

**Purpose**: List files and folders in a specified directory

**Syntax**:
```
LIST [path]
```

**Examples**:
- `LIST /` - List files in root directory
- `LIST /ProjectX` - List files in ProjectX folder
- `LIST` - List files in default folder

**Response Format**:
```
📁 Files in /ProjectX:

1. 📁 Documents
   Modified: 2024-01-15

2. 📄 report.pdf (245.3KB)
   Modified: 2024-01-14

3. 📄 presentation.pptx (1.2MB)
   Modified: 2024-01-13

Total: 3 items
```

#### 2. DELETE Command

**Purpose**: Delete a specific file or folder

**Syntax**:
```
DELETE [path]
```

**Examples**:
- `DELETE /ProjectX/report.pdf` - Delete report.pdf
- `DELETE /ProjectX/old-folder` - Delete old-folder

**Safety Features**:
- Requires confirmation keyword (default: `CONFIRM`)
- Confirmation format: `DELETE [path] CONFIRM`

**Response Format**:
```
⚠️ Delete Confirmation Required

You are about to delete:
/ProjectX/report.pdf

To confirm deletion, reply with:
DELETE /ProjectX/report.pdf CONFIRM
```

#### 3. MOVE Command

**Purpose**: Move a file or folder to a different location

**Syntax**:
```
MOVE [source_path] [destination_path]
```

**Examples**:
- `MOVE /ProjectX/report.pdf /Archive` - Move report.pdf to Archive folder
- `MOVE /ProjectX/old-docs /Archive/2023` - Move old-docs to Archive/2023

**Response Format**:
```
✅ File moved successfully

/ProjectX/report.pdf has been moved to /Archive.
```

#### 4. SUMMARY Command

**Purpose**: Generate AI-powered summaries of documents in a folder

**Syntax**:
```
SUMMARY [path]
```

**Examples**:
- `SUMMARY /ProjectX` - Summarize all documents in ProjectX
- `SUMMARY /` - Summarize documents in root folder

**Supported File Types**:
- PDF files (`application/pdf`)
- Word documents (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`)
- Text files (`text/plain`)
- Markdown files (`text/markdown`)

**Response Format**:
```
📄 Document Summaries

1. report.pdf
   This document provides a comprehensive analysis of Q4 2023 performance metrics. Key findings include a 15% increase in revenue, improved customer satisfaction scores, and successful implementation of new features.

2. presentation.pptx
   The presentation covers the annual strategy review, highlighting three main initiatives: market expansion, product innovation, and operational efficiency improvements.

Total: 2 documents summarized
```

#### 5. HELP Command

**Purpose**: Display help information and available commands

**Syntax**:
```
HELP
```

**Response Format**:
```
🤖 WhatsApp Drive Assistant Help

Available Commands:

📁 LIST /folder - List files in a folder
   Example: LIST /ProjectX

🗑️ DELETE /path/file - Delete a file
   Example: DELETE /ProjectX/report.pdf

📂 MOVE /source /destination - Move a file
   Example: MOVE /ProjectX/report.pdf /Archive

📄 SUMMARY /folder - Summarize documents in a folder
   Example: SUMMARY /ProjectX

❓ HELP - Show this help message

Safety Features:
• Confirmation required for deletions
• Audit logging of all operations
• File count limits for safety
```

## Webhook API

### Endpoint

```
POST /webhook/whatsapp-drive-assistant
```

### Request Format

The webhook expects requests from Twilio in the following format:

```json
{
  "Body": "LIST /ProjectX",
  "From": "whatsapp:+1234567890",
  "To": "whatsapp:+14155238886",
  "MessageSid": "SM1234567890abcdef",
  "AccountSid": "AC1234567890abcdef",
  "NumMedia": "0"
}
```

### Response Format

The webhook responds with a TwiML response:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>📁 Files in /ProjectX:

1. 📄 report.pdf (245.3KB)
   Modified: 2024-01-14

Total: 1 items</Message>
</Response>
```

## Error Handling

### Common Error Responses

#### 1. Unknown Command
```
❓ Unknown Command

I didn't understand: INVALID_COMMAND

Type HELP to see available commands.
```

#### 2. File Not Found
```
📁 /ProjectX is empty or not found.
```

#### 3. Permission Denied
```
❌ Permission denied. You don't have access to this folder.
```

#### 4. File Too Large
```
⚠️ File is too large to process. Maximum size: 10MB
```

#### 5. Rate Limit Exceeded
```
⚠️ Rate limit exceeded. Please try again in a few minutes.
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | `AC1234567890abcdef` |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | `your_auth_token` |
| `TWILIO_WHATSAPP_NUMBER` | Twilio WhatsApp number | `whatsapp:+14155238886` |
| `GOOGLE_DRIVE_CLIENT_ID` | Google OAuth Client ID | `your_client_id` |
| `GOOGLE_DRIVE_CLIENT_SECRET` | Google OAuth Client Secret | `your_client_secret` |
| `GOOGLE_DRIVE_REFRESH_TOKEN` | Google OAuth Refresh Token | `your_refresh_token` |
| `GOOGLE_DRIVE_FOLDER_ID` | Default Google Drive folder ID | `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o` |
| `REQUIRE_CONFIRMATION_FOR_DELETE` | Require confirmation for deletions | `true` |
| `CONFIRMATION_KEYWORD` | Keyword required for deletion confirmation | `CONFIRM` |
| `MAX_FILES_PER_OPERATION` | Maximum files to process in one operation | `50` |
| `AUDIT_SPREADSHEET_ID` | Google Sheets ID for audit logging | - |

## Security Features

### 1. Command Validation

- All commands are validated before execution
- Path traversal attacks are prevented
- File size limits are enforced

### 2. Confirmation System

- Deletion operations require explicit confirmation
- Confirmation keyword can be customized
- Audit logging tracks all deletion attempts

### 3. Rate Limiting

- Built-in rate limiting to prevent abuse
- Configurable limits per user/operation
- Automatic throttling for large operations

### 4. Audit Logging

- All operations are logged with timestamps
- User information is captured
- Operation details are stored for review

## Performance Considerations

### 1. File Size Limits

- Maximum file size for processing: 10MB
- Maximum files per operation: 50 (configurable)
- Timeout for large operations: 5 minutes

### 2. Caching

- File metadata is cached for 5 minutes
- Summary results are cached for 1 hour
- Cache can be cleared via environment variable

### 3. Batch Operations

- Multiple files are processed in batches
- Progress updates for long-running operations
- Automatic retry for failed operations

## Monitoring and Logging

### 1. Audit Logs

All operations are logged with the following information:

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "command": "LIST",
  "fromNumber": "whatsapp:+1234567890",
  "originalMessage": "LIST /ProjectX",
  "response": "📁 Files in /ProjectX:...",
  "status": "completed",
  "executionTime": 1250,
  "filesProcessed": 3
}
```

### 2. Error Logs

Errors are logged with detailed information:

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "error": "Permission denied",
  "command": "DELETE",
  "fromNumber": "whatsapp:+1234567890",
  "filePath": "/ProjectX/report.pdf",
  "stackTrace": "..."
}
```

### 3. Performance Metrics

Performance metrics are tracked:

- Response time per command
- Success/failure rates
- Resource usage
- API call counts

## Troubleshooting

### Common Issues

1. **Webhook not receiving messages**
   - Check n8n accessibility from internet
   - Verify Twilio webhook URL configuration
   - Check n8n logs for errors

2. **Google Drive permission errors**
   - Ensure folder is shared with service account
   - Check OAuth scopes are correct
   - Verify refresh token is valid

3. **OpenAI API errors**
   - Check API key is correct
   - Verify account has credits
   - Check rate limiting

### Debug Mode

Enable debug mode by setting:

```bash
N8N_LOG_LEVEL=debug
```

This will provide detailed logging information for troubleshooting.

## Support

For additional support:

1. Check the troubleshooting section
2. Review the setup guide
3. Check n8n logs for detailed error information
4. Open an issue on GitHub with detailed information
