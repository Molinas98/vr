from flask import Flask, request, render_template, url_for, jsonify, send_from_directory
import os
import qrcode

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
QR_FOLDER = 'static/qr/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Generar el código QR con enlace al modelo 3D
    model_url = url_for('view_model', filename=file.filename, _external=True)
    qr_path = os.path.join(QR_FOLDER, f"{file.filename}.png")
    qr = qrcode.make(model_url)
    qr.save(qr_path)

    return jsonify({'modelUrl': model_url, 'qrUrl': f"/{qr_path}"})

@app.route('/view/<filename>')
def view_model(filename):
    return render_template('view3d.html', model_file=filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(QR_FOLDER, exist_ok=True)
    app.run(debug=True)
