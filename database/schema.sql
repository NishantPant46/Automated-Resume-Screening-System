CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    file_name VARCHAR(255) NOT NULL,
    extracted_text TEXT,
    processed_text TEXT,
    predicted_job_role VARCHAR(100),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);