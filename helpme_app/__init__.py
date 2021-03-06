from flask import Flask
from flask_ask import Ask


app = Flask(__name__)
ask = Ask(app, "/")

app.config.from_pyfile("config.py")

import helpme_app.views
