-- Add password reset OTP table to local database
USE learnloop;

CREATE TABLE IF NOT EXISTS password_reset_otps (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    email       VARCHAR(100) NOT NULL,
    otp         VARCHAR(6) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at  TIMESTAMP NOT NULL,
    used        BOOLEAN DEFAULT FALSE,
    INDEX idx_email (email),
    INDEX idx_otp (otp)
);

SELECT 'Table password_reset_otps created successfully!' AS status;
