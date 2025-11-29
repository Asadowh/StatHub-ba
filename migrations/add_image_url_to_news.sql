-- Migration: Add image_url column to news table
-- Run this SQL script to update your database schema

ALTER TABLE news 
ADD COLUMN IF NOT EXISTS image_url VARCHAR;

-- Verify the column was added
-- SELECT column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name = 'news' AND column_name = 'image_url';

