from sentence_transformers import SentenceTransformer
from pymilvus import Collection, connections
from typing import List, Dict, Any
import configparser


class MilvusEmbeddingProcessor:
    def __init__(self,
                 collection_name: str = "java_interview_qa",
                 embedding_model_name: str = 'paraphrase-MiniLM-L6-v2'):
        cfp = configparser.ConfigParser()
        cfp.read("../config/milvus_config.ini")
        self.milvus_uri = cfp.get('milvus', 'uri')
        self.token = cfp.get('milvus', 'token')
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model_name

        # 连接Milvus
        self._connect_to_milvus()

        # 加载嵌入模型
        self.embedding_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

    def _connect_to_milvus(self):
        """连接到Milvus服务器"""
        try:
            connections.connect(
                uri=self.milvus_uri,
                token=self.token
            )
        except Exception as e:
            print(f"连接Milvus失败: {e}")
            raise

    def _prepare_entities(self, data: List[Dict[str, Any]]) -> List[List]:
        """
        准备要插入的实体数据

        参数:
            data: 包含问题和相关数据的字典列表

        返回:
            准备好的实体列表
        """
        entities = [
            # id会自动生成
            [item["question"] for item in data],  # question
            [item["answer"] for item in data],  # answer
            [item["question_vector"] for item in data],  # question_vector
            [item["category"] for item in data],  # category
            [item["source"] for item in data],  # source
            [item["tags"] for item in data]  # tags
        ]
        return entities

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        为文本列表生成嵌入向量

        参数:
            texts: 要嵌入的文本列表

        返回:
            嵌入向量列表
        """
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            print(f"生成嵌入失败: {e}")
            raise

    def prepare_data(self, questions: List[str], answers: List[str],
                     categories: List[str], sources: List[str],
                     tags_list: List[List[str]]) -> List[Dict[str, Any]]:
        """
        准备数据并生成嵌入向量

        参数:
            questions: 问题列表
            answers: 对应答案列表
            categories: 分类列表
            sources: 来源列表
            tags_list: 标签列表(每个元素是一个标签列表)

        返回:
            准备好的数据字典列表
        """
        if not (len(questions) == len(answers) == len(categories) == len(sources) == len(tags_list)):
            raise ValueError("所有输入列表的长度必须相同")

        # 生成问题嵌入
        question_vectors = self.generate_embeddings(questions)

        # 准备数据
        data = []
        for i in range(len(questions)):
            data.append({
                "question": questions[i],
                "answer": answers[i],
                "category": categories[i],
                "source": sources[i],
                "tags": tags_list[i],
                "question_vector": question_vectors[i]
            })

        print(f"已准备 {len(data)} 条数据")
        return data

    def insert_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        将数据插入到Milvus集合

        参数:
            data: 准备的数据字典列表

        返回:
            插入是否成功
        """
        try:
            collection = Collection(self.collection_name)
            entities = self._prepare_entities(data)

            # 插入数据
            mr = collection.insert(entities)

            # 刷新集合使新数据可搜索
            collection.flush()

            print(f"成功插入 {len(data)} 条数据到集合 {self.collection_name}")
            return True
        except Exception as e:
            print(f"插入数据失败: {e}")
            return False

    def batch_insert(self, questions: List[str], answers: List[str],
                     categories: List[str], sources: List[str],
                     tags_list: List[List[str]], batch_size: int = 100) -> bool:
        """
        批量准备并插入数据

        参数:
            questions: 问题列表
            answers: 对应答案列表
            categories: 分类列表
            sources: 来源列表
            tags_list: 标签列表(每个元素是一个标签列表)
            batch_size: 每批大小

        返回:
            操作是否成功
        """
        try:
            total = len(questions)
            for i in range(0, total, batch_size):
                # 获取当前批次数据
                batch_questions = questions[i:i + batch_size]
                batch_answers = answers[i:i + batch_size]
                batch_categories = categories[i:i + batch_size]
                batch_sources = sources[i:i + batch_size]
                batch_tags = tags_list[i:i + batch_size]

                # 准备并插入数据
                data = self.prepare_data(
                    batch_questions, batch_answers,
                    batch_categories, batch_sources, batch_tags
                )
                self.insert_data(data)

                print(f"已处理 {min(i + batch_size, total)}/{total} 条数据")

            return True
        except Exception as e:
            print(f"批量插入失败: {e}")
            return False

    def close(self):
        """关闭连接"""
        connections.disconnect("default")
        print("Milvus连接已关闭")


# 示例用法
if __name__ == "__main__":

    # 示例数据
    sample_questions = [
        "什么是Java中的多态性？",
        "解释一下Java的垃圾回收机制",
        "ArrayList和LinkedList有什么区别？"
    ]
    sample_answers = [
        "多态性是面向对象编程的一个重要特性，它允许使用统一的接口操作不同的对象...",
        "Java的垃圾回收机制是自动内存管理的一部分，JVM会自动回收不再使用的对象...",
        "ArrayList是基于动态数组实现的，而LinkedList是基于双向链表实现的..."
    ]
    sample_categories = ["OOP", "JVM", "集合"]
    sample_sources = ["Java核心技术", "Java编程思想", "Effective Java"]
    sample_tags = [
        ["面向对象", "基础"],
        ["内存管理", "性能"],
        ["数据结构", "集合框架"]
    ]

    # 创建处理器实例
    processor = MilvusEmbeddingProcessor()

    try:
        # 方法1: 单独准备数据并插入
        prepared_data = processor.prepare_data(
            sample_questions, sample_answers,
            sample_categories, sample_sources, sample_tags
        )
        processor.insert_data(prepared_data)

        # 方法2: 直接批量处理(适合大数据量)
        # processor.batch_insert(
        #     sample_questions, sample_answers,
        #     sample_categories, sample_sources, sample_tags,
        #     batch_size=2
        # )
    finally:
        # 关闭连接
        processor.close()