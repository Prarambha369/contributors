import os
import requests
import json

# Load the contributors.json file
with open('contributors.json', 'r') as file:
    contributors = json.load(file)

# Function to create embeds
def create_embeds(contributors):
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
            ]
        }
        embeds.append(embed)
    return embeds

# Split contributors into chunks of 10
chunks = [contributors[i:i + 10] for i in range(0, len(contributors), 10)]

# Get the webhook URL from environment variables
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

# Send each chunk as a separate message
for i, chunk in enumerate(chunks):
    payload = {
        "content": f"Contributors batch {i + 1}:",
        "embeds": create_embeds(chunk)
    }
    
    # Print the payload for debugging
    print(json.dumps(payload, indent=2))
    
    # Send the message
    response = requests.post(webhook_url, json=payload)
    print(f'Response status code: {response.status_code}')
    print(f'Response text: {response.text}')
    
    if response.status_code == 200 or response.status_code == 204:
        print(f'Webhook updated successfully with batch {i + 1}!')
    else:
        print(f'Failed to update webhook with batch {i + 1}: {response.status_code} {response.text}')
