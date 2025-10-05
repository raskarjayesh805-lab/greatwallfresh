# response.py
import random

# -----------------------------
# Greeting messages
# -----------------------------
GREETINGS = ["hello", "hi", "hey", "hola", "greetings"]

GREETING_RESPONSES = [
    "Hey there! I'm GreatWall Chatbot 🛡. I'm here to help you identify safe and suspicious websites. Feel free to send me a URL to check!",
    "Hello! Ready to keep your online browsing safe? You can share any link, and I'll analyze it for you in detail.",
    "Hi! I'm your fraud detection assistant. I can tell you if a website is trustworthy or potentially risky. Send a URL to start.",
    "Hey! Let's make sure your online activities stay secure. I'm here to check links and provide guidance.",
    "Greetings! Want to stay safe online? Share a URL with me and I'll help determine its safety."
]

# -----------------------------
# Safe URL responses
# -----------------------------
SAFE_RESPONSES = [
    "This site looks completely safe ✅. You can browse without worry, but always stay cautious with unknown links.",
    "All clear! No immediate threats detected. Remember, staying alert online is always important.",
    "The link appears safe. Visiting it should not pose any risk. Keep practicing safe browsing habits!"
]

# -----------------------------
# Suspicious URL responses
# -----------------------------
SUSPICIOUS_RESPONSES = [
    "⚠ This URL looks suspicious. It may be trying to trick you into revealing personal info or credentials. Proceed with caution!",
    "Warning! This website may not be secure. Avoid entering sensitive information if you visit it.",
    "Hmm, this link could be unsafe. Always double-check such URLs before clicking or providing personal data."
]

# -----------------------------
# Get random response functions
# -----------------------------
def get_greeting_response() -> str:
    return random.choice(GREETING_RESPONSES)

def get_safe_response() -> str:
    return random.choice(SAFE_RESPONSES)

def get_suspicious_response() -> str:
    return random.choice(SUSPICIOUS_RESPONSES)
