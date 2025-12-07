import uuid
from datetime import datetime, timezone
from . import db


class TestSession(db.Model):
    __tablename__ = 'test_session'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    metadata_json = db.Column(db.JSON, nullable=True)
    # Mapping of test image numbers (1-10) to pre-generated image IDs (0-99)
    # Format: {"1": 5, "2": 12, ...} (keys are strings in JSON)
    image_mapping = db.Column(db.JSON, nullable=True)

    answers = db.relationship('Answer', backref='session', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'session_id': self.id,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'completed_at': self.completed_at.isoformat() + 'Z' if self.completed_at else None,
            'total_images': 10
        }
