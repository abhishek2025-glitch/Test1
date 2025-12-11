"""Tech stack selection logic based on project requirements."""
from typing import Dict, List, Optional


class TechStackSelector:
    """Intelligently selects appropriate tech stack for projects."""

    def __init__(self):
        self.stack_templates = {
            "nodejs-express": {
                "name": "Node.js + Express",
                "categories": ["web", "backend", "api"],
                "files": ["package.json", "src/server.js", "src/routes/"],
            },
            "python-fastapi": {
                "name": "Python + FastAPI",
                "categories": ["web", "backend", "api"],
                "files": ["requirements.txt", "src/main.py", "src/api/"],
            },
            "react-typescript": {
                "name": "React + TypeScript",
                "categories": ["frontend", "web"],
                "files": ["package.json", "src/App.tsx", "tsconfig.json"],
            },
            "python-cli": {
                "name": "Python CLI",
                "categories": ["cli"],
                "files": ["requirements.txt", "src/cli.py"],
            },
            "go-cli": {
                "name": "Go CLI",
                "categories": ["cli"],
                "files": ["go.mod", "main.go"],
            },
            "python-ml": {
                "name": "Python ML/Data Science",
                "categories": ["data"],
                "files": ["requirements.txt", "src/model.py", "notebooks/"],
            },
        }

    def select_stack(
        self, keywords: List[str], preferred_stack: Optional[str] = None
    ) -> str:
        """
        Select appropriate tech stack based on keywords and preferences.

        Args:
            keywords: List of extracted keywords from description
            preferred_stack: User's preferred tech stack

        Returns:
            Selected tech stack identifier
        """
        if preferred_stack:
            normalized = preferred_stack.lower().replace(" ", "-").replace("+", "-")
            for stack_id in self.stack_templates:
                if normalized in stack_id or stack_id in normalized:
                    return stack_id

        scores = {}
        for stack_id, stack_info in self.stack_templates.items():
            score = 0
            for keyword in keywords:
                if keyword in stack_info["categories"]:
                    score += 1
            scores[stack_id] = score

        if max(scores.values()) > 0:
            return max(scores, key=scores.get)

        return "nodejs-express"

    def get_stack_info(self, stack_id: str) -> Dict:
        """Get detailed information about a tech stack."""
        return self.stack_templates.get(
            stack_id, self.stack_templates["nodejs-express"]
        )

    def get_dependencies(self, stack_id: str) -> Dict:
        """Get dependencies for a specific tech stack."""
        dependencies = {
            "nodejs-express": {
                "runtime": "Node.js 18+",
                "package_manager": "npm",
                "dependencies": {
                    "express": "^4.18.2",
                    "dotenv": "^16.3.1",
                    "cors": "^2.8.5",
                    "helmet": "^7.1.0",
                },
                "dev_dependencies": {
                    "jest": "^29.7.0",
                    "supertest": "^6.3.3",
                    "eslint": "^8.55.0",
                    "nodemon": "^3.0.2",
                },
            },
            "python-fastapi": {
                "runtime": "Python 3.9+",
                "package_manager": "pip",
                "dependencies": {
                    "fastapi": "0.104.1",
                    "uvicorn": "0.24.0",
                    "pydantic": "2.5.2",
                    "python-dotenv": "1.0.0",
                },
                "dev_dependencies": {
                    "pytest": "7.4.3",
                    "pytest-asyncio": "0.21.1",
                    "httpx": "0.25.2",
                    "black": "23.12.1",
                    "pylint": "3.0.3",
                },
            },
            "react-typescript": {
                "runtime": "Node.js 18+",
                "package_manager": "npm",
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                },
                "dev_dependencies": {
                    "typescript": "^5.3.3",
                    "vite": "^5.0.7",
                    "@vitejs/plugin-react": "^4.2.1",
                    "@types/react": "^18.2.45",
                    "@types/react-dom": "^18.2.18",
                    "eslint": "^8.55.0",
                },
            },
            "python-cli": {
                "runtime": "Python 3.9+",
                "package_manager": "pip",
                "dependencies": {
                    "click": "8.1.7",
                    "rich": "13.7.0",
                },
                "dev_dependencies": {
                    "pytest": "7.4.3",
                    "black": "23.12.1",
                    "pylint": "3.0.3",
                },
            },
            "go-cli": {
                "runtime": "Go 1.21+",
                "package_manager": "go",
                "dependencies": {
                    "github.com/spf13/cobra": "v1.8.0",
                },
                "dev_dependencies": {},
            },
            "python-ml": {
                "runtime": "Python 3.9+",
                "package_manager": "pip",
                "dependencies": {
                    "pandas": "2.1.4",
                    "numpy": "1.26.2",
                    "scikit-learn": "1.3.2",
                    "matplotlib": "3.8.2",
                },
                "dev_dependencies": {
                    "pytest": "7.4.3",
                    "jupyter": "1.0.0",
                    "black": "23.12.1",
                },
            },
        }

        return dependencies.get(stack_id, dependencies["nodejs-express"])
