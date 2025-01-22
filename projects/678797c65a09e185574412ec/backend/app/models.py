from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EventPhoto(db.Model):
    __tablename__ = 'event_photos'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class FacialFeature(db.Model):
    __tablename__ = 'facial_features'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, nullable=False)
    face_vector = db.Column(db.PickleType, nullable=False)  # Store facial features as pickled data
    uploaded_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Password(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)

class MatchedFace(db.Model):
    __tablename__ = 'matched_faces'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, nullable=False)
    mobile_number = db.Column(db.String, nullable=False)
    matched_image_path = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
