from app import db

class EventUser(db.Model):
    __tablename__ = "event_user"
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)