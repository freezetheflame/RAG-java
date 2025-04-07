from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    def translate(self, query: str, target_lang: str) -> str:
        pass