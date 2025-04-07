from .base import QueryConstructor
from .intent_classifier import IntentClassifier
from .entity_expander import EntityExpander

class QueryFactory:
    @staticmethod
    def get_constructor(strategy: str) -> QueryConstructor:
        if strategy == "intent":
            return IntentClassifier()
        elif strategy == "entity":
            return EntityExpander()
        # 可扩展其他策略
        else:
            raise ValueError("Unknown strategy")