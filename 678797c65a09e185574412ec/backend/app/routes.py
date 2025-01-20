```python
from flask import Flask, request, jsonify
from models import db, EventPhoto, FacialFeature, PasswordEntry, MatchedResult
from security.auth import generate_password_hash, verify_password
from face_recognition import process_faces, find_matching_faces  # Assuming these are implemented
import os

app = Flask(__name__)
db.init_app(app)

@app.route('/upload', methods=['POST'])
def upload_photos():
    event_id = request.form['event_id']
    files = request.files.getlist('photos')
    if not os.path.exists(f'data/{event_id}'):
        os.makedirs(f'data/{event_id}')
    
    for file in files:
        file.save(f'data/{event_id}/{file.filename}')
    
    return jsonify({'message': 'Photos uploaded successfully'}), 200

@app.route('/generate_faces/<event_id>', methods=['POST'])
def generate_faces(event_id):
    process_faces(event_id)
    return jsonify({'message': 'Facial features generated successfully'}), 200

@app.route('/create_password/<event_id>', methods=['POST'])
def create_password(event_id):
    password = request.json['password']
    hashed_password = generate_password_hash(password)
    password_entry = PasswordEntry(event_id=event_id, password_hash=hashed_password)
    db.session.add(password_entry)
    db.session.commit()
    
    return jsonify({'message': 'Password created successfully'}), 201

@app.route('/find_photos', methods=['POST'])
def find_photos():
    mobile_number = request.json['mobile_number']
    selfie = request.files['selfie']
    matches = find_matching_faces(mobile_number, selfie)
    
    return jsonify({'matched_images': matches}), 200

if __name__ == '__main__':
    app.run(debug=True)
```