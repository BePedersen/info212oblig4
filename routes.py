from flask import Blueprint, Flask, request, jsonify
from models import db

all_routes = Blueprint('all_routes', __name__)

#Car CRUD
@all_routes.route('/create-car', methods=['POST'])
def create_car():
    data = request.get_json()
    db.create_car(data['id'], data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car created successfully'})

@all_routes.route('/create_car/<car_id>', methods=['GET'])
def read_car(car_id):
    car = db.read_car(car_id)
    if car:
        return jsonify(car)
    else:
        return jsonify({'error': 'Car not found'})

@all_routes.route('/create_car/<car_id>', methods=['PUT'])
def update_car(car_id):
    updates = request.get_json()
    db.update_car(car_id, updates)
    return jsonify({'message': f'Car {car_id} updated successfully'})

@all_routes.route('/create_car/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    db.delete_car(car_id)
    return jsonify({'message': f'Car {car_id} deleted successfully'})



#Customer CRUD
@all_routes.route('/create_cust', methods=['POST'])
def create_cust():
    data = request.get_json()
    db.create_customer(data('id', data('name'), data('age'), data('address')))
    return jsonify({'message': 'Customer created successfully'})

@all_routes.route()('/create_cust/', methods=['GET'])
def read_cust(customer_id):
    cust = db.read_customer(customer_id)
    if cust:
        return jsonify(cust)
    else:
        return jsonify({'error': 'Customer not found'})
    
@car_routes.route('/create_cust/<customer_id>', methods=['PUT'])
def update_car(car_id):
    updates = request.get_json()
    db.update_car(car_id, updates)
    return jsonify({'message': f'Car {car_id} updated successfully'})

@car_routes.route('/create_cust/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db.delete_customer(customer_id)
    return jsonify({'message': f'Customer {customer_id} deleted successfully'})




#Employee CRUD
@all_routes.route('/create_employee', methods=['POST'])
def create_employee():
    data = request.get_json()
    db.create_employee(data['id'], data['name'], data['address'], data['branch'])
    return jsonify({'message': 'Employee created successfully'})

@all_routes.route('/read_employee', method=['GET'])
def read_employee(employee_id):
    employee = db.read_employee(employee_id)
    if employee:
        return jsonify(employee)
    else:
        return jsonify({'error': 'Employee not found'})

@all_routes.route('/update_employee', method = ['PUT'])
def update_employee(employee_id):
    data = request.get_json()  
    employee_id = data.get('id')  
    update_result = db.update_employee(employee_id, name=['name'], address=['address'], branch=['branch'])
    
    if update_result:
        return jsonify({'message': 'Employee updated successfully'})
    else:
        return jsonify({'error': 'Employee not found or update failed'})

@all_routes.route('/delete_employee', methods=['DELETE'])
def delete_employee():
    data = request.get_json()  
    employee_id = data.get('id')  
    delete_result = db.delete_employee(employee_id)
    
    if delete_result:
        return jsonify({'message': 'Employee deleted successfully'})
    else:
        return jsonify({'error': 'Employee not found or deletion failed'})


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
