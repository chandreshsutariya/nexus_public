```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_photos.db'
db = SQLAlchemy(app)

# Models
class EventPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(80), nullable=False)
    photo_path = db.Column(db.String(120), nullable=False)

class FacialFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(80), nullable=False)
    feature_vector = db.Column(db.PickleType, nullable=False)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Routes
@app.route('/upload', methods=['POST'])
def upload_event_photos():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'})
    
    files = request.files.getlist('files')
    event_id = request.form.get('event_id')
    if not event_id:
        return jsonify({'error': 'Event ID is required'})

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            photo_path = os.path.join('uploads', f"{event_id}_{file.filename}")
            file.save(photo_path)
            new_photo = EventPhoto(event_id=event_id, photo_path=photo_path)
            db.session.add(new_photo)

    db.session.commit()
    return jsonify({'message': 'Photos uploaded successfully'})

@app.route('/generate_faces/<event_id>', methods=['POST'])
def generate_faces(event_id):
    # Placeholder for faceGrouper.py execution
    # This function should call the face detection algorithm 
    # and save the features into the FacialFeature database.
    return jsonify({'message': 'Facial features generated'})

@app.route('/find_photos', methods=['POST'])
def find_photos():
    mobile_number = request.form.get('mobile_number')
    selfie = request.files.get('selfie')
    
    if not mobile_number or not selfie:
        return jsonify({'error': 'Mobile number and selfie are required'})
    
    # Handle photo comparison logic here with imageFinder.py


if __name__ == '__main__':
    db.create_all()
    app.run(ssl_context='adhoc')  # For HTTPS
```