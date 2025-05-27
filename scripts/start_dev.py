# scripts/start_dev.py
"""
Development server startup script
"""
import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("requirements.txt not found!")
        return False
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✓ All main dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_database():
    """Initialize database"""
    print("Setting up database...")
    try:
        from scripts.init_db import main
        main()
        print("✓ Database setup completed")
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        print("Please check your database configuration")

def main():
    """Start development server"""
    print("PrintOptimizer Backend - Development Server")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    # Start development server
    print("\nStarting development server...")
    print("API Documentation: http://localhost:8000/api/docs")
    print("Admin Panel: http://localhost:8000/api/redoc")
    print("\nPress Ctrl+C to stop the server")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
        "--reload-dir", "app"
    ])

if __name__ == "__main__":
    main()