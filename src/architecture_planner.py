"""Architecture planning module for code generation."""
from typing import Dict, List


class ArchitecturePlanner:
    """Plans project architecture and file structure."""

    def plan_architecture(
        self, stack_id: str, features: List[str], description: str
    ) -> Dict:
        """
        Plan project architecture based on tech stack and features.

        Args:
            stack_id: Selected tech stack identifier
            features: List of requested features
            description: Project description

        Returns:
            Dict containing architecture plan
        """
        base_structures = {
            "nodejs-express": {
                "directories": [
                    "src",
                    "src/routes",
                    "src/controllers",
                    "src/middleware",
                    "src/models",
                    "src/utils",
                    "tests",
                    "tests/unit",
                    "tests/integration",
                ],
                "files": [
                    "src/server.js",
                    "src/app.js",
                    "src/routes/index.js",
                    "src/controllers/healthController.js",
                    "src/middleware/errorHandler.js",
                    "src/utils/logger.js",
                    "tests/unit/health.test.js",
                    "tests/integration/api.test.js",
                    "package.json",
                    ".eslintrc.json",
                    ".gitignore",
                    ".env.example",
                    "README.md",
                    "LICENSE",
                ],
            },
            "python-fastapi": {
                "directories": [
                    "src",
                    "src/api",
                    "src/api/routes",
                    "src/models",
                    "src/services",
                    "src/core",
                    "tests",
                    "tests/unit",
                    "tests/integration",
                ],
                "files": [
                    "src/main.py",
                    "src/api/routes/health.py",
                    "src/core/config.py",
                    "src/core/security.py",
                    "tests/test_health.py",
                    "tests/conftest.py",
                    "requirements.txt",
                    "pytest.ini",
                    ".gitignore",
                    ".env.example",
                    "README.md",
                    "LICENSE",
                ],
            },
            "react-typescript": {
                "directories": [
                    "src",
                    "src/components",
                    "src/hooks",
                    "src/utils",
                    "src/types",
                    "src/styles",
                    "public",
                    "tests",
                ],
                "files": [
                    "src/main.tsx",
                    "src/App.tsx",
                    "src/components/Header.tsx",
                    "src/vite-env.d.ts",
                    "index.html",
                    "package.json",
                    "tsconfig.json",
                    "vite.config.ts",
                    ".eslintrc.json",
                    ".gitignore",
                    "README.md",
                    "LICENSE",
                ],
            },
            "python-cli": {
                "directories": ["src", "src/commands", "src/utils", "tests"],
                "files": [
                    "src/cli.py",
                    "src/__init__.py",
                    "src/commands/__init__.py",
                    "src/commands/main.py",
                    "tests/test_cli.py",
                    "requirements.txt",
                    "setup.py",
                    "pytest.ini",
                    ".gitignore",
                    "README.md",
                    "LICENSE",
                ],
            },
            "go-cli": {
                "directories": ["cmd", "pkg", "internal", "tests"],
                "files": [
                    "main.go",
                    "cmd/root.go",
                    "go.mod",
                    ".gitignore",
                    "README.md",
                    "LICENSE",
                ],
            },
            "python-ml": {
                "directories": [
                    "src",
                    "src/data",
                    "src/models",
                    "src/features",
                    "notebooks",
                    "tests",
                    "data",
                    "data/raw",
                    "data/processed",
                ],
                "files": [
                    "src/model.py",
                    "src/train.py",
                    "src/predict.py",
                    "notebooks/exploration.ipynb",
                    "tests/test_model.py",
                    "requirements.txt",
                    ".gitignore",
                    "README.md",
                    "LICENSE",
                ],
            },
        }

        structure = base_structures.get(
            stack_id, base_structures["nodejs-express"]
        ).copy()

        structure["workflow_file"] = ".github/workflows/ci.yml"
        structure["directories"].append(".github")
        structure["directories"].append(".github/workflows")
        structure["files"].append(".github/workflows/ci.yml")

        return structure

    def generate_api_design(self, features: List[str]) -> Dict:
        """Generate API endpoint design based on features."""
        endpoints = []

        endpoints.append(
            {
                "method": "GET",
                "path": "/health",
                "description": "Health check endpoint",
                "response": {"status": "ok"},
            }
        )

        for feature in features:
            feature_lower = feature.lower()
            if "user" in feature_lower or "auth" in feature_lower:
                endpoints.extend(
                    [
                        {
                            "method": "POST",
                            "path": "/api/users",
                            "description": "Create new user",
                        },
                        {
                            "method": "GET",
                            "path": "/api/users/:id",
                            "description": "Get user by ID",
                        },
                    ]
                )
            elif "product" in feature_lower or "item" in feature_lower:
                endpoints.extend(
                    [
                        {
                            "method": "GET",
                            "path": "/api/items",
                            "description": "List all items",
                        },
                        {
                            "method": "POST",
                            "path": "/api/items",
                            "description": "Create new item",
                        },
                    ]
                )

        return {"endpoints": endpoints}
