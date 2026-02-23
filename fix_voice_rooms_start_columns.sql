-- Add missing columns for voice room start functionality
-- Run this in phpMyAdmin for database: sql12817859

ALTER TABLE `voice_rooms` 
ADD COLUMN started_at TIMESTAMP NULL AFTER created_at,
ADD COLUMN host_online BOOLEAN DEFAULT FALSE AFTER is_active;
