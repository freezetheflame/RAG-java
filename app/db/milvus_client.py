from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

from app.config import Settings


class MilvusClient:
    def __init__(self, port: str = '19530'):
        self.host = Settings.MILVUS_HOST # Milvus 服务器地址
        self.port = port  # Milvus 服务器端口
        self.db_name = 'Java_knowledge_base'
        self.collection_name = "java_interview_qa"  # 默认集合名称
        self.dim = 384  # 与嵌入模型维度匹配
        self.connect()

    def connect(self):
        """连接到 Milvus 服务器"""
        try:
            connections.connect(alias="default",host=self.host, port=self.port, db_name=self.db_name)
            self.collection = Collection(self.collection_name)
            self.collection.load()
            print(f"Connected to Milvus at {self.host}:{self.port}:{self.db_name}")
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")


    def close(self):
        """关闭连接"""
        connections.disconnect("default")
        print("ℹ️ Milvus连接已关闭")

    def search(self, query_vector, top_k=5):
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        print(f"query_vector: {query_vector}")
        results = self.collection.search(
            data=[query_vector],
            anns_field="question_vector",
            param=search_params,
            limit=top_k,
            output_fields=["question", "answer"]
        )
        return results
