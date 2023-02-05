from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False) #limit characters
    description = db.Column(db.String, nullable=False) #limit characters
    # datetime = db.Column # are date and time one column? make sure local to calendar viewer; must be aware
    location_address = db.Column(db.String, nullable=False) #need to make sure to control for case
    location_lat = db.Column(db.String, nullable=True)
    location_lng = db.Column(db.String, nullable=True)
    organizer_first_name = db.Column(db.String, nullable=False) #need to make sure to control for case
    organizer_last_name = db.Column(db.String, nullable=False) #need to make sure to control for case
    organizer_email = db.Column(db.String, nullable=False) #need to make sure to control for case
    target_audience = db.Column(db.String, nullable=False)
    event_creator_id = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", secondary="event_user", back_populates="events")


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title, 
            "description": self.description, 
            # "date": self.date,
            # "time": self.time,
            "location": self.location,
            "organizer_first_name": self.organizer_first_name,
            "organizer_last_name": self.organizer_last_name,
            "organizer_email": self.organizer_email,
            "target_audience": self.target_audience,
            "attendees": []
        }

    @classmethod
    def from_dict(cls, data):
        return Event(
            title=data["title"],
            description=data["description"], 
            # date=data["date"],
            # time=data["time"],
            location=data["location"],
            organizer_first_name=data["organizer_first_name"],
            organizer_last_name=data["organizer_last_name"],
            organizer_email=data["organizer_email"],
            target_audience=data["target_audience"]
        )