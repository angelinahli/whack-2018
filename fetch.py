from datetime import datetime
from app import db
from app.models import User
from app.models import Intervention
from app.models import CheckIn
from app.routes import send_message

from app.routes import get_user

u = User.query.get(2).fb_id
if User.query.get(2).has_onboarded == False:
	send_message(u, "Hi! What is your name? ")

