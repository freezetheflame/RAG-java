from sqlalchemy import Column

from app.extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo

class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(db.Integer, primary_key=True)
    text_hash = Column(db.String(64), unique=True)  # 问题文本哈希值
    text = Column(db.String(500), nullable=False)
    meta_info = Column(db.JSON)  # 存储category/difficulty等元信息