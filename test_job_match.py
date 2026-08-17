from app.services.job_match_service import (
    calculate_similarity,
    calculate_semantic_similarity,
    calculate_skill_match,
    calculate_experience_match,
    get_skill_details
)


resume = """
Python Developer

Professional Summary:
Python developer with 3 years of experience developing backend web applications.

Skills:
Python, Django, Flask, REST API, SQL, Git

Experience:
3 years of professional experience developing backend applications
using Python, Django and Flask.

Developed REST APIs and worked with SQL databases.
Used Git for version control.
"""


job_description = """
We are looking for a Python Developer to develop backend web applications.
The candidate should have experience with Python, Django, Flask,
REST APIs, SQL databases and Git.
"""


job_skills = """
Python, Django, Flask, REST API, SQL, Git
"""


required_experience = 3


# ----------------------------------------
# Calculate Scores
# ----------------------------------------

tfidf_score = calculate_similarity(
    resume,
    job_description
)

semantic_score = calculate_semantic_similarity(
    resume,
    job_description
)

skill_score = calculate_skill_match(
    resume,
    job_skills
)

experience_score = calculate_experience_match(
    resume,
    required_experience
)


# ----------------------------------------
# Skill Details
# ----------------------------------------

skill_details = get_skill_details(
    resume,
    job_skills
)


# ----------------------------------------
# Final Score
# ----------------------------------------

final_score = (
    (tfidf_score * 0.20)
    + (semantic_score * 0.30)
    + (skill_score * 0.30)
    + (experience_score * 0.20)
)


# ----------------------------------------
# Display Result
# ----------------------------------------

print("\n========================================")
print("RESUME JOB MATCH ANALYSIS")
print("========================================")

print("\nRequired Skills:")
print(skill_details["matched_skills"] + skill_details["missing_skills"])

print("\nMatched Skills:")
print(skill_details["matched_skills"])

print("\nMissing Skills:")
print(skill_details["missing_skills"])

print("\nSkill Match:", skill_score, "%")

print("\n========================================")

print("TF-IDF Similarity       :", tfidf_score, "%")
print("Semantic Similarity     :", round(semantic_score, 2), "%")
print("Skill Match             :", skill_score, "%")
print("Experience Match        :", experience_score, "%")

print("----------------------------------------")

print("Final Match Score       :", round(final_score, 2), "%")

print("========================================")