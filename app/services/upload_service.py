import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "app/uploads/resumes"


def save_resume(file):

    # Create folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Secure the filename
    filename = secure_filename(file.filename)

    # Full path
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save file
    file.save(filepath)

    return filename