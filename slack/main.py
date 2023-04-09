from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from pprint import pprint as pp
import logging


# https://api.slack.com/apis/connections/socket

slack_bot_token = os.environ['SLACK_TOKEN']
slack_app_token = os.environ["SLACK_APP_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

logger = logging.getLogger(__name__)

client = WebClient(token=slack_bot_token)
response = client.apps_connections_open(app_token=slack_app_token)
print(response['url'])

# client = WebClient(token=slack_bot_token)
# client.chat_postMessage(channel='#slackbottest', text='Hello')

# Instantiate the Slack app
app = App(token=slack_bot_token, signing_secret=slack_signing_secret)

# Define a handler for incoming messages
@app.event("app_mention")
def handle_mention(event, say):
    # Extract the username and achievement name from the message
    print('teste')
    text = event["text"]
    username = text.split(",")[0][1:]
    achievement_name = text.split("asked for ")[1][:-1]

    # Create a message to send to the admin
    message = f"{username} asked for the achievement \"{achievement_name}\""
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            },
            "accessory": {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Accept"
                        },
                        "style": "primary",
                        "value": "accept"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Decline"
                        },
                        "style": "danger",
                        "value": "decline"
                    }
                ]
            }
        }
    ]
    
    # Send the message to the admin
    say(blocks=blocks)


@app.message("knock knock")
def ask_who(message, say):
    say("_Who's there?_")

# Define a handler for button clicks
@app.action("accept-decline")
def handle_button_click(ack, body, client):
    # Get the user who clicked the button and the action they took
    user_id = body["user"]["id"]
    value = body["actions"][0]["value"]

    if value == "accept":
        # Call the third-party API to grant the achievement to the user
        # If successful, send a confirmation message to the user and admin
        ack("Achievement granted!")
    elif value == "decline":ç
        # Send a message to the user letting them know their request was declined
        client.chat_postEphemeral(
            channel=body["channel"]["id"],
            user=user_id,
            text="Your achievement request was declined."
        )
        ack("Achievement declined.")

# Start the Slack app
if __name__ == "__main__":
    handler = SocketModeHandler(app, slack_app_token)
    # print(handler.app_token)
    # for user in client.users_list():
    #     for member in user['members']:
    #         print(member['profile']['display_name'])

    # for conversation in client.conversations_list():
    #     print(conversation)
    # while True:
    #     handler.connect()
    handler.start()