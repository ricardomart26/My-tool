import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_BOT_TOKEN = "xoxb-5074915163094-5082163755315-dyLS9cfPHRIA7pNtFfcEIjNa"
SLACK_APP_TOKEN = "xapp-1-A0533UMKJJC-5106144698320-edbfc5b3a6aca9edab3f918b8d266a0a6ec95010b54cc1f7c504b5acdcd10af6"
# Initialize your app with socket mode enabled
app = App(token=SLACK_BOT_TOKEN, name="Test Bot")

# Define the handler for the "app_mention" event
@app.event("app_mention")
def handle_mention(event, say):
    # Do something in response to the mention
    say(f"You mentioned me, <@{event['user']}>!")

@app.event("app_home_opened")
def say_hw(message, say):
    say("Hello World!")

def main():
    # Start the Socket Mode handler
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

# Define the entry point for your app
if __name__ == "__main__":
    main()