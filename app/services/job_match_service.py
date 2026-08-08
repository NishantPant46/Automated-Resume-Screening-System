import re

from app import db
from app.models.job_match_model import JobMatch


# ---------------------------------------------
# TF-IDF Similarity
# ---------------------------------------------

def calculate_similarity(resume_text, job_text):
    """
    Calculate similarity between resume and job description
    using TF-IDF and cosine similarity.
    """

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    if not resume_text or not job_text:
        return 0.0

    documents = [
        resume_text.lower(),
        job_text.lower()
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    similarity_percentage = similarity * 100

    return round(similarity_percentage, 2)


# ---------------------------------------------
# Extract Skills
# ---------------------------------------------

def extract_skills(text):
    """
    Extract common technical skills from text.
    """

    if not text:
        return set()

    skill_list = {
        "python",
        "java",
        "c",
        "c++",
        "c#",
        "javascript",
        "html",
        "css",
        "react",
        "angular",
        "vue",
        "node.js",
        "flask",
        "django",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "tensorflow",
        "pytorch",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "linux",
        "rest api",
        "api",
        "bootstrap",
        "figma",
        "adobe xd",
        "photoshop",
        "illustrator",
        "cisco",
        "tcp ip",
        "network security"
    }

    text = text.lower()

    found_skills = set()

    for skill in skill_list:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills


# ---------------------------------------------
# Skill Matching
# ---------------------------------------------

def calculate_skill_match(resume_text, job_skills):
    """
    Calculate percentage of required job skills
    found in the resume.
    """

    resume_skills = extract_skills(
        resume_text
    )

    required_skills = extract_skills(
        job_skills
    )

    if not required_skills:
        return 0.0

    matched_skills = resume_skills.intersection(
        required_skills
    )

    skill_score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return round(skill_score, 2)


# ---------------------------------------------
# Final Score
# ---------------------------------------------

def calculate_final_score(
    resume_text,
    job_description,
    job_skills
):
    """
    Calculate final resume-job matching score.

    TF-IDF similarity = 60%
    Skill matching = 40%
    """

    tfidf_score = calculate_similarity(
        resume_text,
        job_description
    )

    skill_score = calculate_skill_match(
        resume_text,
        job_skills
    )

    final_score = (
        (tfidf_score * 0.60)
        +
        (skill_score * 0.40)
    )

    return round(
        final_score,
        2
    )


# ---------------------------------------------
# Save Job Match
# ---------------------------------------------

def save_job_match(
    resume_id,
    job_id,
    similarity_score
):
    """
    Save a resume-job match.

    If the match already exists,
    update its score instead of creating
    a duplicate record.
    """

    existing_match = JobMatch.query.filter_by(
        resume_id=resume_id,
        job_id=job_id
    ).first()

    if existing_match:

        existing_match.similarity_score = (
            similarity_score
        )

        db.session.commit()

        return existing_match

    new_match = JobMatch(
        resume_id=resume_id,
        job_id=job_id,
        similarity_score=similarity_score
    )

    db.session.add(new_match)

    db.session.commit()

    return new_match


# ---------------------------------------------
# Get Matches For Resume
# ---------------------------------------------

def get_matches_for_resume(resume_id):
    """
    Get all job matches for a specific resume.
    """

    return JobMatch.query.filter_by(
        resume_id=resume_id
    ).order_by(
        JobMatch.similarity_score.desc()
    ).all()


# ---------------------------------------------
# Get Matches For Job
# ---------------------------------------------

def get_matches_for_job(job_id):
    """
    Get all resume matches for a specific job.
    """

    return JobMatch.query.filter_by(
        job_id=job_id
    ).order_by(
        JobMatch.similarity_score.desc()
    ).all()


# ---------------------------------------------
# Match All Resumes To Job
# ---------------------------------------------

def match_all_resumes_to_job(job_id):
    """
    Match all uploaded resumes against
    a specific job.
    """

    from app.models.job_model import Job
    from app.models.resume_model import Resume

    job = Job.query.get_or_404(
        job_id
    )

    resumes = Resume.query.all()

    results = []

    for resume in resumes:

        if not resume.processed_text:
            continue

        final_score = calculate_final_score(
            resume.processed_text,
            job.description,
            job.skills
        )

        match = save_job_match(
            resume.id,
            job.id,
            final_score
        )

        results.append(match)

    return results