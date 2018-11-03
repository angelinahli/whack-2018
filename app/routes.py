import datetime
import json
import random

from flask import request, session

from app import app, bot
from config import VERIFY_TOKEN

LAST_STATUS = None
SECONDARY_STATUS = None

@app.route("/", methods=["GET", "POST"])
def receive_message():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output["entry"]:
            messaging = event["messaging"]
            for message in messaging:
                if message.get("message"):
                    recipient_id = message["sender"]["id"]
                    text = message["message"].get("text").strip().lower()
                    if text:
                        response_sent_text = get_message(text)
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message(text):
    with open("conversation.json", "r") as fl:
        txt = fl.read()
    conv = json.loads(txt)

    if not LAST_STATUS or \
        (LAST_STATUS == "ONBOARDING" and SECONDARY_STATUS == "REFUSE"):
        LAST_STATUS = "INTRODUCTION"
        return random.choice(conv[LAST_STATUS])

    elif LAST_STATUS == "INTRODUCTION":
        LAST_STATUS = "ONBOARDING"
        SECONDARY_STATUS = "START"
        return conv[LAST_STATUS][SECONDARY_STATUS]

    elif LAST_STATUS == "ONBOARDING" and SECONDARY_STATUS == "START":
        SECONDARY_STATUS = "SUCCESS" if txt == "yes" else "REFUSE"
        return conv[LAST_STATUS][SECONDARY_STATUS]

    return "Hi :)"

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Success"
