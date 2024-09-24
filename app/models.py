# app/models.py
from . import db
from datetime import datetime

class BrokenLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    status_code = db.Column(db.String(50), nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BrokenLink {self.url} in {self.page}>'

class SpamReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<SpamReport {self.id} detected at {self.detected_at}>'
