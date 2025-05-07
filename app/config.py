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
    ACCESS_KEY_ID = config('ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = config('ACCESS_KEY_SECRET')
    ENDPOINT_URL = config('ENDPOINT_URL')
    HUNYUAN_API_KEY = config('HUNYUAN_API_KEY')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI')
    LANGSMITH_TRACING = config('LANGSMITH_TRACING')
    LANGSMITH_PROJECT = config('LANGSMITH_PROJECT')
    LANGSMITH_API_KEY = config('LANGSMITH_API_KEY')
    LANGSMITH_ENDPOINT = config('LANGSMITH_ENDPOINT')
    Aliyun_AK_ID = config('Aliyun_AK_ID')
    Aliyun_AK_SECRET = config('Aliyun_AK_SECRET')
    Aliyun_APP_KEY = config('Aliyun_APP_KEY')
    NEO4J_URI = config('NEO4J_URI')
    NEO4J_USERNAME = config('NEO4J_USERNAME')
    NEO4J_PASSWORD = config('NEO4J_PASSWORD')
    SECRET_KEY = config('SECRET_KEY')
