from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate

from app.api.endpoints import chat, search, document
from app.config import Settings
from app.db.milvus_client import milvus_client
from app.db.neo4j_client import neo4j_client

app = Flask(__name__)
db = SQLAlchemy()


@app.route('/')
def home():
    #using as a health check
    return 'Hello, World!'


def create_app():
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(chat.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(document.bp)
    milvus_client.connect(app)
    neo4j_client.connect(app)
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