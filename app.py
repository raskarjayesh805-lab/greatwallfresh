from flask import Flask, request, jsonify, render_template
import os
import random
import re

app = Flask(__name__)
chat_history = {}

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
    "This URL seems safe ✅",
    "All clear! You can visit this website.",
    "No threats detected for this link.",
]

SUSPICIOUS_RESPONSES = [
    "⚠ This URL looks suspicious, be careful!",
    "Hmm, this one might be fake. Double-check before visiting.",
    "Warning! This website may not be secure.",
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

    suspicious_keywords = ["login", "verify", "update", "secure", "bank", "paypal"]
    if any(word in url_lower for word in suspicious_keywords):
        score -= 30
        reasons.append("Contains suspicious keyword")

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

    # Decide response
    if any(greet in user_message.lower() for greet in GREETINGS):
        bot_reply = get_greeting_response()
    elif user_message.startswith("http"):
        result = score_url(user_message)
        if result["label"] == "safe":
            bot_reply = get_safe_response()
        else:
            bot_reply = get_suspicious_response()
        bot_reply += f" (Score: {result['score']}, Reason: {', '.join(result['reasons'])})"
    else:
        bot_reply = "I can check URLs or chat with you. Try sending a link!"

    chat_history[user_id].append({"role": "bot", "text": bot_reply})

    return jsonify({"response": bot_reply})

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
