-- =====================================================
-- LearnLoop Database Schema
-- Run this in phpMyAdmin or MySQL terminal
-- =====================================================

CREATE DATABASE IF NOT EXISTS learnloop;
USE learnloop;

-- Users Table
CREATE TABLE users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    semester   INT NOT NULL,
    college    VARCHAR(150) DEFAULT '',
    bio        TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Groups Table
CREATE TABLE groups (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    group_name  VARCHAR(100) NOT NULL,
    subject     VARCHAR(100) NOT NULL,
    semester    INT NOT NULL,
    description TEXT,
    created_by  INT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Group Members Table
CREATE TABLE group_members (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    group_id  INT,
    user_id   INT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_member (group_id, user_id)
);

-- Notes Table
CREATE TABLE notes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    group_id    INT,
    uploaded_by INT,
    title       VARCHAR(200),
    file_name   VARCHAR(255),
    file_path   VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id)    REFERENCES groups(id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- Messages Table
CREATE TABLE messages (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT,
    user_id  INT,
    message  TEXT NOT NULL,
    sent_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (user_id)  REFERENCES users(id)
);


-- Password Reset OTP Table
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
