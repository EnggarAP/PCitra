from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'

# Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Konversi RGB ke Grayscale ==> Biner manual
def convert_image_to_binary(image_path, result_path, threshold=127):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size
    binary_image = Image.new('L', (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            binary = 255 if gray >= threshold else 0
            binary_image.putpixel((x, y), binary)

    binary_image.save(result_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['image']
        threshold = int(request.form['threshold']) # Ambil input threshold
        
        if uploaded_file.filename != '':
            input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            result_path = os.path.join(RESULT_FOLDER, 'binary_' + uploaded_file.filename)
            uploaded_file.save(input_path)

            # Panggil fungsi dengan threshold dari user
            convert_image_to_binary(input_path, result_path, threshold)

            return render_template('index.html',
                                   original_image=input_path,
                                   result_image=result_path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
