# Slack Fetcher

Simple Python tool to fetch Slack messages via URL for knowledge management workflows.

## Features

- **URL-based fetching**: Paste any Slack message URL to get structured data
- **Complete metadata**: Author, channel, timestamp, message content
- **JSON output**: Perfect for automation and AI workflows
- **OAuth authentication**: Secure user-based access

## Quick Start

### 1. Create Slack App

1. Go to https://api.slack.com/apps
2. Create new app → "From scratch"
3. Add OAuth scopes:
   - `channels:read`, `channels:history`
   - `groups:read`, `groups:history`
   - `im:history`, `mpim:history`
   - `users:read`

### 2. Setup Environment

```bash
# Install dependencies
pip install requests
# or use uv:
uv sync

# Configure credentials
cp .env.example .env
# Edit .env with your Slack app credentials
```

### 3. Get OAuth Token

```bash
# Setup ngrok for OAuth callback
ngrok http 8765

# Update .env with ngrok URL
# Run OAuth setup
python slack_oauth_setup.py

# Follow OAuth flow in browser
```

### 4. Fetch Messages

```bash
python slack_fetch.py "https://yourworkspace.slack.com/archives/CHANNEL/pTIMESTAMP"
```

## Output Format

```json
{
  "success": true,
  "date": "2024-03-15",
  "datetime": "2024-03-15 14:30:25",
  "author": "John Doe",
  "channel": "general",
  "text": "Message content here...",
  "url": "https://yourworkspace.slack.com/archives/C123/p1710507025123456",
  "timestamp": 1710507025.123456
}
```

## Use Cases

- **Knowledge Management**: Extract important discussions for documentation
- **AI Workflows**: Feed structured message data to AI tools
- **Content Archival**: Backup important Slack conversations
- **Cross-platform Integration**: Bridge Slack with other tools

## Security

- Uses OAuth 2.0 for secure authentication
- Personal access tokens (user-scoped)
- No hardcoded credentials
- Minimal required permissions

## Requirements

- Python 3.8+
- Slack workspace access
- Slack app with appropriate OAuth scopes

## License

MIT