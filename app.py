from flask import Flask, request, jsonify, render_template
import os
import random
import re
import spacy

app = Flask(__name__)
chat_history = {}

# ---------------------------
# NLP setup with spaCy
# ---------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ---------------------------
# Greeting + response sets
# ---------------------------
GREETINGS = ["hello", "hi", "hey", "hola", "greetings"]

GREETING_RESPONSES = [
    "Hey! This is GreatWall Chatbot 🛡, how can I help you?",
    "Hello there! Ready to detect some fake URLs?",
    "Hi! I'm your fraud detection assistant. How can I assist?",
    "Hey! Let's keep your browsing safe today.",
    "Greetings! Tell me a URL and I'll check it for you."
]

SAFE_RESPONSES = [
    "It seems completely safe ✅. You can continue browsing with confidence.",
    "All clear! This site doesn’t show any immediate risks.",
    "No threats detected for this link. Keep your browsing habits safe!"
]

SUSPICIOUS_RESPONSES = [
    "⚠ Be cautious! This URL might be malicious or deceptive.",
    "Hmm, this link looks suspicious. Consider double-checking before visiting.",
    "Warning! This website may not be secure. Stay alert!"
]

def get_greeting_response():
    return random.choice(GREETING_RESPONSES)

def get_safe_response():
    return random.choice(SAFE_RESPONSES)

def get_suspicious_response():
    return random.choice(SUSPICIOUS_RESPONSES)

# ---------------------------
# URL scoring function
# ---------------------------
def score_url(url: str) -> dict:
    score = 100
    reasons = []
    url_lower = url.lower()

    # Detect suspicious keywords
    suspicious_keywords = ["login", "verify", "update", "secure", "bank", "paypal"]
    if any(word in url_lower for word in suspicious_keywords):
        score -= 30
        reasons.append("Contains suspicious keyword")

    # Penalize for using HTTP
    if url_lower.startswith("http://"):
        score -= 50
        reasons.append("Uses HTTP instead of HTTPS (insecure connection)")

    # Clamp score between 0 and 100
    score = max(0, min(100, score))

    if score < 40:
        label = "dangerous"
    elif score < 70:
        label = "suspicious"
    else:
        label = "safe"

    if not reasons:
        reasons.append("No obvious red flags detected")

    return {"score": score, "label": label, "reasons": reasons}

# ---------------------------
# Routes
# ---------------------------
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

    # NLP preprocessing (optional sentiment or token usage)
    doc = nlp(user_message.lower())

    # Decide response
    if any(greet in user_message.lower() for greet in GREETINGS):
        bot_reply = get_greeting_response() + " 😊 How can I assist you today? You can send me any URL to check its safety."
    elif re.match(r"^https?://", user_message.lower()):
        url = user_message
        result = score_url(url)
        if result["label"] == "safe":
            bot_reply = f"✅ The URL '{url}' looks safe. {get_safe_response()} Your browsing is secure!"
        else:
            bot_reply = f"⚠️ Attention! The URL '{url}' seems {result['label']}. Reasons: {', '.join(result['reasons'])}. Be careful before visiting this link!"
    else:
        bot_reply = (
            "I can help you check if a URL is safe or suspicious. "
            "Try sending me a link like 'https://example.com', or you can chat with me about online security tips! "
            "I can provide guidance and advice to keep you safe online."
        )

    chat_history[user_id].append({"role": "bot", "text": bot_reply})

    return jsonify({"response": bot_reply})

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
