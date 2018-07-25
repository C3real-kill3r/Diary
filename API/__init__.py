from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "brylee"

from users.routes import users
from entries.routes import entries
from routes import main

app.register_blueprint(users)
app.register_blueprint(entries)
app.register_blueprint(main)