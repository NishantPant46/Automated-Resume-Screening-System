import joblib

from app.services.nlp_service import preprocess_text


# Load trained model
model = joblib.load("training/model.pkl")

# Load TF-IDF vectorizer
vectorizer = joblib.load("training/vectorizer.pkl")


# --------------------------------
# New Resume for Testing
# --------------------------------

resume = """
John is a Python developer with strong experience in
Python, Django, Flask, REST API development and SQL.

He has developed backend web applications using Django
and Flask. He has experience working with databases,
APIs and server-side programming.
"""


# --------------------------------
# NLP Preprocessing
# --------------------------------

processed_text = preprocess_text(resume)

print("Processed Resume:")
print(processed_text)


# --------------------------------
# TF-IDF Transformation
# --------------------------------

resume_vector = vectorizer.transform(
    [processed_text]
)


print("\nTF-IDF Vector Shape:")
print(resume_vector.shape)


# --------------------------------
# Prediction
# --------------------------------

prediction = model.predict(
    resume_vector
)


print("\nPredicted Job Role:")
print(prediction[0])


# --------------------------------
# Prediction Probabilities
# --------------------------------

probabilities = model.predict_proba(
    resume_vector
)

classes = model.classes_


results = sorted(
    zip(classes, probabilities[0]),
    key=lambda x: x[1],
    reverse=True
)


print("\nTop 5 Predictions:")

for role, probability in results[:5]:

    print(
        f"{role}: {probability * 100:.2f}%"
    )