from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

callers = {
    "+18572654887": "Angie",
    "+19739082290": "Hala"
}

from app import routes
