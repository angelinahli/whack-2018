from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pymessenger.bot import Bot

from config import Config, ACCESS_TOKEN

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bot = Bot(ACCESS_TOKEN)

from app import routes, models
