from neo4j import GraphDatabase

class CarRentalDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    
    def create_car(self, car_id, make, model, year, status):
        with self.driver.session() as session:
            session.run("CREATE (c:Car {id: $car_id, make: $make, model: $model, year: $year, status: $status})",
                    car_id=car_id, make=make, model=model, year=year, status=status)

    def read_car(self, car_id):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Car {id: $car_id}) RETURN c", car_id=car_id)
        return result.single()


db = CarRentalDB("neo4j://localhost:7687", "neo4j", "your_password")


