import datetime
import json
import random

from flask import request, session
from twilio.twiml.messaging_response import MessagingResponse

from app import app, callers

@app.route("/", methods=["GET", "POST"])
def hello():
    """ Test route - respond with num messages sent between parties """
    with open("conversation.json", "r") as fl:
        txt = fl.read()
    msgs = json.loads(txt)
    intro = random.choice(msgs["introductions"])
    resp = MessagingResponse()
    resp.message(intro)
    return str(resp)
