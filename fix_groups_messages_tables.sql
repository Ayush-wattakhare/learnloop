-- Fix Groups and Messages pages
-- Run this in phpMyAdmin for database: sql12817859

-- 1. Add is_public column to groups table
ALTER TABLE `groups` 
ADD COLUMN is_public BOOLEAN DEFAULT TRUE;

-- Update existing groups to be public
UPDATE `groups` SET is_public = TRUE WHERE is_public IS NULL;

-- 2. Create friendships table
CREATE TABLE IF NOT EXISTS friendships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    friend_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (friend_id) REFERENCES users(id),
    UNIQUE KEY unique_friendship (user_id, friend_id)
);

-- 3. Create direct_messages table
CREATE TABLE IF NOT EXISTS direct_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message TEXT,
    file_name VARCHAR(255),
    file_path VARCHAR(255),
    file_type ENUM('document', 'image', 'pdf', 'other') DEFAULT 'other',
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);
