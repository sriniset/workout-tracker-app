from app import db

#simple data model with id as primary key, type, duration (minutes), and date
#type is locked to running, biking, and swimming for simplicity
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(25), nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, nullable = False)

    __table_args__ = (
        db.CheckConstraint(type.in_(['running', 'biking', 'swimming']), name = 'check_workout_type'),
    )