import joblib

from app.services.nlp_service import preprocess_text

# ----------------------------
# Load Model
# ----------------------------
model = joblib.load("training/model.pkl")

# ----------------------------
# Load TF-IDF Vectorizer
# ----------------------------
vectorizer = joblib.load("training/vectorizer.pkl")


def predict_resume(resume_text):
    """
    Predict whether a resume is Selected or Rejected.
    """

    # NLP preprocessing
    processed_text = preprocess_text(resume_text)

    # Convert text into TF-IDF vector
    features = vectorizer.transform([processed_text])

    # Predict
    prediction = model.predict(features)[0]

    return prediction