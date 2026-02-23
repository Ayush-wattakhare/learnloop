-- Fix voice_rooms table - Add missing room_type column
-- Run this in phpMyAdmin for database: sql12817859

ALTER TABLE `voice_rooms` 
ADD COLUMN room_type ENUM('video', 'audio', 'screen_share') DEFAULT 'video' AFTER is_public;
