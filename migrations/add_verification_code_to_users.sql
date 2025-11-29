-- Migration: Add verification_code fields to users table
-- Run this migration to add verification code support

ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_code VARCHAR(6) NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_code_expires_at TIMESTAMP WITH TIME ZONE NULL;

-- Verify the columns were added
-- SELECT column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name = 'users' AND column_name IN ('verification_code', 'verification_code_expires_at');



