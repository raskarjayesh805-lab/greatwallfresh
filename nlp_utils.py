import re
from url_checker import score_url
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def preprocess_text(text: str):
    if not text:
        return []
    text = text.replace("\u00A0", " ").strip().lower()
    tokens = re.findall(r"\w+", text)
    return tokens

def generate_response(user_input: str, chat_history: list) -> str:
    cleaned_tokens = preprocess_text(user_input)
    cleaned_input = " ".join(cleaned_tokens)

    urls = re.findall(
        r"(https?://[^\s]+|www\.[^\s]+|\b[a-zA-Z0-9\-.]+\.[a-z]{2,}\b)",
        cleaned_input
    )

    if urls:
        first = urls[0]
        if not first.startswith("http"):
            first = "http://" + first
        result = score_url(first)
        score = result.get("score", 0)
        label = result.get("label", "unknown")
        reasons = result.get("reasons", ["No reason provided"])
        if label == "dangerous":
            return f"❌ Dangerous site detected (score {score}/100). Reasons: {', '.join(reasons)}"
        elif label == "suspicious":
            return f"⚠ Suspicious site (score {score}/100). Reasons: {', '.join(reasons)}"
        else:
            return f"✅ Looks safe (score {score}/100). {reasons[0]}"

    # GPT placeholder
    return "🤖 GPT response placeholder"
