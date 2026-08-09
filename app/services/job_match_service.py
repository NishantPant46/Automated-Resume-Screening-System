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

    return round(
        similarity_percentage,
        2
    )


# ---------------------------------------------
# Semantic Similarity
# ---------------------------------------------

def calculate_semantic_similarity(resume_text, job_text):
    """
    Calculate semantic similarity between resume
    and job description using Sentence Transformers.
    """

    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    if not resume_text or not job_text:
        return 0.0

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    resume_embedding = model.encode(
        resume_text
    )

    job_embedding = model.encode(
        job_text
    )

    similarity = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )[0][0]

    similarity_percentage = similarity * 100

    return round(
        similarity_percentage,
        2
    )


# ---------------------------------------------
# Extract Experience
# ---------------------------------------------

def extract_experience(text):
    """
    Extract years of professional experience
    from resume text.
    """

    if not text:
        return 0.0

    text = text.lower()

    patterns = [
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience',
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+experience',
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+professional\s+experience',
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+working\s+experience',
        r'worked\s+for\s+(\d+(?:\.\d+)?)\+?\s*years?',
        r'worked\s+as\s+.*?\s+for\s+(\d+(?:\.\d+)?)\+?\s*years?',
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+working',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return float(match.group(1))

    return 0.0


# ---------------------------------------------
# Calculate Experience Match
# ---------------------------------------------

def calculate_experience_match(
    resume_text,
    required_experience
):
    """
    Calculate experience match percentage.

    Rules:
    - No experience requirement -> 100%
    - Candidate meets/exceeds requirement -> 100%
    - Candidate has less experience -> proportional score
    - No candidate experience -> 0%
    """

    candidate_experience = extract_experience(
        resume_text
    )

    # Handle empty or missing job requirement
    if required_experience is None:
        return 100.0

    if str(required_experience).strip() == "":
        return 100.0

    try:
        required_experience = float(
            required_experience
        )
    except (TypeError, ValueError):
        return 100.0

    # Job does not require experience
    if required_experience <= 0:
        return 100.0

    # Candidate has no detected experience
    if candidate_experience <= 0:
        return 0.0

    # Candidate meets or exceeds requirement
    if candidate_experience >= required_experience:
        return 100.0

    # Candidate has partial experience
    experience_score = (
        candidate_experience
        / required_experience
    ) * 100

    return round(
        experience_score,
        2
    )

# ---------------------------------------------
# Skill Normalization
# ---------------------------------------------

def normalize_skill(skill):
    """
    Convert skill names and aliases into
    a standard skill name.
    """

    skill = skill.lower().strip()

    aliases = {
        "mysql": "sql",
        "postgresql": "sql",
        "postgres": "sql",
        "mssql": "sql",
        "sql server": "sql",

        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",

        "github": "git",
        "gitlab": "git",
        "bitbucket": "git",

        "node": "node.js",
        "nodejs": "node.js",

        "machine-learning": "machine learning",
        "deep-learning": "deep learning",

        "ai": "artificial intelligence",

        "cisco networking": "cisco",
        "tcp/ip": "tcp ip"
    }

    return aliases.get(skill, skill)

# ---------------------------------------------
# Extract Skills
# ---------------------------------------------

def extract_skills(text):
    """
    Extract technical skills from text and
    normalize skill aliases.
    """

    if not text:
        return set()

    skill_list = {
        "machine learning",
        "deep learning",
        "artificial intelligence",

        "rest api",
        "rest apis",
        "restful api",
        "restful apis",

        "sql server",
        "postgresql",
        "mysql",
        "mssql",

        "node.js",
        "nodejs",

        "network security",
        "tcp ip",
        "tcp/ip",

        "python",
        "javascript",
        "java",
        "c++",
        "c#",
        "c",

        "flask",
        "django",

        "react",
        "angular",
        "vue",

        "html",
        "css",

        "mongodb",

        "tensorflow",
        "pytorch",

        "git",
        "github",
        "gitlab",
        "bitbucket",

        "docker",
        "aws",
        "azure",
        "linux",

        "api",

        "bootstrap",
        "figma",
        "adobe xd",
        "photoshop",
        "illustrator",
        "cisco"
    }

    text = text.lower()

    found_skills = set()

    # First detect specific skills such as
    # "rest api" before generic "api".
    if re.search(r"\brest\s+apis?\b", text):
        found_skills.add("rest api")

    elif re.search(r"\brestful\s+apis?\b", text):
        found_skills.add("rest api")

    # Detect remaining skills
    for skill in skill_list:

        # Skip generic API because REST API
        # already represents API knowledge.
        if skill == "api":
            continue

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            normalized = normalize_skill(skill)

            found_skills.add(normalized)

    return found_skills


# ---------------------------------------------
# Get Skill Details
# ---------------------------------------------

def get_skill_details(resume_text, job_skills):
    """
    Return matched and missing skills.
    """

    resume_skills = extract_skills(resume_text)

    required_skills = extract_skills(job_skills)

    matched_skills = resume_skills.intersection(
        required_skills
    )

    missing_skills = required_skills.difference(
        resume_skills
    )

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }




# ---------------------------------------------
# Calculate Skill Match
# ---------------------------------------------

def calculate_skill_match(resume_text, job_skills):
    """
    Calculate the percentage of required job skills
    found in the resume after normalization.
    """

    resume_skills = extract_skills(resume_text)

    required_skills = extract_skills(job_skills)

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
# Final Resume-Job Score
# ---------------------------------------------

def calculate_final_score(
    resume_text,
    extracted_resume_text,
    job_description,
    job_skills,
    required_experience
):
    """
    Calculate the final resume-job matching score.

    Scoring:
    TF-IDF similarity = 20%
    Semantic similarity = 30%
    Skill matching = 30%
    Experience matching = 20%
    """

    # TF-IDF similarity
    tfidf_score = calculate_similarity(
        resume_text,
        job_description
    )

    # Semantic similarity
    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    # Skill matching
    skill_score = calculate_skill_match(
        resume_text,
        job_skills
    )

    # Experience matching
    experience_score = calculate_experience_match(
        extracted_resume_text,
        required_experience
    )

    # Final weighted score
    final_score = (
        (tfidf_score * 0.20)
        + (semantic_score * 0.30)
        + (skill_score * 0.30)
        + (experience_score * 0.20)
    )

    return round(final_score, 2)

# ---------------------------------------------
# Match Status
# ---------------------------------------------

def get_match_status(score):
    """
    Determine candidate match status
    based on final matching score.
    """

    if score >= 70:
        return "Excellent Match"

    elif score >= 50:
        return "Good Match"

    elif score >= 30:
        return "Moderate Match"

    else:
        return "Low Match"


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

    job = Job.query.get_or_404(job_id)

    resumes = Resume.query.all()

    results = []

    for resume in resumes:

        if not resume.processed_text:
            continue

        final_score = calculate_final_score(
            resume.processed_text,
            resume.extracted_text,
            job.description,
            job.skills,
            job.experience
        )

        match = save_job_match(
            resume.id,
            job.id,
            final_score
        )

        results.append(match)

    return results


# ---------------------------------------------
# Get Selection Status
# ---------------------------------------------

def get_selection_status(score):
    """
    Determine whether a candidate should be selected.

    Selection rules:
    70% - 100% -> Selected
    50% - 69%  -> Selected
    30% - 49%  -> Not Selected
    0%  - 29%  -> Not Selected
    """

    if score >= 50:
        return "Selected"

    return "Not Selected"