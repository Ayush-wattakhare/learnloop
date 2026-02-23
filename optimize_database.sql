-- Database Optimization for LearnLoop
-- Run this in phpMyAdmin for database: sql12817859

-- Add indexes for faster queries
ALTER TABLE users ADD INDEX idx_email (email);
ALTER TABLE users ADD INDEX idx_semester (semester);

ALTER TABLE groups ADD INDEX idx_created_by (created_by);
ALTER TABLE groups ADD INDEX idx_semester (semester);
ALTER TABLE groups ADD INDEX idx_is_public (is_public);

ALTER TABLE group_members ADD INDEX idx_group_id (group_id);
ALTER TABLE group_members ADD INDEX idx_user_id (user_id);

ALTER TABLE messages ADD INDEX idx_group_id (group_id);
ALTER TABLE messages ADD INDEX idx_user_id (user_id);

ALTER TABLE notifications ADD INDEX idx_user_id (user_id);
ALTER TABLE notifications ADD INDEX idx_is_read (is_read);
ALTER TABLE notifications ADD INDEX idx_created_at (created_at);

ALTER TABLE friendships ADD INDEX idx_user_id (user_id);
ALTER TABLE friendships ADD INDEX idx_friend_id (friend_id);
ALTER TABLE friendships ADD INDEX idx_status (status);

ALTER TABLE direct_messages ADD INDEX idx_sender_id (sender_id);
ALTER TABLE direct_messages ADD INDEX idx_receiver_id (receiver_id);
ALTER TABLE direct_messages ADD INDEX idx_sent_at (sent_at);

ALTER TABLE voice_rooms ADD INDEX idx_host_id (host_id);
ALTER TABLE voice_rooms ADD INDEX idx_is_active (is_active);
ALTER TABLE voice_rooms ADD INDEX idx_room_code (room_code);

ALTER TABLE room_participants ADD INDEX idx_room_id (room_id);
ALTER TABLE room_participants ADD INDEX idx_user_id (user_id);

-- Optimize tables
OPTIMIZE TABLE users;
OPTIMIZE TABLE groups;
OPTIMIZE TABLE group_members;
OPTIMIZE TABLE messages;
OPTIMIZE TABLE notifications;
OPTIMIZE TABLE friendships;
OPTIMIZE TABLE direct_messages;
OPTIMIZE TABLE voice_rooms;
OPTIMIZE TABLE room_participants;
