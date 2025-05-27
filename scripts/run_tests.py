# scripts/run_tests.py
"""
Test runner script
"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests"""
    print("Running PrintOptimizer Backend Tests...")
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    
    # Run pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term"
    ])
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)