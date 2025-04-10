from flask import current_app

from app.api.dependency import get_llm_service_dependency
from app.services.llm import LLMService
from app.utils.tokenizer import Tokenizer


class RAGService:
    def __init__(self,LLMrequire:str = 'deepseek'):
        self.tokenizer = Tokenizer()
        self.milvus_client = current_app.extensions['milvus']  # 获取 Milvus 客户端
        self.LLMService = LLMrequire
        self.llm_service = get_llm_service_dependency(LLMrequire)  # 初始化 LLM 服务

    def retrieve(self, query: str, top_k=5):
        # 1. 文本向量化
        query_vector = self.tokenizer.encode(query)

        # 2. 在 Milvus 中检索
        results = self.milvus_client.search(query_vector=query_vector, top_k=top_k)
        print("----------retrieve results:",results)
        # 3. 解析结果
        retrieved_docs = []
        for hit in results[0]:
            retrieved_docs.append({
                "id": hit.id,
                "score": hit.score,
                "question": hit.entity.get("question"),
                "answer": hit.entity.get("answer"),
            })
        return retrieved_docs

    async def generate_answer(self, query: str, retrieved_docs: list):
        # 1. 拼接检索到的文档片段
        context = "\n".join([doc["question"] + "\n" + doc["answer"] for doc in retrieved_docs])

        # 2. 构造提示
        prompt = f"""
        根据以下上下文回答问题：
        上下文：
        {context}

        问题：
        {query}

        回答：
        """

        # 3. 使用 LLM 生成答案
        answer = await self.llm_service.agenerate(prompt)
        return answer

    async def query(self, query: str, top_k=5):
        # 1. 检索相关文档
        retrieved_docs = self.retrieve(query, top_k=top_k)

        # 2. 生成答案
        answer = await self.generate_answer(query, retrieved_docs)

        return {
            "answer": answer,
            "retrieved_docs": retrieved_docs
        }