from neo4j import GraphDatabase

class CarRentalDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Car CRUD
    def create_car(self, car_id, make, model, year, location, status):
        with self.driver.session() as session:
            session.run("CREATE (c:Car {id: $car_id, make: $make, model: $model, year: $year, location: $location ,status: $status})",
                    car_id=car_id, make=make, model=model, year=year, location=location, status=status)

    def read_car(self, car_id):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Car {id: $car_id}) RETURN c", car_id=car_id)
            return result.single()

    def update_car(self, car_id, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Car {id: $car_id}) SET c += $updates RETURN c",
                car_id=car_id, updates=updates
            )

    def delete_car(self, car_id):
        with self.driver.session() as session:
            session.run("MATCH (c:Car {id: $car_id}) DELETE c", car_id=car_id)

    # Customer CRUD
    def create_customer(self, customer_id, name, age, address):
        with self.driver.session() as session:
            session.run(
                "CREATE (cust:Customer {id: $customer_id, name: $name, age: $age, address: $address})",
                customer_id=customer_id, name=name, age=age, address=address
            )

    def read_customer(self, customer_id):
        with self.driver.session() as session:
            result = session.run("MATCH (cust:Customer {id: $customer_id}) RETURN cust", customer_id=customer_id)
            return result.single()

    def update_customer(self, customer_id, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (cust:Customer {id: $customer_id}) SET cust += $updates RETURN cust",
                customer_id=customer_id, updates=updates
            )

    def delete_customer(self, customer_id):
        with self.driver.session() as session:
            session.run("MATCH (cust:Customer {id: $customer_id}) DELETE cust", customer_id=customer_id)

    # Employee CRUD
    def create_employee(self, employee_id, name, address, branch):
        with self.driver.session() as session:
            session.run(
                "CREATE (e:Employee {id: $employee_id, name: $name, address: $address, branch: $branch})",
                employee_id=employee_id, name=name, address=address, branch=branch
            )

    def read_employee(self, employee_id):
        with self.driver.session() as session:
            result = session.run("MATCH (e:Employee {id: $employee_id}) RETURN e", employee_id=employee_id)
            return result.single()

    def update_employee(self, employee_id, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (e:Employee {id: $employee_id}) SET e += $updates RETURN e",
                employee_id=employee_id, updates=updates
            )

    def delete_employee(self, employee_id):
        with self.driver.session() as session:
            session.run("MATCH (e:Employee {id: $employee_id}) DELETE e", employee_id=employee_id)

    # Car rental actions
    def order_car(self, customer_id, car_id):
        with self.driver.session() as session:
            # Ensure car is available and customer has no other bookings
            session.run(
                "MATCH (c:Car {id: $car_id, status: 'available'}), (cust:Customer {id: $customer_id}) "
                "SET c.status = 'booked' "
                "RETURN c, cust",
                car_id=car_id, customer_id=customer_id
            )

    def cancel_order(self, customer_id, car_id):
        with self.driver.session() as session:
            # Ensure the car is booked by the customer, then make it available
            session.run(
                "MATCH (c:Car {id: $car_id, status: 'booked'}), (cust:Customer {id: $customer_id}) "
                "SET c.status = 'available' "
                "RETURN c",
                car_id=car_id, customer_id=customer_id
            )

    def rent_car(self, customer_id, car_id):
        with self.driver.session() as session:
            # Ensure the car is booked by the customer, then rent it out
            session.run(
                "MATCH (c:Car {id: $car_id, status: 'booked'}), (cust:Customer {id: $customer_id}) "
                "SET c.status = 'rented' "
                "RETURN c",
                car_id=car_id, customer_id=customer_id
            )

    def return_car(self, customer_id, car_id, condition):
        with self.driver.session() as session:
            # Ensure the car is rented by the customer, then set its status based on the condition
            status = 'available' if condition == 'ok' else 'damaged'
            session.run(
                "MATCH (c:Car {id: $car_id, status: 'rented'}), (cust:Customer {id: $customer_id}) "
                "SET c.status = $status "
                "RETURN c",
                car_id=car_id, customer_id=customer_id, status=status
            )



db = CarRentalDB("neo4j://localhost:7687", 'Cars', 'passord!')
