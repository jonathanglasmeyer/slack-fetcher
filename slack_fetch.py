#!/usr/bin/env python3
"""
Slack Post Fetcher - Returns JSON data for Claude processing
Usage: python slack_fetch.py <slack_url>
"""
import requests
import json
import os
import sys
import re
from datetime import datetime

class SlackFetcher:
    def __init__(self):
        self.token = None
        self.load_token()

    def load_token(self):
        """Load Slack token from file"""
        token_file = os.path.join(os.path.dirname(__file__), "slack_token.json")
        if not os.path.exists(token_file):
            print(json.dumps({"error": "No token file found. Run slack_oauth_setup.py first!"}))
            sys.exit(1)

        with open(token_file, "r") as f:
            data = json.load(f)
            self.token = data.get("authed_user", {}).get("access_token")
            if not self.token:
                print(json.dumps({"error": "No access token found in token file!"}))
                sys.exit(1)

    def parse_slack_url(self, url):
        """Parse Slack URL to extract channel and message timestamp"""
        pattern = r"https://[^.]+\.slack\.com/archives/([^/]+)/p(\d+)(\d{6})"
        match = re.match(pattern, url)

        if not match:
            raise ValueError("Invalid Slack URL format")

        channel = match.group(1)
        timestamp = f"{match.group(2)}.{match.group(3)}"

        return {"channel": channel, "timestamp": timestamp}

    def fetch_message(self, channel, timestamp):
        """Fetch message from Slack API"""
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "channel": channel,
            "latest": timestamp,
            "oldest": timestamp,
            "inclusive": "true",
            "limit": 1
        }

        response = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params)
        data = response.json()

        if not data.get("ok"):
            raise Exception(f"Slack API error: {data.get('error', 'Unknown error')}")

        messages = data.get("messages", [])
        if not messages:
            raise Exception("Message not found")

        return messages[0]

    def fetch_user_info(self, user_id):
        """Fetch user info"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get("https://slack.com/api/users.info", headers=headers, params={"user": user_id})
        data = response.json()
        return data.get("user", {}) if data.get("ok") else {}

    def fetch_channel_info(self, channel_id):
        """Fetch channel info"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get("https://slack.com/api/conversations.info", headers=headers, params={"channel": channel_id})
        data = response.json()
        return data.get("channel", {}) if data.get("ok") else {}

    def fetch_from_url(self, url):
        """Main method - returns structured data"""
        try:
            url_info = self.parse_slack_url(url)
            message = self.fetch_message(url_info["channel"], url_info["timestamp"])

            user_info = self.fetch_user_info(message.get("user", ""))
            channel_info = self.fetch_channel_info(url_info["channel"])

            timestamp = float(message.get("ts", 0))
            date = datetime.fromtimestamp(timestamp)

            result = {
                "success": True,
                "date": date.strftime("%Y-%m-%d"),
                "datetime": date.strftime("%Y-%m-%d %H:%M:%S"),
                "author": user_info.get("real_name", user_info.get("name", "Unknown User")),
                "channel": channel_info.get("name", "Unknown Channel"),
                "text": message.get("text", ""),
                "url": url,
                "timestamp": timestamp
            }

            # Add attachments if present
            if message.get("attachments"):
                result["attachments"] = message["attachments"]

            return result

        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"success": False, "error": "Usage: python slack_fetch.py <slack_url>"}))
        sys.exit(1)

    url = sys.argv[1]
    fetcher = SlackFetcher()
    result = fetcher.fetch_from_url(url)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()