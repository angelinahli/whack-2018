from twilio.rest import Client
from twilio_config import account_sid, auth_token, twilio_num, callers

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello world :)",
    from_=twilio_num,
    to=callers["Angie"])