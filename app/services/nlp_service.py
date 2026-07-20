import spacy
import nltk

from nltk.corpus import stopwords

# Download stopwords once
nltk.download("stopwords")

# Load English model
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words("english"))


def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Process using spaCy
    doc = nlp(text)

    cleaned_words = []

    for token in doc:

        # Skip punctuation, spaces and stopwords
        if (
            token.is_punct
            or token.is_space
            or token.text in stop_words
        ):
            continue

        # Keep lemma (root word)
        cleaned_words.append(token.lemma_)

    return " ".join(cleaned_words)