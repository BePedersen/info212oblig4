from flask import Flask, request, jsonify
from models import db
from routes import car_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Register the blueprint
app.register_blueprint(car_routes, url_prefix='/')

@app.route('/')
def home():
    return "Welcome to Car Rental API!"

if __name__ == '__main__':
    app.run(debug=True)