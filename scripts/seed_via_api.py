"""
Script to seed achievements via API endpoint.
This is easier than running the seed script directly.
Make sure your FastAPI server is running on http://localhost:8000
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def seed_achievements_via_api(token: str):
    """Seed achievements via API"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/achievements/seed",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Achievements seeded successfully!")
        print(response.json())
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def check_all_players_via_api(token: str):
    """Check all players for achievements via API"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/achievements/check-all",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Checked all players for achievements!")
        print(response.json())
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("StatHub Achievement Seeder")
    print("=" * 50)
    print("\nThis script will:")
    print("1. Seed all 9 achievements into the database")
    print("2. Check all existing players and unlock achievements they've earned")
    print("\n⚠️  Make sure:")
    print("   - Your FastAPI server is running on http://localhost:8000")
    print("   - You have an admin user token")
    print()
    
    token = input("Enter your admin JWT token (or press Enter to skip): ").strip()
    
    if not token:
        print("\n❌ No token provided. Please get your token from:")
        print("   1. Login via Swagger UI: http://localhost:8000/docs")
        print("   2. Copy the token from the response")
        print("   3. Run this script again with the token")
        exit(1)
    
    print("\n📦 Seeding achievements...")
    if seed_achievements_via_api(token):
        print("\n🔍 Checking existing players...")
        check_all_players_via_api(token)
        print("\n✅ Done! All achievements have been seeded and players have been checked.")
    else:
        print("\n❌ Failed to seed achievements. Please check the error above.")


