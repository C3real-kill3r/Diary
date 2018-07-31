from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "brylee"

from users.routes import users
from entries.routes import entries
from routes import main

app.register_blueprint(users, url_prefix='/api/v2')
app.register_blueprint(entries, url_prefix='/api/v2')
app.register_blueprint(main, url_prefix='/api/v2')