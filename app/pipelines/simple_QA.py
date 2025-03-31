from pymilvus import Collection
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional

class MilvusSearcher:
    def __init__(
            self,
            collection_name: str = "java_interview_qa",
            embedding_model_name: str = "paraphrase-MiniLM-L6-v2",
            host: str = "172.29.4.151",
            port: str = "19530",
            db_name: str = "Java_knowledge_base"
    ):
        """
        初始化Milvus搜索器

        参数:
            collection_name: 集合名称
            embedding_model_name: 嵌入模型名称或路径
            host: Milvus服务器地址
            port: Milvus服务器端口
            db_name: 数据库名称
        """
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model_name

        # 连接设置
        self._connect_to_milvus(host, port, db_name)
        self._load_embedding_model()
        self._load_collection()

    def _connect_to_milvus(self, host: str, port: str, db_name: str):
        """连接到Milvus服务器"""
        try:
            from pymilvus import connections
            connections.connect(
                alias="default",
                host=host,
                port=port,
                db_name=db_name
            )
            print(f"成功连接到Milvus: {host}:{port}/{db_name}")
        except Exception as e:
            print(f"连接Milvus失败: {e}")
            raise

    def _load_embedding_model(self):
        """加载嵌入模型"""
        try:
            self.embedding_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
            print(f"成功加载嵌入模型: {self.embedding_model_name}")
        except Exception as e:
            print(f"加载嵌入模型失败: {e}")
            raise

    def _load_collection(self):
        """加载集合"""
        try:
            self.collection = Collection(self.collection_name)
            self.collection.load()
            print(f"集合 {self.collection_name} 加载成功")
        except Exception as e:
            print(f"加载集合失败: {e}")
            raise

    def vector_search(
            self,
            query_text: str,
            top_k: int = 5,
            output_fields: List[str] = None,
            **filters
    ) -> List[Dict]:
        """
        执行向量相似度搜索

        参数:
            query_text: 查询文本
            top_k: 返回结果数量
            output_fields: 要返回的字段列表
            filters: 过滤条件 (如 category="OOP")

        返回:
            搜索结果列表，包含id、score和请求的字段
        """
        try:
            # 设置默认输出字段
            if output_fields is None:
                output_fields = ["question", "answer", "category", "source", "tags"]

            # 生成查询向量
            query_vector = self.embedding_model.encode([query_text])[0].tolist()

            # 构建过滤表达式
            expr = self._build_filter_expression(**filters)

            # 搜索参数
            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10},
                "expr": expr
            }

            # 执行搜索
            results = self.collection.search(
                data=[query_vector],
                anns_field="question_vector",
                param=search_params,
                limit=top_k,
                output_fields=output_fields,
                consistency_level="Strong"
            )

            # 格式化结果
            formatted_results = []
            for hits in results:
                for hit in hits:
                    result = {
                        "id": hit.id,
                        "score": 1 / (1 + hit.distance),  # 转换为相似度分数(0-1)
                        "distance": hit.distance  # 原始距离
                    }
                    # 添加请求的字段
                    for field in output_fields:
                        result[field] = hit.entity.get(field)
                    formatted_results.append(result)

            return formatted_results
        except Exception as e:
            print(f"向量搜索失败: {e}")
            return []

    def filter_search(
            self,
            output_fields: List[str] = None,
            limit: int = 10,
            offset: int = 0,
            **filters
    ) -> List[Dict]:
        """
        执行属性过滤搜索

        参数:
            output_fields: 要返回的字段列表
            limit: 返回结果数量
            offset: 偏移量(用于分页)
            filters: 过滤条件 (如 category="OOP")

        返回:
            搜索结果列表
        """
        try:
            # 设置默认输出字段
            if output_fields is None:
                output_fields = ["question", "answer", "category", "source", "tags"]

            # 构建过滤表达式
            expr = self._build_filter_expression(**filters)

            # 执行查询
            results = self.collection.query(
                expr=expr,
                output_fields=output_fields,
                limit=limit,
                offset=offset
            )

            return results
        except Exception as e:
            print(f"过滤搜索失败: {e}")
            return []

    def hybrid_search(
            self,
            query_text: str,
            top_k: int = 5,
            min_score: float = 0,
            output_fields: List[str] = None,
            **filters
    ) -> List[Dict]:
        """
        执行混合搜索 (向量搜索 + 属性过滤)

        参数:
            query_text: 查询文本
            top_k: 返回结果数量
            min_score: 最小相似度分数阈值
            output_fields: 要返回的字段列表
            filters: 额外过滤条件

        返回:
            搜索结果列表，按相似度排序
        """
        # 执行向量搜索
        vector_results = self.vector_search(
            query_text=query_text,
            top_k=top_k,
            **filters
        )


        # 过滤低质量结果
        filtered_results = [r for r in vector_results if r["score"] >= min_score]

        # 按分数排序
        filtered_results.sort(key=lambda x: x["score"], reverse=True)

        return filtered_results

    def get_by_id(
            self,
            id: str,
            output_fields: List[str] = None
    ) -> Optional[Dict]:
        """
        根据ID获取单条记录

        参数:
            id: 记录ID
            output_fields: 要返回的字段列表

        返回:
            记录字典或None
        """
        try:
            # 设置默认输出字段
            if output_fields is None:
                output_fields = ["question", "answer", "category", "source", "tags"]

            results = self.collection.query(
                expr=f"id == '{id}'",
                output_fields=output_fields
            )
            return results[0] if results else None
        except Exception as e:
            print(f"按ID查询失败: {e}")
            return None

    def _build_filter_expression(self, **filters) -> str:
        """
        构建过滤表达式

        参数:
            filters: 过滤条件键值对

        返回:
            过滤表达式字符串
        """
        conditions = []

        # 支持的条件字段
        filter_fields = {
            "category": str,
            "source": str,
            "tags": list
        }

        for field, field_type in filter_fields.items():
            if field in filters:
                value = filters[field]

                # 处理字符串条件
                if field_type == str:
                    conditions.append(f"{field} == '{value}'")

                # 处理标签数组条件
                elif field_type == list and isinstance(value, (list, str)):
                    if isinstance(value, str):
                        value = [value]
                    tag_conditions = [f"'{tag}' in tags" for tag in value]
                    conditions.append(f"({' or '.join(tag_conditions)})")

        return " and ".join(conditions) if conditions else ""

    def release(self):
        """释放资源"""
        try:
            if hasattr(self, "collection"):
                self.collection.release()
            from pymilvus import connections
            connections.disconnect("default")
            print("资源已释放")
        except Exception as e:
            print(f"释放资源失败: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


# 示例用法
if __name__ == "__main__":
    # 示例用法
    with MilvusSearcher() as searcher:
        # 向量搜索示例
        print("=== 向量搜索示例 ===")
        vector_results = searcher.vector_search(
            query_text="Java的多态是什么",
            top_k=2,
            output_fields=["question", "answer", "category"]
        )
        for result in vector_results:
            print(f"ID: {result['id']}, 分数: {result['score']:.2f}")
            print(f"问题: {result['question']}")
            print(f"分类: {result['category']}")
            print(f"answer: {result['answer']}")
            print("-----")

        # 过滤搜索示例
        print("\n=== 过滤搜索示例 ===")
        filter_results = searcher.filter_search(
            category="OOP",
            limit=3,
            output_fields=["question", "category", "answer"]
        )
        for result in filter_results:
            print(f"问题: {result['question']}")
            print(f"分类: {result['category']}")
            print(f"answer: {result['answer']}")
            print("-----")

        # 混合搜索示例
        print("\n=== 混合搜索示例 ===")
        hybrid_results = searcher.hybrid_search(
            query_text="垃圾回收",
            category="JVM",
            min_score=0,
            output_fields=["question", "answer", "score"]
        )
        for result in hybrid_results:
            print(f"分数: {result['score']:.2f}")
            print(f"问题: {result['question']}")
            print(f"答案摘要: {result['answer'][:50]}...")
            print("-----")