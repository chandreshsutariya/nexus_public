from flask import request, jsonify
from app import app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'data/temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Trigger face recognition processing here (e.g. faceGrouper.py)
        return jsonify({'success': 'File uploaded successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
