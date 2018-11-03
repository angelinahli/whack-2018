from flask import Flask
from config import Config, ACCESS_TOKEN

app = Flask(__name__)
app.config.from_object(Config)
bot = Bot(ACCESS_TOKEN)

from app import routes
