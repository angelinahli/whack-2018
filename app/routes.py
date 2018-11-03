import datetime
import json
import random

from flask import request, session

from app import app, bot, db
from app.models import User, Intervention, CheckIn, Message
from config import VERIFY_TOKEN

### Helper functions

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Success"

def get_user(fb_id):
    user = User.query.filter_by(fb_id=fb_id).first()
    # if this is the first time the user has been seen, add them
    if not user:
        user = User(
            fb_id=fb_id, 
            mid_conversation=True, 
            has_onboarded=False,
            last_action="NONE")
        db.session.add(user)
        db.session.commit()
    return user

def get_next_msg_key(prev_key):
    """ """
    pass

def get_random_message(msg_key):
    pass

def get_checkin_resp():
    pass

def get_interv_prompt():
    pass

def get_next_resp(user):
    pass

def handle_post_message(output):
    try:
        event = output["entry"][0]
        messaging = event["messaging"]
        msg = messaging[0]

        # otherwise we don't want to do anything
        if msg.get("message"):
            fb_id = msg["sender"]["id"]
            user = get_user(fb_id)

            # save the user message
            txt = None
            if msg["message"].get("text"):
                txt = msg["message"]["text"].strip().lower()
                mess = Message(
                    user_id = user.user_id,
                    text = txt) 
                db.session.add(mess)
                db.session.commit()            

            # figure out what to do next

            resp_text = "Test message"  # need to add response text here
            send_message(fb_id, resp_text)
    # this is fine, it's just easier to try except than use for loops 
    except IndexError: 
        print("User didn't have a message")
    return "Post message processed"

### Main route

@app.route("/", methods=["GET", "POST"])
def receive_message():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
         output = request.get_json()
         handle_post_message(output)
    return "Message Processed"
