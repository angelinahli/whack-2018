import datetime
import json
import random

from flask import request, session

from app import app, bot, db
from app.models import User, Intervention, UserIntervention, CheckIn, Message
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

    interventions = Intervention.query.all()
    for interv in interventions:
        ui = UserIntervention(
            user_id=user.user_id, 
            intervention_id=interv.intervention_id)
        db.session.add(ui)

    db.session.commit()

def get_user(fb_id):
    user = User.query.filter_by(fb_id=fb_id).first()
    # if this is the first time the user has been seen, add them
    if not user:
        add_user(fb_id)
        user = User.query.filter_by(fb_id=fb_id).first()
    return user

def valid_score(txt):
    return txt.isdigit() and 1 <= int(txt) <= 5

def valid_yes_no(txt):
    return txt in ["yes", "yup", "no", "nah", "nope", "yah"]

def handle_prev_resp(user, txt):
    # before we move on, we have to handle the info the user sent us
    # handle cases that require additional processing
    key = user.last_action
    is_error = False

    # validate responses
    if key in ["CHECKIN_START", "INTERV_START", "JOURNAL_START", 
            "INTERV_KEEP"] and not valid_yes_no(txt):
        is_error = True
    if key in ["CHECKIN_BASELINE", "INTERV_FEEDBACK"] and not valid_score(txt):
        is_error = True

    if key == "ONBOARDING_FINISH":
        user.has_onboarded = True
        db.session.commit()

    # make changes
    # TODO: do this
    if key == "CHECKIN_BASELINE":
        pass
    if key == "INTERV_FEEDBACK":
        pass
    if key == "INTERV_KEEP":
        new_interv = Intervention(text=txt)
        db.session.add(new_interv)
        ui = UserIntervention(
            user_id=user.user_id, 
            intervention_id=new_interv.intervention_id)
        db.session.add(ui)
        db.session.commit()

    return is_error

def get_next_msg_key(user, txt):
    prev_key = user.last_action
    key_dict = {
        "NONE": "INTRODUCTION",
        "WRAPUP": "INTRODUCTION",
        "ONBOARDING_START": "ONBOARDING_ASK",
        "ONBOARDING_ASK": "ONBOARDING_FINISH",
        "ONBOARDING_FINISH": "CHECKIN_START",
        "CHECKIN_NO": "JOURNAL_START",
        "CHECKIN_YES": "CHECKIN_BASELINE",
        "CHECKIN_BASELINE": "CHECKIN_RESP",
        "CHECKIN_RESP": "INTERV_START",
        "INTERV_YES": "INTERV_PROMPT",
        "INTERV_NO": "JOURNAL_START",
        "INTERV_PROMPT": "INTERV_FEEDBACK",
        "INTERV_FEEDBACK": "INTERV_KEEP",
        "INTERV_KEEP": "INTERV_END",
        "INTERV_END": "JOURNAL_START",
        "JOURNAL_YES": "JOURNAL_PROMPT",
        "JOURNAL_NO": "WRAPUP",
        "JOURNAL_PROMPT": "JOURNAL_END",
        "JOURNAL_END": "WRAPUP"
    }
    
    if prev_key in key_dict:
        return key_dict[prev_key]
    
    if prev_key == "INTRODUCTION":
        return "ONBOARDING_START" if not user.has_onboarded else "CHECKIN_START"
    
    split_key = prev_key.split("_")
    if len(split_key) == 2 and split_key[1] == "START":
        return split_key[0] + "_NO" if txt in ["no", "nah", "nope"] else \
               split_key[0] + "_YES"

def get_yes_no_resp(txt, default_msg):
    if not valid_yes_no(txt):
        return "Sorry, I didn't understand that! Try entering 'yes' or 'no' :)"
    return default_msg

def get_score_resp(txt, default_msg):
    if not valid_score(txt):
        return "Sorry, I didn't understand that! Please enter a whole number " \
                + "between 1 & 5 :)"
    if default_msg:
        return default_msg

    val = int(txt)
    if val in [1, 2]:
        return "I'm sorry to hear that you're having a rough day :( I hope " \
                + "I can be helpful!"
    elif val in [3, 4]:
        return "That's great! :) Let's see if we can make your day rock even more!"
    elif val == 5:
        return "You go Glen Coco!!! Power to you 👏👏"

def get_interv_prompt(user):
    intervs = UserIntervention.query.filter_by(user_id=user.user_id)
    interv = random.choice(intervs)
    txt = Intervention.query.get(interv.intervention_id).text
    return txt + " (Let me know when you're done!)"
       
def get_next_resp_text(user, txt, prev_key, msg_key, convos):
    msg = random.choice(convos.get(msg_key, dict()).get("messages", [None]))
    # there are some things we need to personalize
    if msg_key in ["CHECKIN_RESP", "INTERV_KEEP"]:
        return get_score_resp(txt, default_msg=msg)
    elif prev_key in ["CHECKIN_START", "INTERV_START", "JOURNAL_START", 
                      "INTERV_KEEP"]:
        return get_yes_no_resp(txt, default_msg=msg)
    elif msg_key == "INTERV_PROMPT":
        return get_interv_prompt(user)
    return msg

def handle_post_message(output):
    try:
        event = output["entry"][0]
        messaging = event["messaging"]
        msg = messaging[0]

        # otherwise we don't want to do anything
        if msg.get("message") and msg["message"].get("text"):
            fb_id = msg["sender"]["id"]
            user = get_user(fb_id)
            txt = msg["message"]["text"].strip().lower()

            # process what the user sent us
            error_resp = handle_prev_resp(user, txt)

            add a message
            mess = Message(
                user_id = user.user_id,
                text = txt) 
            db.session.add(mess)
            db.session.commit()

            # figure out what to do next
            prev_key = user.last_action
            with open("conversation.json", "r") as fl:
                conv_text = fl.read()
            convos = json.loads(conv_text)

            # send a follow up message to the user
            next_msg_key = get_next_msg_key(user, txt)
            resp_text = get_next_resp_text(
                user, txt, prev_key, next_msg_key, convos)
            send_message(fb_id, resp_text)

            # if we got a valid input / can move on
            if not error_resp:
                user.last_action = next_msg_key 
                db.session.commit()

            prev_key = user.last_action
            while True:
                # if we're now waiting for the user to respond
                if prev_key != "NONE" and (
                        convos.get(prev_key).get("user_response") == 1 or error_resp):
                    break

                next_msg_key = get_next_msg_key(user, txt)
                resp_text = get_next_resp_text(
                    user, txt, prev_key, next_msg_key, convos)
                send_message(fb_id, resp_text)

                # if we got a valid input / can move on
                if not error_resp:
                    user.last_action = next_msg_key 
                    db.session.commit()

                prev_key = user.last_action

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
