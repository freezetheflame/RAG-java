import asyncio
import os

from openai import AsyncOpenAI

from app.config import Settings
from app.services.llm import LLMService

API_URL = 'https://api.hunyuan.cloud.tencent.com/v1'

class hunyuanService(LLMService):
    def __init__(self):
        self.api_key = Settings.HUNYUAN_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key,base_url=API_URL)

    def generate(self, prompt: str, **kwargs) -> str:
        # 同步方法调用异步方法
        return asyncio.run(self.agenerate(prompt, **kwargs))

    async def agenerate(self, prompt: str, **kwargs) -> str:
        print("---------llm is generating response--------")
        response = await self.client.chat.completions.create(
            model = 'hunyuan-lite',
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=kwargs.get('temperature', 0.5)
        )
        return response.choices[0].message.content