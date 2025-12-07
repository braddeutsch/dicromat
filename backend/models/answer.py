from datetime import datetime, timezone
from . import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(36), db.ForeignKey('test_session.id'), nullable=False)
    image_number = db.Column(db.Integer, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Integer, nullable=True)
    dichromism_type = db.Column(db.String(20), nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('session_id', 'image_number', name='unique_session_image'),
        db.CheckConstraint('image_number >= 1 AND image_number <= 10', name='valid_image_number'),
        db.CheckConstraint('correct_answer >= 0 AND correct_answer <= 99', name='valid_correct_answer'),
        db.CheckConstraint('user_answer IS NULL OR (user_answer >= 0 AND user_answer <= 99)', name='valid_user_answer'),
    )

    def to_dict(self):
        return {
            'image_number': self.image_number,
            'correct_answer': self.correct_answer,
            'user_answer': self.user_answer,
            'is_correct': self.user_answer == self.correct_answer,
            'dichromism_type': self.dichromism_type
        }
