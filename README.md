# 🧙 oracle_web

A lightweight web app that performs Optical Character Recognition (OCR) on uploaded images using Python and Flask. Ideal for extracting text from documents or images through a simple web interface.

## 🚀 Features

- Upload image files and extract text using OCR.
- Display extracted results on a web page.
- Easily customizable configuration via JSON.

## 📁 Project Structure

    oracle_web/
    │
    ├── app.py             # Main Flask app
    ├── ocr.py             # OCR functionality using pytesseract
    ├── utils.py           # Utility functions for handling image data
    ├── config.json        # Primary OCR configuration
    ├── config2.json       # Alternate configuration file
    ├── config3.json       # Another alternate configuration
    │
    ├── static/            # Static assets (e.g., CSS, JS)
    └── templates/         # HTML templates (Jinja2)

## 🧠 How it Works

1. A user uploads an image via the web interface.
2. The app processes the image using Tesseract OCR (`ocr.py`).
3. Extracted text is displayed on a results page.

## 🛠️ Installation

~~~bash
git clone https://github.com/lKingslayer/oracle_web.git
cd oracle_web
pip install -r requirements.txt
python app.py
~~~

Make sure you have [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and available in your system path.

## 🖼️ Screenshot

*(Add screenshots here of the upload interface and results display if available)*

## 🔧 Configuration

You can modify the `config.json` (or `config2.json`, `config3.json`) to customize OCR settings like language, preprocessing options, etc.

## 📜 License

MIT License *(or specify if different)*
