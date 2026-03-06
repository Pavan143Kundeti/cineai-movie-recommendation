"""
Quick test script to verify setup is correct
Run this from the project root directory
"""
import os
import sys

def check_files():
    """Check if all required files exist"""
    print("Checking project structure...")
    
    required_files = [
        "backend/app/main.py",
        "backend/app/core/config.py",
        "backend/app/core/database.py",
        "backend/app/core/security.py",
        "backend/requirements.txt",
        "backend/.env.example",
        "backend/migrate_data.py",
        "frontend/app.py",
        "frontend/requirements.txt",
        "tmdb_5000_movies.csv",
        "tmdb_5000_credits.csv"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("❌ Missing files:")
        for f in missing:
            print(f"   - {f}")
        return False
    else:
        print("✅ All required files present")
        return True


def check_env():
    """Check if .env file exists"""
    print("\nChecking environment configuration...")
    
    if os.path.exists("backend/.env"):
        print("✅ .env file exists")
        
        # Check if it has required variables
        with open("backend/.env", "r") as f:
            content = f.read()
            required_vars = ["DATABASE_URL", "TMDB_API_KEY", "OMDB_API_KEY", "SECRET_KEY"]
            missing_vars = []
            
            for var in required_vars:
                if var not in content or f"{var}=your" in content or f"{var}=" in content and len(content.split(f"{var}=")[1].split("\n")[0].strip()) < 10:
                    missing_vars.append(var)
            
            if missing_vars:
                print("⚠️  Please configure these variables in backend/.env:")
                for var in missing_vars:
                    print(f"   - {var}")
                return False
            else:
                print("✅ Environment variables configured")
                return True
    else:
        print("❌ .env file not found")
        print("   Run: copy backend\\.env.example backend\\.env")
        return False


def check_python_version():
    """Check Python version"""
    print("\nChecking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro}")
        print("   Required: Python 3.8+")
        return False


def check_venv():
    """Check if virtual environment exists"""
    print("\nChecking virtual environment...")
    
    if os.path.exists("backend/venv") or os.path.exists("backend/env"):
        print("✅ Virtual environment exists")
        return True
    else:
        print("⚠️  Virtual environment not found")
        print("   Run: cd backend && python -m venv venv")
        return False


def main():
    print("=" * 50)
    print("Movie Recommendation System - Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_files(),
        check_venv(),
        check_env()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✅ Setup verification passed!")
        print("\nNext steps:")
        print("1. Activate virtual environment:")
        print("   cd backend && venv\\Scripts\\activate")
        print("2. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("3. Create database:")
        print("   mysql -u root -p")
        print("   CREATE DATABASE movie_recommender;")
        print("4. Migrate data:")
        print("   python migrate_data.py")
        print("5. Start backend:")
        print("   uvicorn app.main:app --reload")
        print("6. Start frontend (new terminal):")
        print("   cd frontend && streamlit run app.py")
    else:
        print("❌ Setup verification failed")
        print("\nPlease fix the issues above and run this script again.")
    print("=" * 50)


if __name__ == "__main__":
    main()
