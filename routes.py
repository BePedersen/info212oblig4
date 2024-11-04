from flask import Blueprint, request, jsonify
from models import db

all_routes = Blueprint('all_routes', __name__)

# Car CRUD
@all_routes.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    db.create_car(data['reg_nr'], data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car created successfully'})

@all_routes.route('/cars/<reg_nr>', methods=['GET'])
def read_car(reg_nr):
    car = db.read_car(reg_nr)
    if car:
        return jsonify(car)  
    else:
        return jsonify({'error': 'Car not found'})
    
@all_routes.route('/cars/<reg_nr>', methods=['PUT'])
def update_car(reg_nr):
    updates = request.get_json()
    db.update_car(reg_nr, updates)
    return jsonify({'message': f'Car {reg_nr} updated successfully'})

@all_routes.route('/cars/<reg_nr>', methods=['DELETE'])
def delete_car(reg_nr):
    db.delete_car(reg_nr)
    return jsonify({'message': f'Car {reg_nr} deleted successfully'})

# Customer CRUD
@all_routes.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    db.create_customer(data['id'], data['name'], data['age'], data['address'])
    return jsonify({'message': 'Customer created successfully'})

@all_routes.route('/customers/<customer_id>', methods=['GET'])
def read_customer(customer_id):
    customer = db.read_customer(customer_id)
    if customer:
        return jsonify(customer)  
    else:
        return jsonify({'error': 'Customer not found'})
    
@all_routes.route('/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    updates = request.get_json()
    db.update_customer(customer_id, updates)
    return jsonify({'message': f'Customer {customer_id} updated successfully'})

@all_routes.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db.delete_customer(customer_id)
    return jsonify({'message': f'Customer {customer_id} deleted successfully'})

# Employee CRUD
@all_routes.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    db.create_employee(data['id'], data['name'], data['address'], data['branch'])
    return jsonify({'message': 'Employee created successfully'})

@all_routes.route('/employees/<employee_id>', methods=['GET'])
def read_employee(employee_id):
    employee = db.read_employee(employee_id)
    if employee:
        return jsonify(employee)  
    else:
        return jsonify({'error': 'Employee not found'})
    
@all_routes.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    updates = request.get_json()
    db.update_employee(employee_id, updates)
    return jsonify({'message': f'Employee {employee_id} updated successfully'})

@all_routes.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    db.delete_employee(employee_id)
    return jsonify({'message': f'Employee {employee_id} deleted successfully'})

# Car rental functions
@all_routes.route('/order_car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    reg_nr = data.get('reg_nr')

    
    response = db.order_car(customer_id, reg_nr)
    
   
    if "message" in response:
        return jsonify(response)  # Success
    else:
        return jsonify(response)  # Error


@all_routes.route('/cancel_order_car', methods=['POST'])
def cancel_order_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    reg_nr = data.get('reg_nr')

    
    response = db.cancel_order(customer_id, reg_nr)
    
    if "message" in response:
        return jsonify(response)  # Success
    else:
        return jsonify(response)  # Error

@all_routes.route('/rent_car', methods=['POST'])
def rent_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    reg_nr = data.get('reg_nr')

    
    response = db.rent_car(customer_id, reg_nr)
    
    if "message" in response:
        return jsonify(response)  # Success
    else:
        return jsonify(response)  # Error

@all_routes.route('/return_car', methods=['POST'])
def return_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    reg_nr = data.get('reg_nr')
    condition = data.get('condition')

    if not customer_id or not reg_nr or not condition:
        return jsonify({"error": "Missing customer_id, reg_nr, or condition"})

    response = db.return_car(customer_id, reg_nr, condition)
    
    if "message" in response:
        return jsonify(response)   # Success
    else:
        return jsonify(response)  # Error