from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String) #need to make sure to control for case
    last_name = db.Column(db.String) #need to make sure to control for case
    cohort = db.Column(db.String) #need to make sure to control for case
    location = db.Column(db.String)
    email = db.Column(db.String)
    # goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    # goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "cohort": self.cohort,
            "location": self.location,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        return User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            cohort=data["cohort"],
            location=data["location"],
            email=data["email"]
        )