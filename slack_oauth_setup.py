#!/usr/bin/env python3
"""
Slack OAuth Setup - Run once to get token
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import urllib.parse
import json
import os
import sys

def load_env():
    """Load environment variables from .env file"""
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env()

CLIENT_ID = os.getenv("SLACK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("SLACK_REDIRECT_URI", "http://localhost:8765/callback")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        code = params.get("code", [None])[0]

        if not code:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code param")
            return

        resp = requests.post("https://slack.com/api/oauth.v2.access", data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        })
        data = resp.json()

        if data.get("ok"):
            token_file = os.path.join(os.path.dirname(__file__), "slack_token.json")
            with open(token_file, "w") as f:
                json.dump(data, f, indent=2)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Token saved successfully!")
            print("✅ Token saved to slack_token.json")
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {data}".encode())

    def log_message(self, format, *args):
        pass

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Please create .env file with SLACK_CLIENT_ID and SLACK_CLIENT_SECRET!")
        print("📝 Copy .env.example to .env and fill in your credentials")
        sys.exit(1)

    server = HTTPServer(("localhost", 8765), Handler)
    print("🚀 OAuth server: http://localhost:8765/callback")
    print("🌐 Open this URL:")
    print(f"https://slack.com/oauth/v2/authorize?client_id={CLIENT_ID}"
          f"&user_scope=channels:history,groups:history,im:history,mpim:history,channels:read,groups:read,users:read"
          f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopped")

if __name__ == "__main__":
    main()