from flask import Flask
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
app = Flask(__name__)
app.config['SECRET_KEY'] = "brylee"


from users.routes import users
from entries.routes import entries
from routes import main

app.register_blueprint(users, url_prefix='/api/v2')
app.register_blueprint(entries, url_prefix='/api/v2')
app.register_blueprint(main, url_prefix='/api/v2')