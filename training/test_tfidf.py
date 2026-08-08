import joblib
from app.services.nlp_service import preprocess_text

# Load saved TF-IDF vectorizer
vectorizer = joblib.load("training/vectorizer.pkl")

# Sample resume text
resume = """
Python
Flask
Machine Learning
SQL
NLP
"""

# Preprocess
processed = preprocess_text(resume)

# Transform into TF-IDF vector
vector = vectorizer.transform([processed])

# Print vector size
print("Vector Shape:", vector.shape)

# Print non-zero TF-IDF values
feature_names = vectorizer.get_feature_names_out()

print("\nImportant Features:\n")

for index, value in zip(vector.indices, vector.data):
    print(f"{feature_names[index]} : {value:.4f}")