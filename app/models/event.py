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
    radio_selection = db.Column(db.String, nullable=False)
    is_map_showing = db.Column(db.String, nullable=True)
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
            "target_audience": self.target_audience,
            "created_by_id": self.created_by_id
        }
        if self.video_conf_link:
            event_dict["video_conf_link"] = self.video_conf_link
        if self.meeting_key:
            event_dict["meeting_key"] = self.meeting_key
        if self.radio_selection:
            event_dict["radio_selection"] = self.radio_selection
        if self.is_map_showing:
            event_dict["is_map_showing"] = self.is_map_showing
        if self.location_address:
            event_dict["location_address"] = self.location_address
        if self.location_lat:
            event_dict["location_lat"] = self.location_lat
        if self.location_lng:
            event_dict["location_lng"] = self.location_lng
        if self.organizer_first_name:
            event_dict["organizer_first_name"] = self.organizer_first_name
        if self.organizer_last_name:
            event_dict["organizer_last_name"] = self.organizer_last_name
        if self.organizer_pronouns:
            event_dict["organizer_pronouns"] = self.organizer_pronouns
        if self.organizer_email:
            event_dict["organizer_email"] = self.organizer_email
        if self.users:
            event_dict["users"] = self.users
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
            radio_selection=data["radio_selection"],
            is_map_showing=data["is_map_showing"],
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