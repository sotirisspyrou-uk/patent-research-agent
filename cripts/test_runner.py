## 5. scripts/test_runner.py - Automated Testing
#!/usr/bin/env python3
"""
Comprehensive Test Runner
Runs all tests and generates coverage reports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Run all tests and checks"""
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🧪 Running Patent Research Agent Test Suite")
    
    tests_passed = 0
    total_tests = 0
    
    # Code formatting check
    total_tests += 1
    if run_command("black --check .", "Code formatting check (black)"):
        tests_passed += 1
    
    # Import sorting check
    total_tests += 1
    if run_command("isort --check-only .", "Import sorting check (isort)"):
        tests_passed += 1
    
    # Linting
    total_tests += 1
    if run_command("flake8 .", "Code linting (flake8)"):
        tests_passed += 1
    
    # Type checking
    total_tests += 1
    if run_command("mypy .", "Type checking (mypy)"):
        tests_passed += 1
    
    # Security scanning
    total_tests += 1
    if run_command("bandit -r .", "Security scanning (bandit)"):
        tests_passed += 1
    
    # Dependency vulnerability check
    total_tests += 1
    if run_command("safety check", "Dependency vulnerability check (safety)"):
        tests_passed += 1
    
    # Unit tests with coverage
    total_tests += 1
    if run_command("pytest --cov=app --cov-report=html --cov-report=term", "Unit tests with coverage"):
        tests_passed += 1
    
    # Integration tests
    total_tests += 1
    if run_command("pytest tests/integration/", "Integration tests"):
        tests_passed += 1
    
    # API tests
    total_tests += 1
    if run_command("pytest tests/api/", "API tests"):
        tests_passed += 1
    
    # Generate final report
    print("\n" + "="*50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
