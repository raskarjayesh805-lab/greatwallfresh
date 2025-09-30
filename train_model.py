# train_model_sklearn.py
import joblib
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Whitelist of official safe sites
WHITELIST_SAFE = [
    "googlepay.com", "phonepe.com", "paytm.com", "paypal.com",
    "razorpay.com", "bhimupi.gov.in"
]

# -----------------------------
# Sample dataset
urls = [
    # Official payment sites
    "https://googlepay.com",
    "https://phonepe.com",
    "https://paytm.com",
    "https://paypal.com",
    "https://razorpay.com",
    # Government sites
    "https://india.gov.in",
    "https://bhimupi.gov.in",
    # Phishing / suspicious
    "http://login-paypal.com",
    "http://paytm-login.com",
    "http://google-pay.com",
    "http://fakebank-secure.com",
    "http://scam-example.com",
    # Random HTTPS sites (to be suspicious)
    "https://example.com",
    "https://myblog.net",
    "https://techsite.org",
]

# Labels: 0 = safe, 1 = suspicious/dangerous
labels = [
    0, 0, 0, 0, 0,    # Official payment
    0, 0,              # Government
    1, 1, 1, 1, 1,    # Phishing
    1, 1, 1            # Other HTTPS unknown
]

# -----------------------------
# Feature extraction
def extract_features(url: str) -> dict:
    url_lower = url.lower()
    domain = re.sub(r"https?://(www\.)?", "", url_lower).split("/")[0]

    features = {
        "url_length": len(url),
        "hostname_length": len(urlparse(url).netloc),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r'\W', url)),
        "num_subdomains": url_lower.count('.') - 1,
        "num_hyphens": url_lower.count('-'),
        "is_https": int(url_lower.startswith("https://")),
    }

    # Simple token counts
    tokens = re.findall(r'\w+', domain)
    features['num_tokens'] = len(tokens)
    features['token_length_sum'] = sum(len(t) for t in tokens)

    return features

# -----------------------------
# Prepare dataset
X = [list(extract_features(url).values()) for url in urls]
y = labels

# -----------------------------
# Train RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# -----------------------------
# Save the model
joblib.dump(clf, "model/url_rf_model.joblib")
print("✅ Model trained and saved!")

# Save whitelist separately
joblib.dump(WHITELIST_SAFE, "model/url_whitelist.joblib")
print("✅ Whitelist saved!")
