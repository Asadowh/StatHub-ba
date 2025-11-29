-- Migration: Add category column to news table
-- Run this migration to add the category field to the news table

ALTER TABLE news ADD COLUMN IF NOT EXISTS category VARCHAR(50) NULL;

-- Verify the column was added
-- SELECT column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name = 'news' AND column_name = 'category';

