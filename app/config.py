from pathlib import Path

from decouple import Config, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent

# 加载 .env 文件
env_path = BASE_DIR / ".env"
config = Config(RepositoryEnv(env_path))


class Settings:
    DEEPSEEK_API_KEY = config('DEEPSEEK_API_KEY')
    MILVUS_HOST = config('MILVUS_HOST')
    MILVUS_URL = config('MILVUS_URL')
    MILVUS_TOKEN = config('MILVUS_TOKEN')
