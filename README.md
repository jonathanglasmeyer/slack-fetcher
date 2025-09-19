# Slack Fetcher

Simple Python tool to fetch Slack messages via URL for knowledge management workflows.

## Features

- **URL-based fetching**: Paste any Slack message URL to get structured data
- **Complete metadata**: Author, channel, timestamp, message content
- **JSON output**: Perfect for automation and AI workflows
- **OAuth authentication**: Secure user-based access

## Quick Start

### Option A: Use Existing Slack App (Easiest)

If someone already created a Slack app for your workspace:

1. **Get access to the existing Slack app** (ask the app owner to add you as collaborator)
2. **Install dependencies**: `pip install requests`
3. **Get your OAuth token**:
   - Go to the Slack app in your browser
   - Click "Install to [Workspace]" or "Reinstall to [Workspace]"
   - Copy the **User OAuth Token** that appears
4. **Create token file**:
   ```bash
   # Create slack_token.json
   {
     "authed_user": {
       "access_token": "xoxp-YOUR-TOKEN-HERE"
     }
   }
   ```
5. **Test it**: `python slack_fetch.py "https://yourworkspace.slack.com/archives/CHANNEL/pTIMESTAMP"`

### Option B: Create Your Own Slack App (Advanced)

<details>
<summary>Click to expand full setup instructions</summary>

1. Go to https://api.slack.com/apps → "Create New App" → "From scratch"
2. Add OAuth scopes:
   - `channels:read`, `channels:history`
   - `groups:read`, `groups:history`
   - `im:history`, `mpim:history`, `users:read`
3. **Easy Install Method**:
   - Use the "Install to Workspace" button in Slack Console
   - Copy the User OAuth Token that appears
   - Create `slack_token.json` with token (see format above)
4. **Advanced OAuth Method** (only if you need programmatic setup):
   - Configure redirect URLs and use `slack_oauth_setup.py`
   - Requires ngrok setup for local development

</details>

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