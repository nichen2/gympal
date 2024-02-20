from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def register(cls, username,pwd,email,first_name,last_name):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_password = hashed.decode("utf8")

        return cls(first_name=first_name, last_name=last_name, email=email, username=username, password=hashed_password)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that this user exists and return user, if not valid return false"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        
class Exercise(db.Model):
    """Model for individual exercises"""
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text)
    muscle = db.Column(db.Text)
    difficulty = db.Column(db.Text)
    instructions = db.Column(db.Text)

class Workout(db.Model):
    "Model for workouts that consist of different exercises"
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    exercises = db.relation('Exercise', secondary='workout_exercises', backref='workouts')

class WorkoutExercise(db.Model):
    """Model for the exercises that are contained to different workouts, many to many relationship"""
    __tablename__ = "workout_exercises"

    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), primary_key=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)

# When making log we need to change this, log has to be independent of Workout because if a user ever touched workouts then it would affect past log
# Also, because if a user editted their workout or deleted it, information on log needs to persist
class WorkoutLog(db.Model):
    __tablename__ = "workout_logs"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    workout_type = db.Column(db.Text)  # For example: "Upper Body", "Cardio", etc.
    notes = db.Column(db.Text)

    workout = db.relationship('Workout', backref='logs')
    user = db.relationship('User', backref='workout_logs')
