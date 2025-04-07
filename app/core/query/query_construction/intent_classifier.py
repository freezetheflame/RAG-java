from .base import QueryConstructor
from transformers import pipeline


class IntentClassifier(QueryConstructor):
    def __init__(self, model_name="bert-base-uncased"):
        self.classifier = pipeline("text-classification", model=model_name)

    def build(self, query: str) -> dict:
        intent = self.classifier(query)[0]["label"]
        return {"intent": intent, "original_query": query}