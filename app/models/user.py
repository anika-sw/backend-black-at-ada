from app import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False) 
    pronouns = db.Column(db.String, nullable=True)
    cohort = db.Column(db.Integer, nullable=False) 
    location_name = db.Column(db.String, nullable=False)
    location_lat = db.Column(db.String, nullable=True)
    location_lng = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_pic_file = db.Column(db.String, nullable=True)
    company = db.Column(db.String, nullable=True)
    linkedin = db.Column(db.String, nullable=True)
    job_title = db.Column(db.String, nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    years_experience = db.Column(db.String, nullable=True)
    include_name_salary = db.Column(db.String, nullable=False)
    user_first_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_last_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    events = db.relationship("Event", secondary="event_user", back_populates="users")

    
    def to_dict(self):
        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "cohort": self.cohort,
            "location_name": self.location_name,
            "email": self.email,
            "password": self.password,
            "profile_pic_file": self.profile_pic_file,
            "include_name_salary": self.include_name_salary,
            "user_first_created": self.user_first_created,
            "user_last_updated": self.user_last_updated
        }
        if self.pronouns:
            user_dict["pronouns"] = self.pronouns
        if self.location_lat:
            user_dict["location_lat"] = self.location_lat
        if self.location_lng:
            user_dict["location_lng"] = self.location_lng
        if self.company:
            user_dict["company"] = self.company
        if self.linkedin:
            user_dict["linkedin"] = self.linkedin
        if self.job_title:
            user_dict["job_title"] = self.job_title
        if self.salary:
            user_dict["salary"] = self.salary
        if self.years_experience:
            user_dict["years_experience"] = self.years_experience
        if self.events:
            user_dict["events"] = [event.id for event in self.events]
        return user_dict

    @classmethod
    def from_dict(cls, data):
        return User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            pronouns=data["pronouns"],
            cohort=data["cohort"],
            location_name=data["location_name"],
            location_lat=data["location_lat"],
            location_lng=data["location_lng"],
            email=data["email"],
            password=data["password"],
            profile_pic_file=data["profile_pic_file"],
            company=data["company"],
            linkedin=data["linkedin"],
            job_title=data["job_title"],
            salary=data["salary"],
            years_experience=data["years_experience"],
            include_name_salary=data["include_name_salary"]
        )