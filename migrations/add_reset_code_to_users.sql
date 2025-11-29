-- Migration: Add reset_code fields to users table
-- Run this migration to add password reset code support

ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_code VARCHAR(6) NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_code_expires_at TIMESTAMP WITH TIME ZONE NULL;

-- Verify the columns were added
-- SELECT column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name = 'users' AND column_name IN ('reset_code', 'reset_code_expires_at');



