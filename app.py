from flask import Flask, request, jsonify,render_template
from nlp_utils import generate_response
import spacy
import os
import subprocess
import sys

app = Flask(__name__)
chat_history = {}


# Ensure the SpaCy small English model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Model not found, download it
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_id = data.get("user_id", "default")
    user_message = data.get("message", "")

    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append({"role": "user", "text": user_message})
    bot_reply = generate_response(user_message, chat_history[user_id])
    chat_history[user_id].append({"role": "bot", "text": bot_reply})

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
