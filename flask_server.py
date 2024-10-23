import os
from flask import Flask, request

app = Flask(__name__)
UPLOAD_FOLDER = '/home/ubuntu/SATS_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return f"File uploaded to {file_path}", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)