# test_spacy.py
import spacy

def test_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("❌ SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
        return

    sentence = "Hello Jay, GreatWall chatbot is ready to fight fraud!"
    doc = nlp(sentence)
    for token in doc:
        print(f"{token.text} -> {token.pos_}")

if __name__ == "__main__":
    test_spacy_model()
