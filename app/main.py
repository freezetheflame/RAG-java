from flask import Flask

from app.api.endpoints import chat

app = Flask(__name__)

@app.route('/')
def home():
    #using as a health check
    return 'Hello, World!'


def create_app():
    app.register_blueprint(chat.bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)