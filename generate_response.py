# generate_response.py
import re
from feature_extractor import extract_features
from response import get_safe_response, get_suspicious_response
from url_checker import score_url

def preprocess_text(text: str):
    """Clean and tokenize text input"""
    if not text:
        return []
    text = text.replace("\u00A0", " ").strip().lower()
    tokens = re.findall(r"\w+", text)
    return tokens

def generate_response(user_input: str, chat_history: list) -> str:
    """
    Generate a response to the user input.
    If a URL is detected, score it and provide detailed feedback.
    Otherwise, return a default conversational message.
    """
    cleaned_tokens = preprocess_text(user_input)
    cleaned_input = " ".join(cleaned_tokens)

    # Detect URLs
    urls = re.findall(
        r"(https?://[^\s]+|www\.[^\s]+|\b[a-zA-Z0-9\-.]+\.[a-z]{2,}\b)",
        cleaned_input
    )

    if urls:
        url = urls[0]
        if not url.startswith("http"):
            url = "http://" + url  # Assume HTTP if scheme missing
        result = score_url(url)
        score = result.get("score", 0)
        label = result.get("label", "unknown")
        reasons = result.get("reasons", ["No reason provided"])

        # Feature extraction (optional, for ML or logging)
        features = extract_features(url)

        if label == "dangerous":
            return (
                f"❌ Warning! The URL '{url}' is classified as dangerous (score: {score}/100).\n"
                f"Reasons: {', '.join(reasons)}.\n"
                f"Feature summary: {features}\n"
                "Please avoid visiting this site to stay safe online!"
            )
        elif label == "suspicious":
            return (
                f"⚠ Attention! The URL '{url}' appears suspicious (score: {score}/100).\n"
                f"Reasons: {', '.join(reasons)}.\n"
                f"Feature summary: {features}\n"
                "Proceed with caution if you decide to visit this site."
            )
        else:
            return (
                f"✅ Good news! The URL '{url}' looks safe (score: {score}/100).\n"
                f"{get_safe_response()}\n"
                f"Feature summary: {features}\n"
                "You can visit this site confidently."
            )

    # Default conversational response
    return (
        "🤖 I’m here to help you detect suspicious URLs and keep you safe online. "
        "You can send me a link like 'https://example.com', and I’ll analyze it for you. "
        "If you want, I can also give tips on staying secure on the web!"
    )
