-- Add room_type column to voice_rooms table
-- Run this in MySQL to add the new feature

USE learnloop;

-- Add room_type column (video or audio-only)
ALTER TABLE voice_rooms 
ADD COLUMN room_type ENUM('video', 'audio') DEFAULT 'video' AFTER is_public;
