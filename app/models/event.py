from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) #limit characters
    description = db.Column(db.String) #limit characters
    date = db.Column # are date and time one column? make sure local to calendar viewer; must be aware
    time = db.Column # are date and time one column? make sure local to calendar viewer; must be aware
    location = db.Column(db.String) #need to make sure to control for case
    organizer_first_name = db.Column(db.String) #need to make sure to control for case
    organizer_last_name = db.Column(db.String) #need to make sure to control for case
    organizer_email = db.Column(db.String) #need to make sure to control for case
    target_audience = db.Column(db.String)
    attendees = db.relationship("User", back_populates="event", lazy=True)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title, 
            "description": self.description, 
            "date": self.date,
            "time": self.time,
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
            date=data["date"],
            time=data["time"],
            location=data["location"],
            organizer_first_name=data["organizer_first_name"],
            organizer_last_name=data["organizer_last_name"],
            organizer_email=data["organizer_email"],
            target_audience=data["target_audience"]
        )