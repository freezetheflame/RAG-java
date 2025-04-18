from flask import Flask
from flask_cors import CORS

from app.api.endpoints import chat, search, document
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
    CORS(app, supports_credentials=True)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000,debug=True)