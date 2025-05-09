from app.extensions import db


class UserAnswer(db.Base):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.String(2000), nullable=True)
    ai_analysis = db.Column(db.String(2000), nullable=True)
    is_passed = db.Column(db.Boolean, nullable=True)
    score = db.Column(db.Integer, nullable=True)