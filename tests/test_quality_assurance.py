"""Tests for quality assurance module."""
import pytest
from src.quality_assurance import QualityAssurance


class TestQualityAssurance:
    """Test cases for QualityAssurance."""

    def setup_method(self):
        """Setup test fixtures."""
        self.qa = QualityAssurance()

    def test_validate_python_syntax_valid(self):
        """Test valid Python syntax validation."""
        code = "def hello():\n    print('Hello')"
        errors = self.qa._validate_python_syntax("test.py", code)

        assert len(errors) == 0

    def test_validate_python_syntax_invalid(self):
        """Test invalid Python syntax validation."""
        code = "def hello(\n    print('Hello')"
        errors = self.qa._validate_python_syntax("test.py", code)

        assert len(errors) > 0
        assert "syntax error" in errors[0].lower()

    def test_validate_json_syntax_valid(self):
        """Test valid JSON syntax validation."""
        json_str = '{"name": "test", "version": "1.0.0"}'
        errors = self.qa._validate_json_syntax("package.json", json_str)

        assert len(errors) == 0

    def test_validate_json_syntax_invalid(self):
        """Test invalid JSON syntax validation."""
        json_str = '{"name": "test", "version": 1.0.0}'
        errors = self.qa._validate_json_syntax("package.json", json_str)

        assert len(errors) > 0

    def test_check_security_hardcoded_password(self):
        """Test detection of hardcoded passwords."""
        files = {"config.py": "password = 'secret123'"}
        issues = self.qa._check_security(files)

        assert len(issues) > 0
        assert any("password" in issue.lower() for issue in issues)

    def test_check_security_hardcoded_api_key(self):
        """Test detection of hardcoded API keys."""
        files = {"config.py": "api_key = 'sk-1234567890'"}
        issues = self.qa._check_security(files)

        assert len(issues) > 0
        assert any("api key" in issue.lower() for issue in issues)

    def test_check_security_env_example_ignored(self):
        """Test that .env.example is ignored in security checks."""
        files = {".env.example": "API_KEY=your_api_key_here"}
        issues = self.qa._check_security(files)

        assert len(issues) == 0

    def test_validate_readme_complete(self):
        """Test README validation with complete content."""
        files = {
            "README.md": """
# Project Name

## Requirements

- Node.js 18+

## Setup

1. Install dependencies
2. Run the application
"""
        }
        errors = self.qa._validate_readme(files)

        assert len(errors) == 0

    def test_validate_readme_missing(self):
        """Test README validation when missing."""
        files = {}
        errors = self.qa._validate_readme(files)

        assert len(errors) > 0
        assert any("missing" in error.lower() for error in errors)

    def test_validate_readme_incomplete(self):
        """Test README validation with incomplete content."""
        files = {"README.md": "# Project"}
        errors = self.qa._validate_readme(files)

        assert len(errors) > 0

    def test_estimate_test_coverage(self):
        """Test test coverage estimation."""
        files = {
            "src/main.py": "code",
            "src/utils.py": "code",
            "tests/test_main.py": "test",
            "tests/test_utils.py": "test",
        }
        coverage = self.qa.estimate_test_coverage(files)

        assert coverage >= 70

    def test_count_test_files(self):
        """Test counting test files."""
        files = {
            "src/main.py": "code",
            "tests/test_main.py": "test",
            "tests/test_utils.py": "test",
        }
        count = self.qa.count_test_files(files)

        assert count == 2

    def test_check_required_files_nodejs(self):
        """Test required files check for Node.js."""
        files = {
            "package.json": "{}",
            "README.md": "# Project",
            ".gitignore": "",
        }
        result = self.qa._check_required_files(files, "nodejs-express")

        assert result is True

    def test_check_required_files_missing(self):
        """Test required files check with missing files."""
        files = {"package.json": "{}"}
        result = self.qa._check_required_files(files, "nodejs-express")

        assert result is False

    def test_validate_project_success(self):
        """Test complete project validation success."""
        files = {
            "package.json": '{"name": "test"}',
            "README.md": """
# Test Project

A comprehensive test project for validating the quality assurance system.

## Requirements

- Node.js 18+
- npm or yarn

## Setup

1. Clone the repository
2. Install dependencies
3. Run the application

## Testing

Run tests with npm test
""",
            ".gitignore": "node_modules/",
            "src/main.js": "console.log('hello');",
            "tests/test_main.js": "test code",
        }

        is_valid, errors = self.qa.validate_project(files, "nodejs-express")

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_no_placeholders(self):
        """Test placeholder detection."""
        files = {
            "src/config.py": "API_KEY = 'TODO: Add your key'",
        }
        errors = self.qa.validate_no_placeholders(files)

        assert len(errors) > 0
        assert any("TODO" in error for error in errors)
