FROM python:3.11-slim
LABEL authors="lhy"

# 设置工作目录
WORKDIR /app 

# 安装依赖
COPY  requirements.txt . 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask[async]
RUN pip install --no-cache-dir -U huggingface_hub
ENV HF_ENDPOINT=https://hf-mirror.com

# 复制应用代码
COPY . .


# 启动命令
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]