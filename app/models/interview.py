from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db

class Interview(db.Base):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # 可与用户表关联
    started_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))
    ended_at = db.Column(db.DateTime, nullable=True)
    final_score = db.Column(db.Integer, nullable=True)  # 总分（0~100）
    feedback = db.Column(db.String(1000), nullable=True)  # AI生成的反馈