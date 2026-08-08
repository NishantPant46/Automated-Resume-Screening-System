from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from app.services.upload_service import save_resume
from app.services.resume_service import save_resume_data
from app.services.resume_service import get_all_resumes
from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import preprocess_text
from app.services.job_match_service import calculate_similarity
from app.services.job_match_service import save_job_match

import os
import joblib


resume_bp = Blueprint("resume", __name__)


# ----------------------------
# Load ML Model and Vectorizer
# ----------------------------

MODEL_PATH = os.path.join(
    "training",
    "model.pkl"
)

VECTORIZER_PATH = os.path.join(
    "training",
    "vectorizer.pkl"
)

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# ----------------------------
# Login Page
# ----------------------------

@resume_bp.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        print(email)
        print(password)

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "auth/login.html"
    )


# ----------------------------
# Resume Upload Page
# ----------------------------

@resume_bp.route("/resume")
def resume_page():

    return render_template(
        "resume/upload_resume.html"
    )


# ----------------------------
# Resume Upload API
# ----------------------------

@resume_bp.route("/upload-resume", methods=["POST"])
def upload_resume():

    # Check whether a file was selected
    if "resume" not in request.files:

        return jsonify({
            "success": False,
            "message": "Resume file missing."
        }), 400


    resume = request.files["resume"]


    # Check empty filename
    if resume.filename == "":

        return jsonify({
            "success": False,
            "message": "Please choose a PDF."
        }), 400


    # ----------------------------
    # Save PDF
    # ----------------------------

    filename = save_resume(resume)


    # ----------------------------
    # PDF Path
    # ----------------------------

    file_path = os.path.join(
        "app",
        "uploads",
        "resumes",
        filename
    )


    # ----------------------------
    # Extract Text
    # ----------------------------

    extracted_text = extract_text_from_pdf(
        file_path
    )


    # ----------------------------
    # NLP Preprocessing
    # ----------------------------

    processed_text = preprocess_text(
        extracted_text
    )


    # ----------------------------
    # TF-IDF Transformation
    # ----------------------------

    resume_vector = vectorizer.transform(
        [processed_text]
    )


    # ----------------------------
    # Logistic Regression Prediction
    # ----------------------------

    predicted_job_role = model.predict(
        resume_vector
    )[0]


    print(
        "Predicted Job Role:",
        predicted_job_role
    )


    # ----------------------------
    # Read Form Data
    # ----------------------------

    full_name = request.form.get(
        "full_name"
    )

    email = request.form.get(
        "email"
    )

    phone = request.form.get(
        "phone"
    )


    # ----------------------------
    # Save Resume Information
    # ----------------------------

    save_resume_data(
        full_name,
        email,
        phone,
        filename,
        extracted_text,
        processed_text,
        predicted_job_role
    )


    # ----------------------------
    # Return Result
    # ----------------------------

    return jsonify({
        "success": True,
        "message": "Resume uploaded and analyzed successfully.",
        "file_name": filename,
        "predicted_job_role": predicted_job_role
    }), 201


# ----------------------------
# Candidate List
# ----------------------------

@resume_bp.route("/candidates")
def candidates():

    resumes = get_all_resumes()

    return render_template(
        "candidates/candidates_list.html",
        resumes=resumes
    )


# ----------------------------
# View Resume Text
# ----------------------------

@resume_bp.route("/resume-text/<int:id>")
def resume_text(id):

    from app.models.resume_model import Resume

    resume = Resume.query.get_or_404(id)

    return f"<pre>{resume.extracted_text}</pre>"