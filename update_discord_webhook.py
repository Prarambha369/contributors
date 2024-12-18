import requests
import json

# Load the contributors.json file
with open('contributors.json', 'r') as file:
    contributors = json.load(file)

# Prepare the embeds for the Discord message
embeds = []
for contributor in contributors:
    embed = {
        "title": contributor["name"],
        "description": contributor["bio"],
        "url": contributor["html_url"],
        "thumbnail": {
            "url": contributor["avatar_url"]
        },
        "fields": [
            {
                "name": "GitHub Username",
                "value": contributor["login"],
                "inline": True
            },
            {
                "name": "Company",
                "value": contributor.get("company", "N/A"),
                "inline": True
            }
        ],
        "color": 0x2ECC71,
        "footer": {
            "text": f"Contributions: {contributor['contributions']}"
        }
    }
    embeds.append(embed)

# Prepare the payload to update the Discord message
payload = {
    "content": "Here are the latest contributors:",
    "embeds": embeds
}

# Update the Discord message
webhook_url = 'DISCORD_WEBHOOK_URL'
message_id = 'DISCORD_MESSAGE_ID'
response = requests.patch(f'{webhook_url}/messages/{message_id}', json=payload)
if response.status_code == 200:
    print('Webhook updated successfully!')
else:
    print(f'Failed to update webhook: {response.status_code} {response.text}')