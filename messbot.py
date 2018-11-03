import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAADv4LxOKP8BAAAG7iC6N1MnF6iNJlmLxZB9l4ZBSMKUh6FqJDC9CNdMhIRbTl3SqcunaMpwwnA7MMtF6cHzVDOuDDJhzr2LTR3xMHZAtdl0zpDLr6gg4ZBbvd5GhCb4ZCDdIFUAQmZChVjv4bUPDJ8kR2uimLMyCbGFAgUwe0Lv1bg4RlYRZB5'
VERIFY_TOKEN = 'PROOF_BY_EXAMPLE'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:

        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)

                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):


    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    sample_responses = ["You are loved.", "You are important", "The world is a better place with you in it."]
    return random.choice(sample_responses)

def send_message(recipient_id, response):

    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run(debug=True)
