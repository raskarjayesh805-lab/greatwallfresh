# feature_extractor.py
import re
from urllib.parse import urlparse

def preprocess_text(text: str):
    """Simple tokenizer / cleaner for URL or text"""
    if not text:
        return []
    text = text.replace("\u00A0", " ").strip().lower()
    tokens = re.findall(r"\w+", text)
    return tokens

def extract_features(url: str) -> dict:
    """
    Extract features from a URL for ML or rule-based scoring.
    Includes token count, URL length, subdomains, HTTPS, etc.
    """
    parsed = urlparse(url)
    hostname = parsed.netloc

    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r'\W', url)),
        "num_subdomains": hostname.count('.') if hostname else 0,
        "num_hyphens": url.count('-'),
        "has_https": 1 if parsed.scheme == 'https' else 0
    }

    tokens = preprocess_text(url)
    features["num_tokens"] = len(tokens)
    features["clean_text_length"] = len(" ".join(tokens))

    return features
