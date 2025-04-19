import asyncio
import os
from typing import AsyncGenerator

from langsmith.wrappers import wrap_openai
from langsmith import traceable


from openai import AsyncOpenAI, OpenAI

from app.config import Settings
from app.services.llm import LLMService

API_URL = 'https://api.hunyuan.cloud.tencent.com/v1'

class hunyuanService(LLMService):
    def __init__(self):
        self.api_key = Settings.HUNYUAN_API_KEY
        self.client = wrap_openai(AsyncOpenAI(api_key=self.api_key,base_url=API_URL))


    def generate(self, prompt: str, **kwargs) -> str:
        # 同步方法调用异步方法
        return asyncio.run(self.agenerate(prompt, **kwargs))

    @traceable
    async def agenerate(self, prompt: str, **kwargs) -> str:
        print("---------llm is generating response--------")
        retrieved_docs = kwargs.get('retrieved_docs')
        # 关于prompt的处理
        if retrieved_docs:
            context = "\n".join([doc["content"] for doc in retrieved_docs])
            prompt = f"""
            根据以下上下文回答问题：
            上下文：
            {context}

            问题：
            {prompt}

            回答：
            """
        response = await self.client.chat.completions.create(
            model = 'hunyuan-lite',
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=kwargs.get('temperature', 0.5)
        )
        return response.choices[0].message.content

    def stream_generate(self, prompt: str, **kwargs):
        """
        流式生成响应，逐步返回每个 token。
        :param prompt: 用户输入的提示
        :param kwargs: 其他参数（如 temperature）
        """
        print("---------llm is streaming response--------")
        retrieved_docs = kwargs.get('retrieved_docs')
        # 关于prompt的处理
        if retrieved_docs:
            context = "\n".join([doc["content"] for doc in retrieved_docs])
            prompt = f"""
            根据以下上下文回答问题：
            上下文：
            {context}

            问题：
            {prompt}

            回答：
            """
        client = wrap_openai(OpenAI(base_url=API_URL,api_key=self.api_key))
        stream = client.chat.completions.create(
            model='hunyuan-lite',
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get('temperature', 0.5),
            stream=True  # 启用流式输出
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                print(f"Yielding chunk: {content}")  # 调试日志
                yield content