from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from pprint import pprint as pp
import logging
import re

# https://api.slack.com/apis/connections/socket

slack_bot_token = os.environ['SLACK_TOKEN']
slack_app_token = os.environ["SLACK_APP_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

logger = logging.getLogger(__name__)

# client = WebClient(token=slack_bot_token)
# response = client.apps_connections_open(app_token=slack_app_token)
# print(response['url'])

# client = WebClient(token=slack_bot_token)
# client.chat_postMessage(channel='#slackbottest', text='Hello')

# Instantiate the Slack app
app = App(token=slack_bot_token, signing_secret=slack_signing_secret)

#Define a handler for incoming messages
@app.event("app_mention")
def handle_mention(event, say):
    # Extract the username and achievement name from the message
    text: str = event["text"]
    username: str = text.split(" ")[0][1:]
    achievement_name: str = text.split("asked for ")[1][:-1]
    print(text)

    # Create a message to send to the admin
    message = f"{username} asked for the achievement \"{achievement_name}\""
    blocks = [
            {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Accept"
                        },
                        "style": "primary",
                        "value": "accept",
                        "action_id": "accept"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Decline"
                        },
                        "style": "danger",
                        "value": "decline",
                        "action_id": "decline"
                    }
                ]
            }
    ]
    # Send the message to the admin
    say(blocks=blocks)


@app.message("knock knock")
def ask_who(message, say):
    say("_Who's there?_")

# Define a handler for button clicks
@app.action(re.compile("(accept|decline)"))
def handle_button_click(ack, body, client):
    # print("\n\n\n\nteste2\n\n\n\n")
    # Get the user who clicked the button and the action they took
    user_id = body["user"]["id"]
    value = body["actions"][0]["value"]
    pp(body)
    pp(client)
    if value == "accept":
        ack("Achievement granted!")
    elif value == "decline":
        # Send a message to the user letting them know their request was declined
        client.chat_postEphemeral(
            channel=user_id,
            user=user_id,
            text="Your achievement request was declined."
        )
        ack("Achievement declined.")

# Start the Slack app
if __name__ == "__main__":
    handler = SocketModeHandler(app=app, app_token=slack_app_token)
    handler.start()