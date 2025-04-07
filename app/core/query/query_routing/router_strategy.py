from .base import Router
from .dense_router import DenseRetrievalRouter
from .bm25_router import BM25Router


class RouterStrategy:
    def __init__(self):
        self.routers = {
            "technical": DenseRetrievalRouter,
            "general": BM25Router
        }

    def select_router(self, intent: str) -> Router:
        return self.routers.get(intent, BM25Router)()