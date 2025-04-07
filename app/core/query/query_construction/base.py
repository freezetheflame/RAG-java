from abc import ABC, abstractmethod

class QueryConstructor(ABC):
    @abstractmethod
    def build(self, query: str) -> dict:
        """构建增强后的查询结构"""
        pass