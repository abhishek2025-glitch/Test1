"""Tests for code generator module."""
import pytest
from src.code_generator import CodeGenerator


class TestCodeGenerator:
    """Test cases for CodeGenerator."""

    def setup_method(self):
        """Setup test fixtures."""
        self.generator = CodeGenerator()

    def test_generate_nodejs_express_project(self):
        """Test Node.js Express project generation."""
        project_info = {
            "repo_name": "test-api",
            "repo_description": "Test API",
            "license": "MIT",
        }
        dependencies = {
            "dependencies": {"express": "^4.18.2"},
            "dev_dependencies": {"jest": "^29.7.0"},
        }

        files = self.generator._generate_nodejs_express(project_info, dependencies)

        assert "package.json" in files
        assert "src/app.js" in files
        assert "src/server.js" in files
        assert "tests/unit/health.test.js" in files
        assert "express" in files["package.json"]

    def test_generate_python_fastapi_project(self):
        """Test Python FastAPI project generation."""
        project_info = {
            "repo_name": "test-api",
            "repo_description": "Test API",
            "license": "MIT",
        }
        dependencies = {
            "dependencies": {"fastapi": "0.104.1"},
            "dev_dependencies": {"pytest": "7.4.3"},
        }

        files = self.generator._generate_python_fastapi(project_info, dependencies)

        assert "requirements.txt" in files
        assert "src/main.py" in files
        assert "src/api/routes/health.py" in files
        assert "tests/test_health.py" in files

    def test_generate_react_typescript_project(self):
        """Test React TypeScript project generation."""
        project_info = {
            "repo_name": "test-app",
            "repo_description": "Test App",
            "license": "MIT",
        }
        dependencies = {
            "dependencies": {"react": "^18.2.0"},
            "dev_dependencies": {"typescript": "^5.3.3"},
        }

        files = self.generator._generate_react_typescript(project_info, dependencies)

        assert "package.json" in files
        assert "src/App.tsx" in files
        assert "tsconfig.json" in files
        assert "index.html" in files

    def test_generate_python_cli_project(self):
        """Test Python CLI project generation."""
        project_info = {
            "repo_name": "test-cli",
            "repo_description": "Test CLI",
            "license": "MIT",
        }
        dependencies = {
            "dependencies": {"click": "8.1.7"},
            "dev_dependencies": {"pytest": "7.4.3"},
        }

        files = self.generator._generate_python_cli(project_info, dependencies)

        assert "requirements.txt" in files
        assert "src/cli.py" in files
        assert "setup.py" in files
        assert "tests/test_cli.py" in files

    def test_generate_gitignore_nodejs(self):
        """Test .gitignore generation for Node.js."""
        gitignore = self.generator._generate_gitignore("nodejs-express")

        assert "node_modules/" in gitignore
        assert ".env" in gitignore

    def test_generate_gitignore_python(self):
        """Test .gitignore generation for Python."""
        gitignore = self.generator._generate_gitignore("python-fastapi")

        assert "__pycache__/" in gitignore
        assert "venv/" in gitignore

    def test_generate_license(self):
        """Test LICENSE generation."""
        project_info = {"license": "MIT"}
        license_text = self.generator._generate_license(project_info)

        assert "MIT License" in license_text
        assert "Permission is hereby granted" in license_text

    def test_generate_readme(self):
        """Test README generation."""
        project_info = {
            "repo_name": "test-project",
            "repo_description": "Test project",
            "license": "MIT",
        }
        dependencies = {"runtime": "Node.js 18+"}

        readme = self.generator._generate_readme(
            "nodejs-express", project_info, dependencies
        )

        assert "# test-project" in readme
        assert "Node.js 18+" in readme
        assert "Setup" in readme
        assert "Testing" in readme

    def test_generate_ci_workflow_nodejs(self):
        """Test CI workflow generation for Node.js."""
        workflow = self.generator._generate_ci_workflow("nodejs-express")

        assert "name: CI" in workflow
        assert "setup-node@v3" in workflow
        assert "npm ci" in workflow

    def test_generate_ci_workflow_python(self):
        """Test CI workflow generation for Python."""
        workflow = self.generator._generate_ci_workflow("python-fastapi")

        assert "name: CI" in workflow
        assert "setup-python@v4" in workflow
        assert "pytest" in workflow

    def test_generate_project_includes_all_required_files(self):
        """Test that generate_project includes all required files."""
        project_info = {
            "repo_name": "test-project",
            "repo_description": "Test",
            "license": "MIT",
        }
        architecture = {"files": []}
        dependencies = {"dependencies": {}, "dev_dependencies": {}}

        files = self.generator.generate_project(
            "nodejs-express", architecture, project_info, dependencies
        )

        assert ".gitignore" in files
        assert ".env.example" in files
        assert "LICENSE" in files
        assert "README.md" in files
        assert ".github/workflows/ci.yml" in files
