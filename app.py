import os, uuid, random
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'screenshot' not in request.files:
            return render_template('index.html', error="No file part")
        file = request.files['screenshot']
        if file.filename == '':
            return render_template('index.html', error="No file selected")
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = str(uuid.uuid4()) + '.' + ext
            file_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(file_path)
            dummy_accuracy = random.randint(60, 98)
            result_text = f"Dummy Signal Accuracy: {dummy_accuracy}%"
            image_url = url_for('static', filename=f'uploads/{unique_name}')
            return render_template('index.html', result_text=result_text, image_url=image_url)
        else:
            return render_template('index.html', error="Unsupported file type. Please upload an image.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
