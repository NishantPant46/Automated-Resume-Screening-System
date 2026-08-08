import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("training/dataset.csv")

# ----------------------------
# Use Processed Resume Text
# ----------------------------
texts = df["processed_text"].fillna("")

# ----------------------------
# Create TF-IDF Vectorizer
# ----------------------------
vectorizer = TfidfVectorizer(

    max_features=5000,

    ngram_range=(1,2)

)

# ----------------------------
# Convert Text → Numerical Features
# ----------------------------
X = vectorizer.fit_transform(texts)

print("TF-IDF Matrix Shape:")

print(X.shape)

# ----------------------------
# Save Vectorizer
# ----------------------------
joblib.dump(

    vectorizer,

    "training/vectorizer.pkl"

)

print("Vectorizer saved successfully!")