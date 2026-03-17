import re
import nltk

nltk.download("wordnet")
nltk.download("omw-1.4")


def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation & special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return text