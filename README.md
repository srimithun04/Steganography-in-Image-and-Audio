# Steganography-in-Image-and-Audio

## 👋 Introduction

Steganography Master is a web app for hiding and revealing secret messages in images (PNG, JPG) and audio (WAV) files using LSB steganography. It's an educational tool for exploring data hiding.

## ✨ Key Features

* **Encode/Decode:** Embed or extract text in images and WAV audio.
* **User-Friendly UI:** Simple interface for uploads, messaging, and media selection, with clear output.
* **Responsive Design:** Includes a dark/light theme toggle.
* **Secure & Downloadable:** Uses secure file handling and allows downloading encoded files.

## 🛠️ Technologies Used

* **Backend:** Python, Flask
* **Steganography:** `wave` module, OpenCV-Python (cv2), LSB logic
* **Frontend:** HTML5, CSS3 (custom properties), JavaScript
* **File Handling:** Python OS libraries

## 🚀 Getting Started

### Prerequisites

* Python 3.x, Flask, OpenCV-Python, NumPy

### Installation & Setup
1.  **Venv (Recommended):** `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
2.  **Install:** `pip install Flask opencv-python numpy`
3.  **Run:** `python app.py`
4.  Access at `http://127.0.0.1:5000/`.

## 📁 Project Structure


.
├── app.py                # Main Flask application
├── static/
│   └── css/
│       ├── landing.css   # Styles for landing page
│       ├── style.css     # Styles for main tool
│       └── result.css    # Styles for result page
├── templates/
│   ├── landing.html      # Welcome page
│   ├── index.html        # Main tool page
│   ├── result.html       # Decoded message display
│   └── error.html        # (Optional) Error display
└── uploads/              # Temporary file uploads


## 🎯 Purpose

This project demonstrates LSB steganography and serves as an educational resource for data security and web development with Python/Flask.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! See the [issues page](https://github.com/srimithun04/Steganography-in-Image-and-Audio/issues).

---

