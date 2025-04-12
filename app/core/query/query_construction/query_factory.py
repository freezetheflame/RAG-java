from .base import QueryConstructor
from .intent_classifier import IntentClassifier
from .entity_expander import EntityExpander, load_synonyms


class QueryFactory:
    @staticmethod
    def get_constructor(strategy: str) -> QueryConstructor:
        if strategy == "intent":
            return IntentClassifier()
        elif strategy == "entity":
            return EntityExpander(load_synonyms("app/core/query/query_construction/java_synonyms.txt"))
        # 可扩展其他策略
        else:
            raise ValueError("Unknown strategy")