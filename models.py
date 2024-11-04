from neo4j import GraphDatabase

class CarRentalDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Car CRUD
    def create_car(self, reg_nr, make, model, year, location, status):
        with self.driver.session() as session:
            session.run("CREATE (c:Car {reg_nr: $reg_nr, make: $make, model: $model, year: $year, location: $location ,status: $status})",
                    reg_nr=reg_nr, make=make, model=model, year=year, location=location, status=status)

    def read_car(self, reg_nr):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Car {reg_nr: $reg_nr}) RETURN c", reg_nr=reg_nr)
            record = result.single() 
        if record:
            car_node = record["c"] 
            return dict(car_node)  
        else:
            return None  

    def update_car(self, reg_nr, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Car {reg_nr: $reg_nr}) SET c += $updates RETURN c",
                reg_nr=reg_nr, updates=updates
            )

    def delete_car(self, reg_nr):
        with self.driver.session() as session:
            session.run("MATCH (c:Car {reg_nr: $reg_nr}) DELETE c", reg_nr=reg_nr)

    # Customer CRUD
    def create_customer(self, customer_id, name, age, address):
        with self.driver.session() as session:
            session.run(
                "CREATE (cust:Customer {customer_id: $customer_id, name: $name, age: $age, address: $address})",
                customer_id=customer_id, name=name, age=age, address=address
            )

    def read_customer(self, customer_id):
        with self.driver.session() as session:
            result = session.run("MATCH (cust:Customer {customer_id: $customer_id}) RETURN cust", customer_id=customer_id)
            record = result.single()  
        if record:
            customer_node = record["cust"]  
            return dict(customer_node)  
        else:
            return None  

    def update_customer(self, customer_id, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (cust:Customer {customer_id: $customer_id}) SET cust += $updates RETURN cust",
                customer_id=customer_id, updates=updates
            )

    def delete_customer(self, customer_id):
        with self.driver.session() as session:
            session.run("MATCH (cust:Customer {customer_id: $customer_id}) DELETE cust", customer_id=customer_id)

    # Employee CRUD
    def create_employee(self, employee_id, name, address, branch):
        with self.driver.session() as session:
            session.run(
                "CREATE (e:Employee {employee_id: $employee_id, name: $name, address: $address, branch: $branch})",
                employee_id=employee_id, name=name, address=address, branch=branch
            )

    def read_employee(self, employee_id):
        with self.driver.session() as session:
            result = session.run("MATCH (e:Employee {employee_id: $employee_id}) RETURN e", employee_id=employee_id)
            record = result.single()  
        if record:
            employee_node = record["e"] 
            return dict(employee_node)  
        else:
            return None  

    def update_employee(self, employee_id, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (e:Employee {employee_id: $employee_id}) SET e += $updates RETURN e",
                employee_id=employee_id, updates=updates
            )

    def delete_employee(self, employee_id):
        with self.driver.session() as session:
            session.run("MATCH (e:Employee {employee_id: $employee_id}) DELETE e", employee_id=employee_id)

    # Car rental actions
    def order_car(self, customer_id, reg_nr):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (c:Car {reg_nr: $reg_nr, status: 'available'}), (cust:Customer {customer_id: $customer_id})
                WHERE NOT (cust)-[:BOOKED]->(:Car)
                SET c.status = 'booked'
                CREATE (cust)-[:BOOKED]->(c)
                RETURN c, cust
                """,
                reg_nr=reg_nr, customer_id=customer_id
            )

            # Check if the query returned a result 
            record = result.single()
            if record:
                return {"message": "Car booked successfully"}
            else:
                return {"error": "Booking failed. Either the car is not available or the customer already has a booking."}

    def cancel_order(self, customer_id, reg_nr):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (cust:Customer {customer_id: $customer_id})-[r:BOOKED]->(c:Car {reg_nr: $reg_nr, status: 'booked'})
                SET c.status = 'available'
                DELETE r
                RETURN c, cust
                """,
                reg_nr=reg_nr, customer_id=customer_id
            )

            # Check if the cancellation was successful
            record = result.single()
            if record:
                return {"message": "Order cancelled successfully"}
            else:
                return {"error": "Cancellation failed. Either the car is not booked or the customer did not book this car."}

    def rent_car(self, customer_id, reg_nr):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (cust:Customer {customer_id: $customer_id})-[r:BOOKED]->(c:Car {reg_nr: $reg_nr, status: 'booked'})
                SET c.status = 'rented'
                DELETE r
                CREATE (cust)-[:RENTED]->(c)
                RETURN c, cust
                """,
                reg_nr=reg_nr, customer_id=customer_id
            )

            # Check if the query returned a result 
            record = result.single()
            if record:
                return {"message": "Car rented successfully"}
            else:
                return {"error": "Renting failed. Either the car is not booked or the customer did not book this car."}

    def return_car(self, customer_id, reg_nr, condition):
        with self.driver.session() as session:
            # Set the car status based on the condition
            status = 'available' if condition == 'ok' else 'damaged'
            result = session.run(
                """
                MATCH (cust:Customer {customer_id: $customer_id})-[r:RENTED]->(c:Car {reg_nr: $reg_nr, status: 'rented'})
                SET c.status = $status
                DELETE r
                RETURN c
                """,
                reg_nr=reg_nr, customer_id=customer_id, status=status
            )

            # Check if the query returned a result 
            record = result.single()
            if record:
                return {"message": "Car returned successfully", "status": status}
            else:
                return {"error": "Return failed. Either the car is not rented or the customer did not rent this car."}


db = CarRentalDB("neo4j://localhost:7687", 'Cars', 'passord!')
