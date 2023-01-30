from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String, nullable=False) #need to make sure to control for case
    last_name = db.Column(db.String, nullable=False) #need to make sure to control for case
    cohort = db.Column(db.Integer, nullable=False) #need to make sure to control for case
    location_name = db.Column(db.String, nullable=False)
    location_lat = db.Column(db.Numeric(8,6), nullable=True)
    location_lng = db.Column(db.Numeric(9,6), nullable=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False) #look up password type in Flask db
    company = db.Column(db.String, nullable=True)
    linkedin = db.Column(db.String, nullable=True)
    job_title = db.Column(db.String, nullable=True)
    salary = db.Column(db.Integer, nullable=True)
    years_experience = db.Column(db.Integer, nullable=True)
    user_last_updated = db.Column(db.DateTime, nullable=False)
    events = db.relationship("Event", secondary="event_user", back_populates="users")


    def to_dict(self):
        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "cohort": self.cohort,
            "location_name": self.location_name,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "email": self.email,
            "password": self.password,
            "user_last_updated": self.user_last_updated
        }
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
            event_titles = [event.title for event in self.events]
            user_dict["events"] = event_titles
        return user_dict

    @classmethod
    def from_dict(cls, data):
        return User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            cohort=data["cohort"],
            location_name=data["location_name"],
            location_lat=data["location_lat"],
            location_lng=data["location_lng"],
            email=data["email"],
            password=data["password"],
            company=data["company"],
            linkedin=data["linkedin"],
            job_title=data["job_title"],
            salary=data["salary"],
            years_experience=data["years_experience"]
        )