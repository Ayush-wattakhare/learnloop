-- =====================================================
-- Complete LearnLoop Database Schema for Production
-- Run this in phpMyAdmin for sql12817859 database
-- =====================================================

-- Voice Rooms Table
CREATE TABLE IF NOT EXISTS `voice_rooms` (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    room_name   VARCHAR(150) NOT NULL,
    subject     VARCHAR(100) NOT NULL,
    description TEXT,
    host_id     INT NOT NULL,
    group_id    INT NULL,
    is_public   BOOLEAN DEFAULT TRUE,
    is_active   BOOLEAN DEFAULT TRUE,
    max_stage   INT DEFAULT 6,
    room_code   VARCHAR(20) UNIQUE NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at    TIMESTAMP NULL,
    FOREIGN KEY (host_id) REFERENCES `users`(id),
    FOREIGN KEY (group_id) REFERENCES `groups`(id)
);

-- Room Participants Table
CREATE TABLE IF NOT EXISTS `room_participants` (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    room_id     INT NOT NULL,
    user_id     INT NOT NULL,
    role        ENUM('host', 'stage', 'audience') DEFAULT 'audience',
    is_video_on BOOLEAN DEFAULT FALSE,
    is_audio_on BOOLEAN DEFAULT FALSE,
    joined_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    left_at     TIMESTAMP NULL,
    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
    FOREIGN KEY (user_id) REFERENCES `users`(id)
);

-- Room Chat Messages Table
CREATE TABLE IF NOT EXISTS `room_messages` (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    room_id    INT NOT NULL,
    user_id    INT NOT NULL,
    message    TEXT NOT NULL,
    is_pinned  BOOLEAN DEFAULT FALSE,
    sent_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
    FOREIGN KEY (user_id) REFERENCES `users`(id)
);

-- Stage Requests Table
CREATE TABLE IF NOT EXISTS `stage_requests` (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    room_id     INT NOT NULL,
    user_id     INT NOT NULL,
    status      ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP NULL,
    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
    FOREIGN KEY (user_id) REFERENCES `users`(id)
);

-- Whiteboard Snapshots Table
CREATE TABLE IF NOT EXISTS `whiteboard_snapshots` (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    room_id     INT NOT NULL,
    snapshot_data LONGTEXT NOT NULL,
    created_by  INT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
    FOREIGN KEY (created_by) REFERENCES `users`(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_voice_rooms_active ON `voice_rooms`(is_active);
CREATE INDEX IF NOT EXISTS idx_voice_rooms_host ON `voice_rooms`(host_id);
CREATE INDEX IF NOT EXISTS idx_room_participants_room ON `room_participants`(room_id);
CREATE INDEX IF NOT EXISTS idx_room_participants_user ON `room_participants`(user_id);
CREATE INDEX IF NOT EXISTS idx_room_messages_room ON `room_messages`(room_id);
CREATE INDEX IF NOT EXISTS idx_stage_requests_room ON `stage_requests`(room_id);
