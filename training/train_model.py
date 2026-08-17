import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from app.services.nlp_service import preprocess_text


# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("training/resume_dataset_3000.csv")

print("Dataset Shape:", df.shape)
print("Columns:", list(df.columns))


# ----------------------------
# Remove Missing Values
# ----------------------------

df = df.dropna(
    subset=["resume_text", "job_role"]
)

print("Samples after cleaning:", len(df))


# ----------------------------
# NLP Preprocessing
# ----------------------------

print("\nPreprocessing resumes...")

df["processed_text"] = df["resume_text"].apply(
    preprocess_text
)


# ----------------------------
# Input and Labels
# ----------------------------

X = df["processed_text"]

y = df["job_role"]


print("\nNumber of Job Categories:", y.nunique())
print("\nJob Categories:")
print(y.value_counts())


# ----------------------------
# Train/Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))


# ----------------------------
# TF-IDF Vectorization
# ----------------------------

print("\nPerforming TF-IDF Vectorization...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_vectorized = vectorizer.fit_transform(X_train)

X_test_vectorized = vectorizer.transform(X_test)

print("Training TF-IDF Shape:",
      X_train_vectorized.shape)

print("Testing TF-IDF Shape:",
      X_test_vectorized.shape)


# ----------------------------
# Logistic Regression
# ----------------------------

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

model.fit(
    X_train_vectorized,
    y_train
)

print("Model training completed!")


# ----------------------------
# Prediction
# ----------------------------

y_pred = model.predict(
    X_test_vectorized
)


# ----------------------------
# Model Evaluation
# ----------------------------

print("\n============================")
print("MODEL EVALUATION")
print("============================")

print("\nAccuracy:")
print(
    accuracy_score(
        y_test,
        y_pred
    )
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

# ----------------------------
# Confusion Matrix
# ----------------------------

print("\nConfusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# ----------------------------
# Save Confusion Matrix Figure
# ----------------------------

plt.figure(
    figsize=(20, 18)
)

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.xlabel("Predicted Category")
plt.ylabel("Actual Category")

plt.title(
    "Confusion Matrix - Resume Classification"
)

plt.xticks(
    rotation=90,
    fontsize=8
)

plt.yticks(
    rotation=0,
    fontsize=8
)

plt.tight_layout()

plt.savefig(
    "training/confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\nConfusion Matrix saved as:"
)

print(
    "training/confusion_matrix.png"
)


# ----------------------------
# Save Model
# ----------------------------

joblib.dump(
    model,
    "training/model.pkl"
)


# ----------------------------
# Save TF-IDF Vectorizer
# ----------------------------

joblib.dump(
    vectorizer,
    "training/vectorizer.pkl"
)


print("\n============================")
print("FILES SAVED")
print("============================")

print("Model saved as:")
print("training/model.pkl")

print("Vectorizer saved as:")
print("training/vectorizer.pkl")