from flask import Flask, request, jsonify
from models import db
@app.route('/create-car', methods=['POST'])
def create_car():
    data = request.json
    db.create_car(data['id'], data['make'], data['model'], data['year'], 'available')
    return jsonify({'message': 'Car created successfully'})

@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    # Implement logic to check if customer has no other booking and update status
    return jsonify({'message': 'Car ordered successfully'})

