import os

from app.services.llm import LLMService
from app.services.llm.deepseek import deepseekService
from app.services.llm.hunyuan import hunyuanService
from app.services.llm.ollama import OllamaService

LLM_PROVIDERS = {
    "deepseek": deepseekService,
    "ollama": OllamaService,
    "hunyuan": hunyuanService

}

def get_llm_service(provider:str) -> LLMService:
    if provider not in LLM_PROVIDERS:
        raise ValueError(f"Invalid provider: {provider}")
    return LLM_PROVIDERS[provider]()