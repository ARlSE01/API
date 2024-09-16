from flask import Flask, request, send_file, jsonify
import os
import uuid

app = Flask(__name__)


db = './uploads'
if not os.path.exists(db):
    os.makedirs(db)

# 1.Upload File
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part found'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_id = str(uuid.uuid4())
    file.save(os.path.join(db, file_id))
    
    return jsonify({'file_id': file_id}), 201

# 2.Download File
@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    file_path = os.path.join(db, file_id)
    
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({'error': 'File not found'}), 404

# 3.Update file
@app.route('/update/<file_id>', methods=['PUT'])
def update_file(file_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    file_path = os.path.join(db, file_id)
    
    if os.path.exists(file_path):
        file.save(file_path)
        return jsonify({'message': 'File updated successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

# Delete File
@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    file_path = os.path.join(db, file_id)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
