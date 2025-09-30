# response.py
import random

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

def get_greeting_response() -> str:
    return random.choice(GREETING_RESPONSES)

def get_safe_response() -> str:
    return random.choice(SAFE_RESPONSES)

def get_suspicious_response() -> str:
    return random.choice(SUSPICIOUS_RESPONSES)
