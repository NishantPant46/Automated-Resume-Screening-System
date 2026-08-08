from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import preprocess_text

import os
import re
import pandas as pd

# Folder containing uploaded resumes
RESUME_FOLDER = "app/uploads/resumes"

dataset = []

# Loop through every PDF
for file_name in os.listdir(RESUME_FOLDER):

    if file_name.lower().endswith(".pdf"):

        file_path = os.path.join(RESUME_FOLDER, file_name)

        print(f"Processing {file_name}...")

        # Extract text
        extracted_text = extract_text_from_pdf(file_path)

        # NLP preprocessing
        processed_text = preprocess_text(extracted_text)

        # -----------------------------
        # Extract Candidate Name
        # -----------------------------
        lines = extracted_text.split("\n")
        candidate_name = lines[0].strip() if lines else ""

        # -----------------------------
        # Extract Email
        # -----------------------------
        email_match = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            extracted_text
        )

        email = email_match.group(0) if email_match else ""

        # -----------------------------
        # Extract Phone Number
        # -----------------------------
        phone_match = re.search(
            r'(\+977[- ]?\d{10}|\d{10})',
            extracted_text
        )

        phone = phone_match.group(0) if phone_match else ""

        # -----------------------------
        # Extract Role
        # -----------------------------
        role = ""

        role_match = re.search(
            r'Role:\s*(.*)',
            extracted_text
        )

        if role_match:
            role = role_match.group(1).strip()

        # -----------------------------
        # Extract Education
        # -----------------------------
        education = ""

        education_match = re.search(
            r'Education\s*(.*?)\s*(Skills|Technical Skills|Experience|Projects)',
            extracted_text,
            re.DOTALL
        )

        if education_match:
            education = education_match.group(1).replace("\n", " ").strip()

        # -----------------------------
        # Extract Skills
        # -----------------------------
        skills = ""

        skills_match = re.search(
            r'(Skills|Technical Skills)\s*(.*?)\s*(Experience|Projects|Certifications)',
            extracted_text,
            re.DOTALL
        )

        if skills_match:
            skills = skills_match.group(2).replace("\n", " ").strip()

        # -----------------------------
        # Extract Projects
        # -----------------------------
        projects = ""

        projects_match = re.search(
            r'Projects\s*(.*?)\s*(Certifications|$)',
            extracted_text,
            re.DOTALL
        )

        if projects_match:
            projects = projects_match.group(1).replace("\n", " ").strip()

        # -----------------------------
        # Save Data
        # -----------------------------
        dataset.append({

            "file_name": file_name,

            "candidate_name": candidate_name,

            "email": email,

            "phone": phone,

            "role": role,

            "education": education,

            "skills": skills,

            "projects": projects,

            "extracted_text": extracted_text,

            "processed_text": processed_text

        })

# Create DataFrame
df = pd.DataFrame(dataset)

# Save CSV
output_file = "training/dataset.csv"

df.to_csv(output_file, index=False)

print("\nDataset created successfully!")
print(f"Saved to: {output_file}")
print(f"Total resumes processed: {len(df)}")