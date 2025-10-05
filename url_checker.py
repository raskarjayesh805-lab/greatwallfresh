# url_checker.py
import re

def score_url(url: str) -> dict:
    """
    Score a URL for safety.
    Returns a dict with score, label, and reasons.
    """
    score = 100
    reasons = []
    url_lower = url.lower()

    # Suspicious keywords commonly found in phishing URLs
    suspicious_keywords = ["login", "verify", "update", "secure", "bank", "paypal", "account", "free", "gift"]
    if any(word in url_lower for word in suspicious_keywords):
        score -= 30
        reasons.append("Contains suspicious keyword(s)")

    # Penalize HTTP (not HTTPS)
    if url_lower.startswith("http://"):
        score -= 50
        reasons.append("Uses HTTP instead of HTTPS (insecure connection)")

    # Penalize very long URLs
    if len(url) > 75:
        score -= 10
        reasons.append("URL is unusually long")

    # Clamp score between 0 and 100
    score = max(0, min(100, score))

    # Determine label
    if score < 40:
        label = "dangerous"
    elif score < 70:
        label = "suspicious"
    else:
        label = "safe"

    if not reasons:
        reasons.append("No obvious red flags detected")

    return {"score": score, "label": label, "reasons": reasons}
