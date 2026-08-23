import re

from app import db
from app.models.job_match_model import JobMatch
from app.models.selected_candidate_model import SelectedCandidate
from datetime import datetime

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
# Extract Experience From Job Entries
# ---------------------------------------------

def extract_job_entry_experience(text):
    """
    Extract experience from job-entry formats such as:

    Senior Data Scientist — Google Brain | 5+ Years
    Data Scientist — Netflix | 3 Years
    Python Developer | 2+ Years

    Returns total years found in job-entry patterns.
    """

    if not text:
        return 0.0

    text = text.lower()

    total_years = 0.0

    # -----------------------------------------
    # Pattern:
    # | 5+ Years
    # | 3 Years
    # -----------------------------------------

    pattern = re.compile(
        r'\|\s*(\d+(?:\.\d+)?)\+?\s*years?'
    )

    matches = pattern.findall(text)

    for value in matches:

        total_years += float(value)

    return round(
        total_years,
        2
    )





def extract_experience(text):
    """
    Extract total professional experience from a resume.

    Supports:
    - 5+ years of experience
    - 3 years experience
    - Jan 2021 - Dec 2025
    - June 2020 - August 2023
    - 2018 - 2020
    - March 2019 - Present
    - 2021 - Present

    Returns total experience in years.
    """

    if not text:
        return 0.0

    text = text.lower()

    import re
    from datetime import datetime

    # -------------------------------------------------
    # Month names
    # -------------------------------------------------

    months = {
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12
    }

    # -------------------------------------------------
    # Convert date to month number
    # -------------------------------------------------

    def convert_to_month(date_text):

        date_text = date_text.strip().lower()

        # Month + Year
        match = re.match(
            r"([a-z]+)\s+(\d{4})",
            date_text
        )

        if match:

            month_name = match.group(1)
            year = int(match.group(2))

            if month_name in months:

                month = months[month_name]

                return year * 12 + month

        # Year only
        match = re.match(
            r"(\d{4})",
            date_text
        )

        if match:

            year = int(match.group(1))

            # Assume January
            return year * 12 + 1

        return None

    # -------------------------------------------------
    # Current date
    # -------------------------------------------------

    now = datetime.now()

    current_month = (
        now.year * 12
        + now.month
    )

    # -------------------------------------------------
    # Find employment date ranges
    # -------------------------------------------------

    date_pattern = re.compile(
        r"""
        (?P<start>
            (?:jan(?:uary)?|
            feb(?:ruary)?|
            mar(?:ch)?|
            apr(?:il)?|
            may|
            jun(?:e)?|
            jul(?:y)?|
            aug(?:ust)?|
            sep(?:t(?:ember)?)?|
            oct(?:ober)?|
            nov(?:ember)?|
            dec(?:ember)?)?
            \s*
            \d{4}
        )
        \s*
        (?:-|–|—|to)
        \s*
        (?P<end>
            (?:
                (?:jan(?:uary)?|
                feb(?:ruary)?|
                mar(?:ch)?|
                apr(?:il)?|
                may|
                jun(?:e)?|
                jul(?:y)?|
                aug(?:ust)?|
                sep(?:t(?:ember)?)?|
                oct(?:ober)?|
                nov(?:ember)?|
                dec(?:ember)?)
                \s*
            )?
            (?:\d{4}|present|current)
        )
        """,
        re.VERBOSE | re.IGNORECASE
    )

    total_months = 0

    date_ranges_found = False

    for match in date_pattern.finditer(text):

        start_text = match.group("start").strip()
        end_text = match.group("end").strip()

        start_month = convert_to_month(
            start_text
        )

        # Present / Current
        if end_text in ["present", "current"]:

            end_month = current_month

        else:

            end_month = convert_to_month(
                end_text
            )

        if start_month is None:
            continue

        if end_month is None:
            continue

        # Prevent invalid ranges
        if end_month < start_month:
            continue

        duration = (
            end_month - start_month + 1
        )

        total_months += duration

        date_ranges_found = True

    # -------------------------------------------------
    # If date ranges were found
    # -------------------------------------------------

    if date_ranges_found:

        experience_years = (
            total_months / 12
        )

        return round(
            experience_years,
            1
        )

    # -------------------------------------------------
    # Fallback: Explicit experience statements
    # -------------------------------------------------

    patterns = [

        r'(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+professional\s+experience',

        r'(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience',

        r'(\d+(?:\.\d+)?)\+?\s*years?\s+experience',

        r'(\d+(?:\.\d+)?)\+?\s*years?\s+working\s+experience',

        r'worked\s+for\s+(\d+(?:\.\d+)?)\+?\s*years?',

        r'worked\s+as\s+.*?\s+for\s+(\d+(?:\.\d+)?)\+?\s*years?',

        r'(\d+(?:\.\d+)?)\+?\s*years?\s+working'
    ]

    detected_experience = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for value in matches:

            try:

                years = float(value)

                detected_experience.append(
                    years
                )

            except ValueError:

                continue

    if detected_experience:

        return max(
            detected_experience
        )

    # -------------------------------------------------
    # No experience found
    # -------------------------------------------------

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

        # -------------------------
        # SQL
        # -------------------------

        "mysql": "sql",
        "postgresql": "sql",
        "postgres": "sql",
        "mssql": "sql",
        "sql server": "sql",

        # -------------------------
        # REST API
        # -------------------------

        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",

        # -------------------------
        # Git
        # -------------------------

        "github": "git",
        "gitlab": "git",
        "bitbucket": "git",

        # -------------------------
        # Node
        # -------------------------

        "node": "node.js",
        "nodejs": "node.js",

        # -------------------------
        # Machine Learning
        # -------------------------

        "machine-learning": "machine learning",
        "deep-learning": "deep learning",

        # -------------------------
        # AI
        # -------------------------

        "ai": "artificial intelligence",

        # -------------------------
        # Networking
        # -------------------------

        "cisco networking": "cisco",
        "tcp/ip": "tcp ip"
    }

    return aliases.get(
        skill,
        skill
    )


# ---------------------------------------------
# Extract Skills
# ---------------------------------------------

def extract_skills(text):
    """
    Extract technical skills from text
    and normalize aliases.
    """

    if not text:
        return set()

    text = text.lower()

    skill_list = {

        # Programming
        "python",
        "java",
        "javascript",
        "c++",
        "c#",
        "c",

        # Web / Backend
        "html",
        "css",
        "bootstrap",
        "flask",
        "django",
        "fastapi",
        "spring",
        "spring boot",

        # API
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",

        # Database
        "sql",
        "sql server",
        "mysql",
        "postgresql",
        "postgres",
        "mssql",
        "mongodb",
        "oracle",

        # Data / AI
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "scikit-learn",

        # Frontend
        "react",
        "angular",
        "vue",

        # Mobile
        "android",
        "flutter",
        "kotlin",
        "swift",

        # DevOps / Cloud
        "git",
        "github",
        "gitlab",
        "bitbucket",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "linux",

        # Security
        "network security",
        "cybersecurity",
        "penetration testing",

        # Networking
        "tcp ip",
        "tcp/ip",
        "cisco",

        # Design
        "figma",
        "adobe xd",
        "photoshop",
        "illustrator"
    }

    found_skills = set()

    for skill in skill_list:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            normalized = normalize_skill(skill)

            found_skills.add(
                normalized
            )

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

def calculate_skill_match(
    resume_text,
    job_skills
):
    """
    Calculate percentage of required skills
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

    matched_skills = (
        resume_skills.intersection(
            required_skills
        )
    )

    missing_skills = (
        required_skills.difference(
            resume_skills
        )
    )

    skill_score = (
        len(matched_skills)
        /
        len(required_skills)
    ) * 100

    print("\nRequired Skills:")
    print(
        sorted(required_skills)
    )

    print("\nMatched Skills:")
    print(
        sorted(matched_skills)
    )

    print("\nMissing Skills:")
    print(
        sorted(missing_skills)
    )

    print(
        f"\nSkill Match: {round(skill_score, 2)}%"
    )

    return round(
        skill_score,
        2
    )

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
    Calculate final resume-job matching score.

    Weighting:

    TF-IDF similarity       = 15%
    Semantic similarity     = 25%
    Skill matching          = 40%
    Experience matching     = 20%
    """

    # -----------------------------------------
    # TF-IDF Similarity
    # -----------------------------------------

    tfidf_score = calculate_similarity(
        resume_text,
        job_description
    )

    # -----------------------------------------
    # Semantic Similarity
    # -----------------------------------------

    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    # -----------------------------------------
    # Skill Matching
    # -----------------------------------------

    skill_score = calculate_skill_match(
        resume_text,
        job_skills
    )

    # -----------------------------------------
    # Experience Matching
    # -----------------------------------------

    experience_score = calculate_experience_match(
        extracted_resume_text,
        required_experience
    )

    # -----------------------------------------
    # Final Weighted Score
    # -----------------------------------------

    final_score = (

        (tfidf_score * 0.15)

        + (semantic_score * 0.25)

        + (skill_score * 0.40)

        + (experience_score * 0.20)
    )

    # -----------------------------------------
    # Terminal Debug Information
    # -----------------------------------------

    print("\n========================================")
    print("RESUME JOB MATCH ANALYSIS")
    print("========================================")

    print(
        f"TF-IDF Similarity       : {tfidf_score}%"
    )

    print(
        f"Semantic Similarity     : {semantic_score}%"
    )

    print(
        f"Skill Match             : {skill_score}%"
    )

    print(
        f"Experience Match        : {experience_score}%"
    )

    print("----------------------------------------")

    print(
        f"Final Match Score       : {round(final_score, 2)}%"
    )

    print("========================================\n")

    return round(
        final_score,
        2
    )

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

    If the score is 50% or higher,
    also save the candidate in
    selected_candidates.
    """

    # -----------------------------------------
    # Check existing job match
    # -----------------------------------------

    existing_match = JobMatch.query.filter_by(
        resume_id=resume_id,
        job_id=job_id
    ).first()

    if existing_match:

        existing_match.similarity_score = (
            similarity_score
        )

    else:

        existing_match = JobMatch(
            resume_id=resume_id,
            job_id=job_id,
            similarity_score=similarity_score
        )

        db.session.add(
            existing_match
        )

    # -----------------------------------------
    # Selected Candidate
    # -----------------------------------------

    if similarity_score >= 50:

        existing_selection = SelectedCandidate.query.filter_by(
            resume_id=resume_id,
            job_id=job_id
        ).first()

        # Don't create duplicate selection
        if not existing_selection:

            selected_candidate = SelectedCandidate(
                resume_id=resume_id,
                job_id=job_id
            )

            db.session.add(
                selected_candidate
            )

    # -----------------------------------------
    # Save to database
    # -----------------------------------------

    db.session.commit()

    return existing_match


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