from neo4j import GraphDatabase

from app.config import Settings

# TODO: extend the use of neo4j
# blame: CHY
class Neo4jClient:
    def __init__(self):
        self.uri = Settings.NEO4J_URI
        self.user = Settings.NEO4J_USERNAME
        self.password =Settings.NEO4J_PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def connect(self, _app=None):
        try:
            self.driver.verify_connectivity()
            print(f"Neo4j connection successful")
            _app.extensions['neo4j'] = self  # Store in Flask app extensions
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")


    def close(self):
        self.driver.close()


def main():
    neo4j_client = Neo4jClient()
    print("Neo4j client initialized.")
    neo4j_client.driver.verify_connectivity()

neo4j_client = Neo4jClient()

if __name__ == "__main__":
    main()