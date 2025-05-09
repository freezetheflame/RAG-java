from app.extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo

class Question(db.Base):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100))  # 如：技术、行为、产品等
    difficulty = db.Column(db.String(50))  # 如：easy, medium, hard
    is_required = db.Column(db.Boolean, default=True)  # 是否为必答题
    depends_on = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=True)  # 父问题ID
    created_at = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))
    # 子问题关系
    children = db.relationship("Question", backref=db.backref('parent', remote_side=[id]))
    parent = db.relationship("Question", remote_side=[id], back_populates="children")