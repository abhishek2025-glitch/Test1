"""Tests for response formatter module."""
import pytest
import tempfile
import os
from src.response_formatter import ResponseFormatter


class TestResponseFormatter:
    """Test cases for ResponseFormatter."""

    def setup_method(self):
        """Setup test fixtures."""
        self.formatter = ResponseFormatter()

    def test_format_response(self):
        """Test response formatting."""
        repo_info = {
            "name": "test-repo",
            "url": "https://github.com/user/test-repo",
            "default_branch": "main",
            "clone_url": "https://github.com/user/test-repo.git",
        }
        project_info = {"repo_name": "test-repo"}

        with tempfile.TemporaryDirectory() as tmpdir:
            response = self.formatter.format_response(
                repo_info=repo_info,
                project_info=project_info,
                stack_id="nodejs-express",
                file_count=10,
                test_count=3,
                repo_path=tmpdir,
            )

            assert "AI CODE GENERATOR - SUCCESS" in response
            assert "test-repo" in response
            assert "nodejs-express" in response
            assert "10" in response
            assert "3" in response

    def test_format_error(self):
        """Test error formatting."""
        error_msg = "Repository already exists"
        details = ["Error type: ValueError", "Additional detail"]

        response = self.formatter.format_error(error_msg, details)

        assert "AI CODE GENERATOR - ERROR" in response
        assert error_msg in response
        assert "ValueError" in response
        assert "Additional detail" in response

    def test_format_error_without_details(self):
        """Test error formatting without details."""
        error_msg = "GitHub token is invalid"

        response = self.formatter.format_error(error_msg)

        assert "ERROR" in response
        assert error_msg in response
        assert "Suggestions" in response

    def test_generate_tree(self):
        """Test directory tree generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "src"))
            os.makedirs(os.path.join(tmpdir, "tests"))
            
            with open(os.path.join(tmpdir, "README.md"), "w") as f:
                f.write("# Test")
            with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
                f.write("print('hello')")

            tree = self.formatter._generate_tree(tmpdir)

            assert "README.md" in tree
            assert "src" in tree
            assert "tests" in tree
