import asyncio
import os

from openai import AsyncOpenAI

from app.config import Settings
from app.services.llm import LLMService
from langsmith.wrappers import wrap_openai
from langsmith import traceable

API_URL = 'https://api.deepseek.com/v1'

class DeepseekService(LLMService):
    def __init__(self):
        self.api_key = Settings.DEEPSEEK_API_KEY
        self.client = wrap_openai(AsyncOpenAI(api_key=self.api_key,base_url=API_URL))

    def generate(self, prompt: str, **kwargs) -> str:
        # 同步方法调用异步方法
        return asyncio.run(self.agenerate(prompt, **kwargs))

    @traceable
    async def agenerate(self, prompt: str, **kwargs) -> str:
        print("---------llm is generating response--------")
        # 关于prompt的处理
        response = await self.client.chat.completions.create(
            model = 'deepseek-chat',
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=kwargs.get('temperature', 0.5)
        )
        return response.choices[0].message.content