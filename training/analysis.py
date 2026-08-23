import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split, learning_curve
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from app.services.nlp_service import preprocess_text


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    "training/resume_dataset_3000.csv"
)

print("Dataset Shape:", df.shape)

df = df.dropna(
    subset=["resume_text", "job_role"]
)

print("Samples after cleaning:", len(df))


# ============================================================
# PREPROCESSING
# ============================================================

print("\nPreprocessing resumes...")

df["processed_text"] = df["resume_text"].apply(
    preprocess_text
)

X = df["processed_text"]

y = df["job_role"]


# ============================================================
# GRAPH 1
# TRAINING DATASET DISTRIBUTION
# ============================================================

print("\nGenerating Graph 1: Dataset Distribution")

job_counts = y.value_counts().sort_index()

plt.figure(figsize=(16, 8))

plt.bar(
    job_counts.index,
    job_counts.values
)

plt.title(
    "Training Dataset Distribution by Job Role",
    fontsize=16
)

plt.xlabel(
    "Job Role"
)

plt.ylabel(
    "Number of Resumes"
)

plt.xticks(
    rotation=70,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "training/dataset_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: training/dataset_distribution.png"
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# GRAPH 2
# TRAINING VS TESTING DATASET DISTRIBUTION
# ============================================================

print("\nGenerating Graph 2: Training vs Testing Distribution")

dataset_names = [
    "Training",
    "Testing"
]

dataset_sizes = [
    len(X_train),
    len(X_test)
]

plt.figure(figsize=(8, 6))

plt.bar(
    dataset_names,
    dataset_sizes
)

plt.title(
    "Training and Testing Dataset Distribution",
    fontsize=16
)

plt.xlabel(
    "Dataset"
)

plt.ylabel(
    "Number of Samples"
)

plt.tight_layout()

plt.savefig(
    "training/training_testing_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: training/training_testing_distribution.png"
)


# ============================================================
# TF-IDF
# ============================================================

print("\nPerforming TF-IDF Vectorization...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_vectorized = vectorizer.fit_transform(
    X_train
)

X_test_vectorized = vectorizer.transform(
    X_test
)


# ============================================================
# TRAIN YOUR ACTUAL MODEL
# ============================================================

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


# ============================================================
# PREDICTIONS
# ============================================================

train_prediction = model.predict(
    X_train_vectorized
)

test_prediction = model.predict(
    X_test_vectorized
)


# ============================================================
# CALCULATE TRAINING PERFORMANCE
# ============================================================

training_accuracy = accuracy_score(
    y_train,
    train_prediction
) * 100

training_precision = precision_score(
    y_train,
    train_prediction,
    average="weighted",
    zero_division=0
) * 100

training_recall = recall_score(
    y_train,
    train_prediction,
    average="weighted",
    zero_division=0
) * 100

training_f1 = f1_score(
    y_train,
    train_prediction,
    average="weighted",
    zero_division=0
) * 100


# ============================================================
# CALCULATE TESTING PERFORMANCE
# ============================================================

testing_accuracy = accuracy_score(
    y_test,
    test_prediction
) * 100

testing_precision = precision_score(
    y_test,
    test_prediction,
    average="weighted",
    zero_division=0
) * 100

testing_recall = recall_score(
    y_test,
    test_prediction,
    average="weighted",
    zero_division=0
) * 100

testing_f1 = f1_score(
    y_test,
    test_prediction,
    average="weighted",
    zero_division=0
) * 100


print("\n================================")
print("TRAINING PERFORMANCE")
print("================================")

print(
    "Accuracy:",
    round(training_accuracy, 2),
    "%"
)

print(
    "Precision:",
    round(training_precision, 2),
    "%"
)

print(
    "Recall:",
    round(training_recall, 2),
    "%"
)

print(
    "F1 Score:",
    round(training_f1, 2),
    "%"
)


print("\n================================")
print("TESTING PERFORMANCE")
print("================================")

print(
    "Accuracy:",
    round(testing_accuracy, 2),
    "%"
)

print(
    "Precision:",
    round(testing_precision, 2),
    "%"
)

print(
    "Recall:",
    round(testing_recall, 2),
    "%"
)

print(
    "F1 Score:",
    round(testing_f1, 2),
    "%"
)


# ============================================================
# GRAPH 3
# TRAINING VS TESTING PERFORMANCE
# ============================================================

print(
    "\nGenerating Graph 3: Training vs Testing Performance"
)

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score"
]

training_scores = [
    training_accuracy,
    training_precision,
    training_recall,
    training_f1
]

testing_scores = [
    testing_accuracy,
    testing_precision,
    testing_recall,
    testing_f1
]

x = np.arange(
    len(metrics)
)

width = 0.35

plt.figure(figsize=(10, 6))

plt.bar(
    x - width / 2,
    training_scores,
    width,
    label="Training"
)

plt.bar(
    x + width / 2,
    testing_scores,
    width,
    label="Testing"
)

plt.xticks(
    x,
    metrics
)

plt.xlabel(
    "Evaluation Metric"
)

plt.ylabel(
    "Performance (%)"
)

plt.title(
    "Training vs Testing Performance",
    fontsize=16
)

plt.ylim(
    0,
    105
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "training/training_testing_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: training/training_testing_performance.png"
)


# ============================================================
# GRAPH 4
# LEARNING CURVE
# ============================================================

print(
    "\nGenerating Graph 4: Learning Curve"
)

learning_model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

train_sizes, train_scores, validation_scores = learning_curve(

    learning_model,

    X_train_vectorized,

    y_train,

    cv=5,

    scoring="accuracy",

    train_sizes=np.linspace(
        0.1,
        1.0,
        5
    ),

    n_jobs=-1
)


train_mean = (
    train_scores.mean(axis=1) * 100
)

train_std = (
    train_scores.std(axis=1) * 100
)

validation_mean = (
    validation_scores.mean(axis=1) * 100
)

validation_std = (
    validation_scores.std(axis=1) * 100
)


plt.figure(figsize=(10, 6))

plt.plot(
    train_sizes,
    train_mean,
    marker="o",
    label="Training Accuracy"
)

plt.plot(
    train_sizes,
    validation_mean,
    marker="o",
    label="Validation Accuracy"
)

plt.fill_between(
    train_sizes,
    train_mean - train_std,
    train_mean + train_std,
    alpha=0.15
)

plt.fill_between(
    train_sizes,
    validation_mean - validation_std,
    validation_mean + validation_std,
    alpha=0.15
)

plt.xlabel(
    "Number of Training Samples"
)

plt.ylabel(
    "Accuracy (%)"
)

plt.title(
    "Learning Curve - TF-IDF + Logistic Regression",
    fontsize=16
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "training/learning_curve.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: training/learning_curve.png"
)


# ============================================================
# GRAPH 5
# MATCHING COMPONENT WEIGHTS
# ============================================================

print(
    "\nGenerating Graph 5: Matching Component Weights"
)

components = [
    "TF-IDF Similarity",
    "Semantic Similarity",
    "Skill Matching",
    "Experience Matching"
]

weights = [
    15,
    25,
    40,
    20
]

plt.figure(figsize=(10, 6))

plt.bar(
    components,
    weights
)

plt.title(
    "Resume-Job Matching Component Weights",
    fontsize=16
)

plt.xlabel(
    "Matching Component"
)

plt.ylabel(
    "Weight (%)"
)

plt.ylim(
    0,
    50
)

plt.xticks(
    rotation=20
)

plt.tight_layout()

plt.savefig(
    "training/matching_component_weights.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: training/matching_component_weights.png"
)


# ============================================================
# OPTIONAL GRAPH 6
# MATCHING SCORE COMPONENT CONTRIBUTION
# ============================================================

print(
    "\nGenerating Graph 6: Matching Score Contribution"
)

contribution_labels = [
    "TF-IDF",
    "Semantic",
    "Skills",
    "Experience"
]

contribution_values = [
    15,
    25,
    40,
    20
]

plt.figure(figsize=(9, 6))

plt.pie(
    contribution_values,
    labels=contribution_labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Contribution of Matching Components"
)

plt.tight_layout()

plt.savefig(
    "training/matching_component_contribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: training/matching_component_contribution.png"
)


# ============================================================
# FINISHED
# ============================================================

print("\n============================================")
print("ALL ANALYSIS GRAPHS GENERATED SUCCESSFULLY")
print("============================================")

print("""
Generated files:

1. training/dataset_distribution.png
2. training/training_testing_distribution.png
3. training/training_testing_performance.png
4. training/learning_curve.png
5. training/matching_component_weights.png
6. training/matching_component_contribution.png

Your existing confusion matrix remains:

7. training/confusion_matrix.png
""")