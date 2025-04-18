FROM python:3.9-slim
LABEL authors="lhy"

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ .

# 设置Flask 环境变量
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:create_app()"]