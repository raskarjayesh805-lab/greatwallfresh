# test_spacy.py
import spacy

def test_spacy_model():
    """
    Test if the spaCy NLP model is loaded correctly.
    Prints tokens and their part-of-speech for a sample sentence.
    """
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("❌ SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
        return

    sample_sentence = "Hello Jay, GreatWall Chatbot is ready to fight fraud!"
    doc = nlp(sample_sentence)

    print("✅ SpaCy model loaded successfully!\n")
    print(f"Sample sentence: {sample_sentence}\n")
    print("Token analysis:")
    for token in doc:
        print(f"  {token.text:15} -> {token.pos_:10} (lemma: {token.lemma_})")

if __name__ == "__main__":
    test_spacy_model()
