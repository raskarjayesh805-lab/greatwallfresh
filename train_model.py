# train_model_sklearn.py
import joblib
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from feature_extractor import extract_features

# -----------------------------
# Whitelist of official safe sites
# -----------------------------
WHITELIST_SAFE = [
    "googlepay.com", "phonepe.com", "paytm.com", "paypal.com",
    "razorpay.com", "bhimupi.gov.in"
]

# -----------------------------
# Sample dataset
# -----------------------------
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
# Add 500 dummy URLs (250 safe, 250 suspicious)
# -----------------------------
for i in range(1, 251):
    urls.append(f"https://secure-site{i}.com")
    labels.append(0)

for i in range(1, 251):
    if i % 5 == 0:
        urls.append(f"http://login-secure{i}.info")
    elif i % 5 == 1:
        urls.append(f"http://verify-account{i}.net")
    elif i % 5 == 2:
        urls.append(f"http://paypal-secure{i}.xyz")
    elif i % 5 == 3:
        urls.append(f"http://bank-verify{i}.site")
    else:
        urls.append(f"http://free-gift{i}.ru")
    labels.append(1)

# -----------------------------
# Rule: http:// is always unsafe
def is_http_unsafe(url: str) -> bool:
    return url.lower().startswith("http://")

# -----------------------------
# Prepare dataset
X, y = [], []
for url, label in zip(urls, labels):
    # Force http URLs as unsafe
    y.append(1 if is_http_unsafe(url) else label)
    features = extract_features(url)
    X.append(list(features.values()))

# -----------------------------
# Train RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# -----------------------------
# Save the model and whitelist
joblib.dump(clf, "model/url_rf_model.joblib")
joblib.dump(WHITELIST_SAFE, "model/url_whitelist.joblib")
print("✅ Model trained and saved!")
print("✅ Whitelist saved!")

# -----------------------------
# Example runtime check
def check_url_runtime(url: str):
    if is_http_unsafe(url):
        return f"⚠️ The URL '{url}' is unsafe because it uses HTTP (not HTTPS)."
    features = [list(extract_features(url).values())]
    prediction = clf.predict(features)[0]
    return f"✅ The URL '{url}' looks safe." if prediction == 0 else f"🚨 Warning! The URL '{url}' looks suspicious."

# Test examples
if __name__ == "__main__":
    test_urls = [
        "http://fakebank.com",
        "https://googlepay.com",
        "https://unknown-site123.net"
    ]
    for t in test_urls:
        print(t, "->", check_url_runtime(t))
