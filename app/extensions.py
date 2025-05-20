from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from app.db.doc_to_oss import DocToOSS
from app.pipelines.pipeline import ProcessingPipeline



db = SQLAlchemy()
redis_client = FlaskRedis()
oss_client = DocToOSS()
upload_pipeline = ProcessingPipeline()