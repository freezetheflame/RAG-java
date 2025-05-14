from app.db.neo4j_client import Neo4jClient
from typing import Dict, List

# TODO: extend the use of neo4j
# blame: CHY
class GraphDemo:
    def __init__(self):
        self.neo4j_client = Neo4jClient()

    def create_node(self, label: str, properties: Dict):
        with self.neo4j_client.driver.session() as session:
            query = (
                f"CREATE (n:{label} $properties) "
                "RETURN n"
            )
            result = session.run(query, properties=properties)
            return result.single()

    def create_relationship(self, source_id: int, target_id: int, relationship_type: str, properties: Dict = None):
        if properties is None:
            properties = {}
        
        with self.neo4j_client.driver.session() as session:
            query = (
                "MATCH (source) WHERE ID(source) = $source_id "
                "MATCH (target) WHERE ID(target) = $target_id "
                f"CREATE (source)-[r:{relationship_type} $properties]->(target) "
                "RETURN r"
            )
            result = session.run(query, 
                               source_id=source_id, 
                               target_id=target_id, 
                               properties=properties)
            return result.single()

    def demo_knowledge_graph(self):
        # Create some example nodes
        java = self.create_node("Technology", {"name": "Java", "type": "Programming Language"})
        spring = self.create_node("Framework", {"name": "Spring", "type": "Web Framework"})
        hibernate = self.create_node("Framework", {"name": "Hibernate", "type": "ORM Framework"})

        # Create relationships
        self.create_relationship(
            spring['n'].id, 
            java['n'].id, 
            "RUNS_ON",
            {"since": "2002"}
        )
        self.create_relationship(
            hibernate['n'].id,
            java['n'].id,
            "DEPENDS_ON",
            {"version_compatibility": "Java 8+"}
        )

    def query_graph(self, query: str, parameters: Dict = None):
        if parameters is None:
            parameters = {}
            
        with self.neo4j_client.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

def main():
    demo = GraphDemo()
    
    # Create a sample knowledge graph
    print("Creating sample knowledge graph...")
    demo.demo_knowledge_graph()
    
    # Query to verify the created data
    print("\nQuerying created nodes and relationships:")
    query = (
        "MATCH (n)-[r]->(m) "
        "RETURN n.name as source, type(r) as relationship, m.name as target"
    )
    results = demo.query_graph(query)
    
    for record in results:
        print(f"{record['source']} --[{record['relationship']}]--> {record['target']}")

if __name__ == "__main__":
    main()