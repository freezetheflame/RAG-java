from abc import ABC, abstractmethod

class Router(ABC):
    @abstractmethod
    def route(self, query: dict) -> str:
        """根据查询意图选择检索策略"""
        pass