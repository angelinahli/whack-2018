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


def get_next_msg_key(txt, user):
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
            "INTERV_START":"INVERV_YES",
            "INTERV_YES":"INTERV_TYPE",
            "INTERV_TYPE":"INTERV_LENGTH",
            "INTERV_LENGTH":"INTERV_PROMPT",
            "INTERV_PROMPT":"INTERV_FEEDBACK",
            "INTERV_FEEDBACK":"INTERV_KEEP",
            "INTERV_KEEP":"INTERV_END",
            "INTERV_END":"JOURNAL_START",
            "INTERV_NO":"JOURNAL_START",
            "JOURNAL_YES":"JOURNAL_PROMPT",
            "JOURNAL_PROMPT":"JOURNAL_END",
            "JOURNAL_END":"WRAPUP"}
    
    if prev_key in key_dict:
        return key_dict[prev_key]
    
    p_head = prev_key.split("_")[0]
    p_fork = prev_key.split("_")[1]
    if p_fork == "INTRODUCTION":
        if user.has_onboarded == False:
            next_key = "ONBOARDING_START"
        else:
            next_key = "CHECKIN_START"

    elif p_fork == "START":
        if "no" in txt:
            next_key = p_head + "_NO"
        else:
            next_key = p_head = "_YES"
                
    return next_key

        
def get_checkin_resp(txt):
    error_req = "Please enter a number between 1 & 5 :)"
    if not txt.isdigit():
        return "Sorry, I didn't understand that! " + error_req
    val = int(txt)
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
    pass

def handle_prev_resp(user, txt):
    # before we move on, we have to handle the info the user sent us
    # handle cases that require additional processing
    if msg_key == "ONBOARDING_FINISH":
        pass
    elif msg_key == "CHECKIN_BASELINE":
        pass
    elif msg_key == "":
        pass
        
def get_next_resp_text(user, txt):
    msg_key = get_next_msg_key(user, txt)
    with open("conversation.json", "r") as fl:
        txt = fl.read()
    convos = json.loads(txt)
    
    # grab response text
    resp_txt = None
    if msg_key in convos:
        resp_txt = random.choice(convos.get(msg_key))
    
    # there are some things we need to personalize
    elif msg_key == "CHECKIN_RESP":
        resp_txt = get_checkin_resp(user, txt)
    elif msg_key == "INTERV_PROMP"
        resp_txt = get_interv_prompt(user, txt)
    return resp_txt

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
            resp_text = get_next_resp_text(user, txt)
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
