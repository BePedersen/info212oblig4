from flask import Blueprint, Flask, request, jsonify
from models import db

all_routes = Blueprint('all_routes', __name__)

#Car CRUD
@all_routes.route('/create-car', methods=['POST'])
def create_car():
    data = request.get_json()
    db.create_car(data['id'], data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car created successfully'})

#Customer CRUD

#Employee CRUD

#Car rental functions
@all_routes.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    db.order_car(data['customer_id'], data['car_id'])
    return jsonify({'message': 'Car ordered successfully'})

@all_routes.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.get_json()
    db.cancel_order(data['customer_id'], data['car_id'])
    return jsonify({'message': 'Order cancelled successfully'})

@all_routes.route('/rent-car', methods=['POST'])
def rent_car():
    data = request.get_json()
    db.rent_car(data['customer_id'], data['car_id'])
    return jsonify({'message': 'Car rented successfully'})

@all_routes.route('/return-car', methods=['POST'])
def return_car():
    data = request.get_json()
    db.return_car(data['customer_id'], data['car_id'], data['condition'])
    return jsonify({'message': 'Car returned successfully'})
