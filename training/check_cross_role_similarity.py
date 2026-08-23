import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    "training/resume_dataset_3000.csv"
)

df = df.dropna(
    subset=["resume_text", "job_role"]
).reset_index(drop=True)


# ============================================================
# SAMPLE DATA
# ============================================================

sample = df.sample(
    min(1000, len(df)),
    random_state=42
).reset_index(drop=True)


# ============================================================
# TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X = vectorizer.fit_transform(
    sample["resume_text"]
)


# ============================================================
# COSINE SIMILARITY
# ============================================================

similarity = cosine_similarity(X)


# ============================================================
# FIND CROSS-ROLE HIGH SIMILARITY
# ============================================================

pairs = []

for i in range(len(similarity)):

    for j in range(i + 1, len(similarity)):

        # Only consider different job roles
        if (
            sample.iloc[i]["job_role"]
            !=
            sample.iloc[j]["job_role"]
        ):

            score = similarity[i, j]

            if score >= 0.80:

                pairs.append({

                    "similarity": score,

                    "role_1":
                        sample.iloc[i]["job_role"],

                    "role_2":
                        sample.iloc[j]["job_role"]

                })


# ============================================================
# SORT
# ============================================================

pairs = sorted(
    pairs,
    key=lambda x: x["similarity"],
    reverse=True
)


# ============================================================
# RESULTS
# ============================================================

print("\n========================================")
print("CROSS-ROLE SIMILARITY ANALYSIS")
print("========================================")

print(
    "\nNumber of cross-role pairs with similarity >= 0.80:",
    len(pairs)
)


print(
    "\nTop 30 cross-role similar pairs:"
)


for pair in pairs[:30]:

    print(
        "Similarity:",
        round(pair["similarity"], 4),
        "|",
        pair["role_1"],
        "|",
        pair["role_2"]
    )


if len(pairs) == 0:

    print(
        "\nNo highly similar cross-role resumes were found."
    )