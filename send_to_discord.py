import json
import requests
import os

# Load contributors.json
with open('contributors.json', 'r') as file:
    contributors = json.load(file)

# Prepare the message
message = "Contributors:\n"
for contributor in contributors:
    message += f"{contributor['login']}: {contributor['contributions']} contributions\n"

# Send the message to Discord
discord_webhook_url = os.environ['DISCORD_WEBHOOK_URL']
data = {
    "content": message
}
response = requests.post(discord_webhook_url, json=data)

if response.status_code == 204:
    print("Message sent to Discord successfully!")
else:
    print(f"Failed to send message to Discord. Status code: {response.status_code}")

