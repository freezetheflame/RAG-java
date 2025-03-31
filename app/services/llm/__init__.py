'''
services/llm/__init__.py
进行抽象接口的定义
'''
# app/services/llm/__init__.py
from abc import ABC, abstractmethod
# from typing import Dict, Any

class LLMService(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def agenerate(self, prompt: str, **kwargs) -> str:
        pass