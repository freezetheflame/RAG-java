from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import configparser


class MilvusDBInitializer:

    def __init__(self):
        cfp = configparser.ConfigParser()
        cfp.read("../config/milvus_config.ini")
        self.milvus_uri = cfp.get("milvus", "uri")
        self.token = cfp.get("milvus", "token")
        self.collection_name = "java_interview_qa"  # 默认集合名称
        self.dim = 384  # 与嵌入模型维度匹配
        self.connect()

    def connect(self):
        """连接到 Milvus 服务器"""
        try:
            connections.connect(uri=self.milvus_uri, token=self.token)
            print(f"Connected to Milvus at {self.milvus_uri}")
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")

    def create_collection(self):

        """创建集合（如果存在则先删除）"""
        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)

        # 定义字段结构
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=64),  # 主键ID
            FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=1024),  # 问题描述
            FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=4096),  # 数据来源
            FieldSchema(name="question_vector", dtype=DataType.FLOAT_VECTOR, dim=self.dim),  # 匹配嵌入模型维度
            FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=64),  # 问题分类
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=1024),  # 数据来源
            FieldSchema(name="tags", dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=10,
                        max_length=32)  # 标签
        ]

        # 创建集合模式
        schema = CollectionSchema(fields, description="Java面试问答集合")
        collection = Collection(self.collection_name, schema)

        # 创建索引
        index_params = {
            "metric_type": "L2",  # 使用L2距离
            "index_type": "IVF_FLAT",  # 使用倒排文件索引
            "params": {"nlist": 128}  # 聚类中心数量
        }
        collection.create_index("question_vector", index_params)

        print(f"Collection {self.collection_name} created with index")

        return collection

    def close(self):
        """关闭连接"""
        connections.disconnect("default")
        print("ℹ️ Milvus连接已关闭")


if __name__ == '__main__':
    db_initializer = MilvusDBInitializer()
    try:
        db_initializer.create_collection()
        print("Collection created")
    finally:
        db_initializer.close()