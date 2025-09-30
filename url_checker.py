import re

def score_url(url: str) -> dict:
    score = 100
    reasons = []
    url_lower = url.lower()

    suspicious_keywords = ["login", "verify", "update", "secure", "bank", "paypal"]
    if any(word in url_lower for word in suspicious_keywords):
        score -= 30
        reasons.append("Contains suspicious keyword")

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
