"""Tests for input processor module."""
import pytest
from src.input_processor import InputProcessor


class TestInputProcessor:
    """Test cases for InputProcessor."""

    def setup_method(self):
        """Setup test fixtures."""
        self.processor = InputProcessor()

    def test_process_input_basic(self):
        """Test basic input processing."""
        result = self.processor.process_input(
            description="Build a web API",
            repo_name="test-api",
        )

        assert result["description"] == "Build a web API"
        assert result["repo_name"] == "test-api"
        assert result["license"] == "MIT"
        assert result["is_private"] is False

    def test_process_input_with_features(self):
        """Test input processing with features."""
        features = ["user authentication", "data validation"]
        result = self.processor.process_input(
            description="Build a web API", features=features
        )

        assert result["features"] == features

    def test_process_input_empty_description(self):
        """Test that empty description raises error."""
        with pytest.raises(ValueError, match="Project description is required"):
            self.processor.process_input(description="")

    def test_generate_repo_name_from_description(self):
        """Test automatic repo name generation."""
        result = self.processor.process_input(
            description="Build a todo list application"
        )

        assert result["repo_name"] == "build-a-todo"

    def test_sanitize_repo_name(self):
        """Test repository name sanitization."""
        sanitized = self.processor._sanitize_repo_name("My Project! @#$%")
        assert sanitized == "My-Project"

    def test_validate_repo_name_invalid_chars(self):
        """Test repo name validation with invalid characters."""
        with pytest.raises(ValueError, match="can only contain"):
            self.processor._validate_repo_name("repo@name#invalid")

    def test_extract_keywords_web(self):
        """Test keyword extraction for web projects."""
        keywords = self.processor.extract_keywords(
            "Build a REST API web service with database"
        )

        assert "web" in keywords
        assert "backend" in keywords

    def test_extract_keywords_mobile(self):
        """Test keyword extraction for mobile projects."""
        keywords = self.processor.extract_keywords("Create a mobile app for iOS and Android")

        assert "mobile" in keywords

    def test_extract_keywords_cli(self):
        """Test keyword extraction for CLI projects."""
        keywords = self.processor.extract_keywords("Build a command-line tool")

        assert "cli" in keywords

    def test_invalid_license_defaults_to_mit(self):
        """Test that invalid license defaults to MIT."""
        result = self.processor.process_input(
            description="Test project", license_type="INVALID"
        )

        assert result["license"] == "MIT"
