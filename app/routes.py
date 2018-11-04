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

def add_user(fb_id):
    user = User(
        fb_id=fb_id, 
        mid_conversation=True, 
        has_onboarded=False,
        last_action="NONE"
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_user(fb_id):
    user = User.query.filter_by(fb_id=fb_id).first()
    # if this is the first time the user has been seen, add them
    if not user:
        add_user(fb_id)
        user = User.query.filter_by(fb_id=fb_id).first()
    return user

def get_next_msg_key(user, txt):
    prev_key = user.last_action
    key_dict = {
        "NONE":"INTRODUCTION",
        "WRAPUP":"INTRODUCTION",
        "ONBOARDING_START":"ONBOARDING_ASK",
        "ONBOARDING_ASK":"ONBOARDING_FINISH",
        "ONBOARDING_FINISH":"CHECKIN_START",
        "CHECKIN_NO":"JOURNAL_START",
        "CHECKIN_YES":"CHECKIN_BASELINE",
        "CHECKIN_BASELINE":"CHECKIN_RESP",
        "CHECKIN_RESP":"INTERV_START",
        "INTERV_START":"INTERV_YES",
        "INTERV_YES":"INTERV_TYPE",
        "INTERV_TYPE":"INTERV_LENGTH",
        "INTERV_LENGTH":"INTERV_PROMPT",
        "INTERV_PROMPT":"INTERV_FEEDBACK",
        "INTERV_FEEDBACK":"INTERV_KEEP",
        "INTERV_KEEP":"INTERV_END",
        "INTERV_END":"JOURNAL_START",
        "INTERV_NO":"JOURNAL_START",
        "JOURNAL_YES":"JOURNAL_PROMPT",
        "JOURNAL_NO":"WRAPUP",
        "JOURNAL_PROMPT":"JOURNAL_END",
        "JOURNAL_END":"WRAPUP"
    }
    
    if prev_key in key_dict:
        return key_dict[prev_key]
    
    if prev_key == "INTRODUCTION":
        return "ONBOARDING_START" if not user.has_onboarded else "CHECKIN_START"
    
    split_key = prev_key.split("_")
    if len(split_key) == 2 and split_key[1] == "START":
        return split_key[0] + "_NO" if "no" in txt else split_key[0] + "_YES"
        
def get_checkin_resp(txt):
    error_req = "Please enter a number between 1 & 5 :)"
    val = None
    try:
        val = int(txt)
    except ValueError:
        return "Sorry, I didn't understand that! " + error_req
    if val < 1 or val > 5:
        return "Sorry, I didn't catch that! " + error_req
    if val in [1, 2]:
        return "I'm sorry to hear that you're having a rough day :( " \
               + "I hope I can be helpful!"
    elif val in [3, 4]:
        return "That's great! :) Let's see if we can make your day rock " \
               + "even more!"
    elif val == 5:
        return "You go Glen Coco!!! Power to you 👏👏"
    return "Sorry, something went wrong :/ That's my bad! Will you tell me " \
           + "again? " + error_req

def get_interv_prompt(user, txt):
    return "interv_prompt_text"

def handle_prev_resp(user, txt):
    # before we move on, we have to handle the info the user sent us
    # handle cases that require additional processing
    pass
       
def get_next_resp_text(user, txt, msg_key):
    with open("conversation.json", "r") as fl:
        conv_text = fl.read()
    convos = json.loads(conv_text)
    
    # grab response text
    resp_txt = None
    if msg_key in convos:
        return random.choice(convos.get(msg_key))
    
    # there are some things we need to personalize
    elif msg_key == "CHECKIN_RESP":
        return get_checkin_resp(txt)
    elif msg_key == "INTERV_PROMPT":
        return get_interv_prompt(user, txt)

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

                # process what the user sent us
                handle_prev_resp(user, txt)

                mess = Message(
                    user_id = user.user_id,
                    text = txt) 
                db.session.add(mess)
                db.session.commit()

            # figure out what to do next
            next_msg_key = get_next_msg_key(user, txt)
            print("\n\n\nTESTING")
            print(user.last_action, next_msg_key)
            print("\n\n\n")
            resp_text = get_next_resp_text(user, txt, next_msg_key)
            send_message(fb_id, resp_text)
            
            user.last_action = next_msg_key
            db.session.commit()
            db.session.close()

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
