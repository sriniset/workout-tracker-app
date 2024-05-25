from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


#creating app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

#load configuration
app.config.from_object('config.Config')

#init DB
db = SQLAlchemy(app)

#get the routes
from routes import *

if __name__ == '__main__':
    app.run(port = 8000, debug=True)