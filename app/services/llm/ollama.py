import asyncio
import os

from openai import AsyncOpenAI
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from app.config import Settings
from app.services.llm import LLMService

API_URL = 'http://localhost:11434/v1'

class OllamaService(LLMService):
    def __init__(self):
        self.api_key = "ollama"
        self.client = AsyncOpenAI(api_key=self.api_key,base_url=API_URL)

    def generate(self, prompt: str, **kwargs) -> str:
        # 同步方法调用异步方法
        return asyncio.run(self.agenerate(prompt, **kwargs))

    @traceable
    async def agenerate(self, prompt: str, **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model = 'llama3.1:latest',
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=kwargs.get('temperature', 0.5)
        )
        return response.choices[0].message.content