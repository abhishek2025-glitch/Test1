"""Tests for tech stack selector module."""
import pytest
from src.tech_stack_selector import TechStackSelector


class TestTechStackSelector:
    """Test cases for TechStackSelector."""

    def setup_method(self):
        """Setup test fixtures."""
        self.selector = TechStackSelector()

    def test_select_stack_nodejs_express(self):
        """Test Node.js selection for web backend."""
        stack_id = self.selector.select_stack(["web", "backend"])

        assert stack_id == "nodejs-express"

    def test_select_stack_python_fastapi(self):
        """Test Python FastAPI selection."""
        stack_id = self.selector.select_stack(["web", "api"], preferred_stack="python")

        assert stack_id == "python-fastapi"

    def test_select_stack_react(self):
        """Test React selection for frontend."""
        stack_id = self.selector.select_stack(["frontend", "web"])

        assert stack_id == "react-typescript"

    def test_select_stack_python_cli(self):
        """Test Python CLI selection."""
        stack_id = self.selector.select_stack(["cli"], preferred_stack="python-cli")

        assert stack_id == "python-cli"

    def test_select_stack_go_cli(self):
        """Test Go CLI selection."""
        stack_id = self.selector.select_stack(["cli"], preferred_stack="go")

        assert stack_id == "go-cli"

    def test_select_stack_python_ml(self):
        """Test Python ML selection."""
        stack_id = self.selector.select_stack(["data"])

        assert stack_id == "python-ml"

    def test_select_stack_default(self):
        """Test default stack selection."""
        stack_id = self.selector.select_stack([])

        assert stack_id == "nodejs-express"

    def test_get_stack_info(self):
        """Test getting stack information."""
        info = self.selector.get_stack_info("nodejs-express")

        assert info["name"] == "Node.js + Express"
        assert "web" in info["categories"]

    def test_get_dependencies_nodejs(self):
        """Test getting Node.js dependencies."""
        deps = self.selector.get_dependencies("nodejs-express")

        assert "express" in deps["dependencies"]
        assert "jest" in deps["dev_dependencies"]
        assert deps["runtime"] == "Node.js 18+"

    def test_get_dependencies_python_fastapi(self):
        """Test getting Python FastAPI dependencies."""
        deps = self.selector.get_dependencies("python-fastapi")

        assert "fastapi" in deps["dependencies"]
        assert "pytest" in deps["dev_dependencies"]

    def test_preferred_stack_normalization(self):
        """Test that preferred stack is normalized correctly."""
        stack_id = self.selector.select_stack([], preferred_stack="Node.js + Express")

        assert stack_id == "nodejs-express"
