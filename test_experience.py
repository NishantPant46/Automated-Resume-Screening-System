from app.services.job_match_service import extract_experience


tests = [

    # Test 1
    """
    Python Developer
    Jan 2022 - Dec 2025
    Developed backend applications using Python and Flask.
    """,

    # Test 2
    """
    Software Engineer
    2020 - 2023
    Worked on web applications.
    """,

    # Test 3
    """
    Senior Developer
    5+ years of professional experience in Python and Django.
    """,

    # Test 4
    """
    Data Scientist
    March 2018 - June 2024
    Built machine learning models.
    """,

    # Test 5
    """
    Developer
    2019 - Present
    Working with Python and Flask.
    """,

    # Test 6
    """
    Senior Data Scientist — Google Brain
    Jan 2021 - Dec 2025

    Data Scientist — Netflix
    2018 - 2020
    """
]


for i, resume in enumerate(tests, start=1):

    experience = extract_experience(resume)

    print(
        f"Test {i}: {experience} Years"
    )