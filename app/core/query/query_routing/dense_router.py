from .base import Router
from faiss import IndexFlatL2


class DenseRetrievalRouter(Router):
    def __init__(self, index: IndexFlatL2):
        self.index = index

    def route(self, query: dict) -> str:
        # 基于向量相似度的路由逻辑
        return "dense_retrieval"