from app.core.query.query_routing.base import Router


class BM25Router(Router):
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def route(self, query: dict) -> str:
        """
        根据查询意图选择检索策略
        :param query: 查询意图
        :return: 检索策略名称
        """
        if query.get("bm25_score", 0) > self.threshold:
            return "BM25"
        else:
            return "default"