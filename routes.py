from flask import Flask, request, jsonify
from models import db

routes = Blueprint('app', __name__)

@app.route('/create-car', methods=['POST'])
def create_car():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Print the data to confirm it was received correctly
        print("Data received:", data)

        # Attempt to create a car in the database
        db.create_car(data['id'], data['make'], data['model'], data['year'], 'available')
        return jsonify({'message': 'Car created successfully'})
    except Exception as e:
        # Print the error to the console for debugging
        print("Error in create_car:", e)
        return jsonify({"error": "Failed to create car", "details": str(e)}), 500
"""def create_car():
    data = request.get_json()
    db.create_car(data['id'], data['make'], data['model'], data['year'], 'available')
    return jsonify({'message': 'Car created successfully'})"""

@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    # Implement logic to check if customer has no other booking and update status
    return jsonify({'message': 'Car ordered successfully'})

@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        db.create_car("test_id", "TestMake", "TestModel", "2021", "available")
        return jsonify({"message": "Test car created successfully"})
    except Exception as e:
        print("Error in test_db:", e)
        return jsonify({"error": str(e)}), 500