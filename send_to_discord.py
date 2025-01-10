import os
import requests
import json

# Ensure the Discord webhook URL is set
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
if not webhook_url:
    raise ValueError("Discord webhook URL is not set")

# Ensure the Discord message ID is set
message_id = os.getenv('DISCORD_MESSAGE_ID')
if not message_id:
    raise ValueError("Discord message ID is not set")

# Read contributors.json
with open('contributors.json', 'r') as file:
    contributors = json.load(file)

# Ensure contributors.json is not empty
if not contributors:
    raise ValueError("contributors.json is empty")

# Sort contributors by contributions and get top 10
top_contributors = sorted(contributors, key=lambda x: x['contributions'], reverse=True)[:10]

# Create embeds
def create_embeds(contributors):
    embeds = []
    for contributor in contributors:
        embed = {
            "title": contributor["name"],
            "color": int("4A90E2", 16),
            "username": contributor["login"],
            "description": contributor.get("bio", "No bio provided"),
            "footer": {"text": f"Total contributions: {contributor['contributions']}"},
            "url": contributor["html_url"],
            "thumbnail": {"url": contributor["avatar_url"]},
        }
        embeds.append(embed)
    return embeds

# Prepare the payload with top 10 contributors
payload = {"embeds": create_embeds(top_contributors)}

# Edit the existing message
edit_url = f"{webhook_url}/messages/{message_id}"
response = requests.patch(edit_url, json=payload)

# Check the response from Discord
if response.status_code not in [200, 204]:
    raise Exception(f"Failed to update webhook: {response.status_code} {response.text}")
