from app.services.nlp_service import preprocess_text

text = """
John has worked as a Python Developer for five years.
He has experience in Flask, SQL and Machine Learning.
"""

print(preprocess_text(text))