Here's the code for the `models.py` file based on the outlined project structure:

```python
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database object
db = SQLAlchemy()

class EventPhoto(db.Model):
    __tablename__ = 'event_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, nullable=False)
    photo_path = db.Column(db.String, nullable=False)

class FacialFeature(db.Model):
    __tablename__ = 'facial_features'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, nullable=False)
    feature_vector = db.Column(db.PickleType, nullable=False)

class PasswordEntry(db.Model):
    __tablename__ = 'passwords'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

class MatchedResults(db.Model):
    __tablename__ = 'matched_results'
    
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String, nullable=False)
    matched_photo_path = db.Column(db.String, nullable=False)
    event_id = db.Column(db.String, nullable=False)
```

This code defines the database models needed for the Face Recognition System, including tables for event photos, facial features, passwords, and matched results. Each class corresponds to a table in the database, and appropriate columns are defined within these classes.