from flask import Flask, request, jsonify
from models import db
from routes import all_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Register the blueprint
app.register_blueprint(all_routes, url_prefix='/')

@app.route('/')
def home():
    return "Welcome to Car Rental API!"

if __name__ == '__main__':
    app.run(debug=True)