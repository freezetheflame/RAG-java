from app.extensions import db


class Answer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    interview_question_id = db.Column(db.Integer, db.ForeignKey('interview_questions.id'), nullable=False)
    text = db.Column(db.String(2000), nullable=True)
    evaluation = db.Column(db.String(2000),nullable=True)