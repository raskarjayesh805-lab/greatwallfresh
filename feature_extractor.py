# feature_extractor.py
import re
from urllib.parse import urlparse
from nlp_utils import preprocess_text

def extract_features(url: str) -> dict:
    parsed = urlparse(url)
    hostname = parsed.netloc

    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r'\W', url)),
        "num_subdomains": hostname.count('.') if hostname else 0,
        "has_https": 1 if parsed.scheme == 'https' else 0
    }

    tokens = preprocess_text(url)
    features["num_tokens"] = len(tokens)
    features["clean_text_length"] = len(" ".join(tokens))

    return features
