from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from PIL import Image, ImageDraw
import os

app = Flask(__name__)

# Directory to save generated QR codes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    url = request.form['url']
    color = request.form.get('color', 'black')
    shape = request.form.get('shape', 'square')

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill=color, back_color="white").convert("RGB")

    # Apply shape mask
    img_with_shape = apply_shape_mask(img, shape)

    # Save QR image to file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qr_code.png')
    img_with_shape.save(file_path)

    return send_file(file_path, mimetype='image/png', as_attachment=True)

def apply_shape_mask(qr_image, shape):
    width, height = qr_image.size
    mask = Image.new("L", (width, height), 255)  # Start with a white mask (opaque)
    draw = ImageDraw.Draw(mask)

    if shape == "square":
        draw.rectangle([0, 0, width, height], fill=255)  # Full area
    elif shape == "circle":
        draw.ellipse([0, 0, width, height], fill=255)  # Full circle
    elif shape == "triangle":
        draw.polygon([(width // 2, 0), (width, height), (0, height)], fill=255)  # Full triangle

    qr_image.putalpha(mask)  # Apply mask to the QR code image
    return qr_image

if __name__ == "__main__":
    app.run(debug=True)
