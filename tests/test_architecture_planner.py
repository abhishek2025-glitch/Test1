"""Tests for architecture planner module."""
import pytest
from src.architecture_planner import ArchitecturePlanner


class TestArchitecturePlanner:
    """Test cases for ArchitecturePlanner."""

    def setup_method(self):
        """Setup test fixtures."""
        self.planner = ArchitecturePlanner()

    def test_plan_architecture_nodejs(self):
        """Test architecture planning for Node.js."""
        architecture = self.planner.plan_architecture(
            "nodejs-express", ["user management"], "Build a REST API"
        )

        assert "directories" in architecture
        assert "files" in architecture
        assert "src" in architecture["directories"]
        assert "tests" in architecture["directories"]
        assert ".github/workflows/ci.yml" in architecture["files"]

    def test_plan_architecture_python_fastapi(self):
        """Test architecture planning for Python FastAPI."""
        architecture = self.planner.plan_architecture(
            "python-fastapi", [], "Build an API"
        )

        assert "src" in architecture["directories"]
        assert "src/main.py" in architecture["files"]
        assert "tests" in architecture["directories"]

    def test_plan_architecture_includes_ci_workflow(self):
        """Test that architecture includes CI/CD workflow."""
        architecture = self.planner.plan_architecture(
            "nodejs-express", [], "Test project"
        )

        assert ".github" in architecture["directories"]
        assert ".github/workflows" in architecture["directories"]
        assert ".github/workflows/ci.yml" in architecture["files"]

    def test_generate_api_design_basic(self):
        """Test basic API design generation."""
        api_design = self.planner.generate_api_design([])

        assert "endpoints" in api_design
        assert len(api_design["endpoints"]) > 0

        health_endpoint = api_design["endpoints"][0]
        assert health_endpoint["method"] == "GET"
        assert health_endpoint["path"] == "/health"

    def test_generate_api_design_with_user_feature(self):
        """Test API design with user features."""
        api_design = self.planner.generate_api_design(["user authentication"])

        endpoints = api_design["endpoints"]
        paths = [ep["path"] for ep in endpoints]

        assert any("/api/users" in path for path in paths)

    def test_generate_api_design_with_product_feature(self):
        """Test API design with product features."""
        api_design = self.planner.generate_api_design(["product management"])

        endpoints = api_design["endpoints"]
        paths = [ep["path"] for ep in endpoints]

        assert any("/api/items" in path for path in paths)
