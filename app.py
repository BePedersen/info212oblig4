from flask import Flask, request, jsonify
from models import db
from routes import routes

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to Car Rental API!"

if __name__ == '__main__':
    app.run(debug=True)