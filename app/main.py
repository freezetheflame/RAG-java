from flask import Flask
from flask_cors import CORS

from app.api.endpoints import chat, search, document
from app.config import Settings
from app.db.milvus_client import milvus_client

app = Flask(__name__)

@app.route('/')
def home():
    #using as a health check
    return 'Hello, World!'


def create_app():
    app.register_blueprint(chat.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(document.bp)
    milvus_client.connect(app)
    set_env()
    CORS(app, supports_credentials=True)
    return app

def set_env():
    import os
    os.environ['LANGSMITH_ENDPOINT'] = Settings.LANGSMITH_ENDPOINT
    os.environ['LANGSMITH_API_KEY'] = Settings.LANGSMITH_API_KEY
    os.environ['LANGSMITH_TRACING'] = Settings.LANGSMITH_TRACING
    os.environ['LANGSMITH_PROJECT'] = Settings.LANGSMITH_PROJECT

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000,debug=True)