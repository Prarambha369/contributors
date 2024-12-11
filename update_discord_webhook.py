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

# Create embeds for the first 10 contributors
first_embeds = create_embeds(contributors[:10])

# Create embeds for the remaining contributors
remaining_embeds = create_embeds(contributors[10:])

# Prepare the payloads to update the Discord messages
first_payload = {
    "content": "Here are the latest TOP 10 contributors:",
    "embeds": first_embeds
}

remaining_payload = {
    "content": "Here are the remaining contributors:",
    "embeds": remaining_embeds
}

# Print the payloads for debugging
print(json.dumps(first_payload, indent=2))
print(json.dumps(remaining_payload, indent=2))

# Get the webhook URL and message ID from environment variables
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
message_id = os.getenv('DISCORD_MESSAGE_ID')

# Update the Discord message with the first payload
response = requests.patch(f'{webhook_url}/messages/{message_id}', json=first_payload)
print(f'Response status code: {response.status_code}')
print(f'Response text: {response.text}')

if response.status_code == 200:
    print('Webhook updated successfully with the first payload!')
else:
    print(f'Failed to update webhook with the first payload: {response.status_code} {response.text}')

# Send the second message with the remaining payload
response = requests.post(webhook_url, json=remaining_payload)
print(f'Response status code: {response.status_code}')
print(f'Response text: {response.text}')

if response.status_code == 200 or response.status_code == 204:
    print('Webhook updated successfully with the remaining payload!')
else:
    print(f'Failed to update webhook with the remaining payload: {response.status_code} {response.text}')
