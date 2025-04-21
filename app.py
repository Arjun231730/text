import os
import requests
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"
OCR_API_KEY = "bbef5d657f88957"  # Your Space OCR API key

@app.route("/", methods=["GET", "POST"])
def index():
    raw_text = ""
    error = None

    if request.method == "POST":
        image = request.files.get("image")
        if image:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filepath)

            with open(filepath, "rb") as f:
                response = requests.post(
                    "https://api.ocr.space/parse/image",
                    files={"file": f},
                    data={
                        "apikey": OCR_API_KEY,
                        "language": "eng",
                        "OCREngine": "2",
                        "scale": "true",
                        "detectOrientation": "true"
                    }
                )

            try:
                result = response.json()
                if not result.get("IsErroredOnProcessing"):
                    raw_text = result["ParsedResults"][0]["ParsedText"]
                else:
                    error = "❌ OCR failed. Please check the image."
            except Exception:
                error = "⚠️ Unexpected error occurred."

    return render_template("index.html", raw_text=raw_text, error=error)

if __name__ == "__main__":
    app.run(debug=True)
