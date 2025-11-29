"""
Simple script to seed achievements.
Run this from the backend directory: python scripts/run_seed.py
"""
from scripts.seed_achievements import seed_achievements

if __name__ == "__main__":
    print("Starting achievement seeding...")
    seed_achievements()
    print("Done!")


