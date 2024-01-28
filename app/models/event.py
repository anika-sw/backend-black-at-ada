from app import db
from sqlalchemy.sql import func

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False) #limit characters
    description = db.Column(db.String, nullable=False) #limit characters
    image_url = db.Column(db.String, nullable=False)
    date_time_start = db.Column(db.DateTime(timezone=False), nullable=False)
    date_time_stop = db.Column(db.DateTime(timezone=False), nullable=False)
    timezone = db.Column(db.String, nullable=False)
    video_conf_link = db.Column(db.String, nullable=True)
    meeting_key = db.Column(db.String, nullable=True)
    online_in_person = db.Column(db.String, nullable=False)
    location_address = db.Column(db.String, nullable=True)
    location_lat = db.Column(db.String, nullable=True)
    location_lng = db.Column(db.String, nullable=True)
    organizer_first_name = db.Column(db.String, nullable=True) 
    organizer_last_name = db.Column(db.String, nullable=True) 
    organizer_pronouns = db.Column(db.String, nullable=True) 
    organizer_email = db.Column(db.String, nullable=True) 
    target_audience = db.Column(db.String, nullable=False)
    created_by_id = db.Column(db.Integer, nullable=False)
    date_time_created = db.Column(db.DateTime(timezone=False), server_default=func.now())
    users = db.relationship("User", secondary="event_user", back_populates="events")


    def to_dict(self):
        event_dict = {
            "id": self.id,
            "title": self.title, 
            "description": self.description, 
            "image_url": self.image_url,
            "date_time_start": self.date_time_start,
            "date_time_stop": self.date_time_stop,
            "timezone": self.timezone,
            "video_conf_link": self.video_conf_link,
            "meeting_key": self.meeting_key,
            "online_in_person": self.online_in_person,
            "location_address": self.location_address,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "organizer_first_name": self.organizer_first_name, 
            "organizer_last_name": self.organizer_last_name, 
            "organizer_pronouns": self.organizer_pronouns, 
            "organizer_email": self.organizer_email, 
            "target_audience": self.target_audience,
            "created_by_id": self.created_by_id
        }
        event_dict["users"] = [user.id for user in self.users] if self.users else []
        return event_dict

    @classmethod
    def from_dict(cls, data):
        return Event(
            title=data["title"],
            description=data["description"], 
            image_url=data["image_url"],
            date_time_start=data["date_time_start"],
            date_time_stop=data["date_time_stop"],
            timezone=data["timezone"],
            video_conf_link=data["video_conf_link"],
            meeting_key=data["meeting_key"],
            online_in_person=data["online_in_person"],
            location_address=data["location_address"],
            location_lat=data["location_lat"],
            location_lng=data["location_lng"],
            organizer_first_name=data["organizer_first_name"],
            organizer_last_name=data["organizer_last_name"],
            organizer_pronouns=data["organizer_pronouns"],
            organizer_email=data["organizer_email"],
            target_audience=data["target_audience"],
            created_by_id=data["created_by_id"]
        )