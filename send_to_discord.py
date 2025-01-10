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
            "title": contributor.get("name", contributor["login"]),
            "color": 0x4A90E2,  # GNOME blue color
            "description": contributor.get("bio", "No bio provided"),
            "footer": {"text": f"Total contributions: {contributor['contributions']}"},
            "url": contributor["html_url"],
            "thumbnail": {"url": contributor["avatar_url"]},
            "fields": [
                {"name": "GitHub Username", "value": contributor["login"], "inline": True},
                {"name": "Company", "value": contributor.get("company", "N/A"), "inline": True},
                {"name": "Email", "value": contributor.get("email", "N/A"), "inline": True},
                {"name": "Website", "value": contributor.get("blog", "N/A"), "inline": True},
                {"name": "Twitter", "value": contributor.get("twitter_username", "N/A"), "inline": True},
                {"name": "Hireable", "value": "Yes" if contributor.get("hireable") else "No", "inline": True},
                {"name": "Location", "value": contributor.get("location", "N/A"), "inline": True},
                {"name": "Bio", "value": contributor.get("bio", "N/A"), "inline": False},
                {"name": "Public Repos", "value": str(contributor.get("public_repos", "N/A")), "inline": True},
                {"name": "Followers", "value": str(contributor.get("followers", "N/A")), "inline": True},
                {"name": "Following", "value": str(contributor.get("following", "N/A")), "inline": True},
                {"name": "> Feature by", "value": "> <@1132618599798947871>", "inline": True}
            ]
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
