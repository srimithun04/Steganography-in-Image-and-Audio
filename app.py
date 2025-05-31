from flask import Flask, request, render_template, send_file
import wave
import cv2
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper Functions for Audio Steganography
def encode_audio(input_audio_path, message, output_audio_path):
    with wave.open(input_audio_path, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))
        message += '\0'
        bits = ''.join([bin(ord(i))[2:].zfill(8) for i in message])
        
        if len(bits) > len(frames):
            raise ValueError("Message is too large to encode in the audio file.")
        
        for i, bit in enumerate(bits):
            frames[i] = (frames[i] & 254) | int(bit)

        with wave.open(output_audio_path, 'wb') as output:
            output.setparams(audio.getparams())
            output.writeframes(bytes(frames))

def decode_audio(input_audio_path):
    with wave.open(input_audio_path, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))
        bits = [str(frames[i] & 1) for i in range(len(frames))]
        
        chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
        decoded_message = ''.join(chars).split('\0')[0]
        return decoded_message

# Helper Functions for Image Steganography
def encode_image(input_image_path, message, output_image_path):
    img = cv2.imread(input_image_path)
    message += '\0'
    bits = ''.join([bin(ord(i))[2:].zfill(8) for i in message])

    flat_img = img.flatten()
    if len(bits) > len(flat_img):
        raise ValueError("Message is too large to encode in the image.")

    for i, bit in enumerate(bits):
        flat_img[i] = (flat_img[i] & 254) | int(bit)

    encoded_img = flat_img.reshape(img.shape)
    cv2.imwrite(output_image_path, encoded_img)

def decode_image(input_image_path):
    img = cv2.imread(input_image_path)
    flat_img = img.flatten()

    bits = [str(flat_img[i] & 1) for i in range(len(flat_img))]
    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    decoded_message = ''.join(chars).split('\0')[0]
    return decoded_message

# Flask Routes
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    file = request.files['file']
    message = request.form['message']
    media_type = request.form['media_type']
    
    if file and message and media_type:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"encoded_{filename}")

        try:
            if media_type == 'audio':
                encode_audio(input_path, message, output_path)
            elif media_type == 'image':
                encode_image(input_path, message, output_path)
            else:
                return "Unsupported media type.", 400
        except Exception as e:
            return str(e), 400

        return send_file(output_path, as_attachment=True)
    return "Missing required data.", 400

@app.route('/decode', methods=['POST'])
def decode():
    file = request.files['file']
    media_type = request.form['media_type']

    if file and media_type:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        try:
            if media_type == 'audio':
                message = decode_audio(input_path)
            elif media_type == 'image':
                message = decode_image(input_path)
            else:
                return render_template('error.html', message="Unsupported media type.")

        except Exception as e:
            return render_template('error.html', message=str(e))

        return render_template('result.html', decoded_message=message)
    return render_template('error.html', message="Missing required data.")

if __name__ == '__main__':
    app.run(debug=True)
