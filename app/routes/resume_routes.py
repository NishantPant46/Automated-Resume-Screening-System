from flask import Blueprint, render_template, request, jsonify, redirect, url_for


from app.services.upload_service import save_resume
from app.services.resume_service import save_resume_data
from app.services.resume_service import get_all_resumes
from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import preprocess_text

import os

resume_bp = Blueprint("resume", __name__)

# ----------------------------
# Login Page
# ----------------------------
@resume_bp.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Temporary login
        print(email)
        print(password)

        return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/login.html")


# ----------------------------
# Resume Upload Page
# ----------------------------
@resume_bp.route("/resume")
def resume_page():
    return render_template("resume/upload_resume.html")


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

    # Save PDF
    filename = save_resume(resume)

    # Path of uploaded PDF
    file_path = os.path.join(
        "app",
        "uploads",
        "resumes",
        filename
    )

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)


    processed_text = preprocess_text(extracted_text)


    # Read form data
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    # Save information to database
    save_resume_data(
        full_name,
        email,
        phone,
        filename,
        extracted_text,
        processed_text
    )

    return jsonify({
        "success": True,
        "message": "Resume uploaded successfully.",
        "file_name": filename
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

@resume_bp.route("/resume-text/<int:id>")
def resume_text(id):

    from app.models.resume_model import Resume

    resume = Resume.query.get_or_404(id)

    return f"<pre>{resume.extracted_text}</pre>"