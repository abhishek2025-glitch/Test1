"""Input processing and validation module."""
from typing import Dict, List, Optional
import re


class InputProcessor:
    """Processes and validates user input for code generation."""

    def __init__(self):
        self.valid_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC"]

    def process_input(
        self,
        description: str,
        tech_stack: Optional[str] = None,
        features: Optional[List[str]] = None,
        repo_name: Optional[str] = None,
        repo_description: Optional[str] = None,
        is_private: bool = False,
        license_type: str = "MIT",
    ) -> Dict:
        """
        Process and validate all inputs.

        Args:
            description: Natural language project description
            tech_stack: Preferred tech stack (optional)
            features: List of features to implement
            repo_name: GitHub repository name
            repo_description: Repository description
            is_private: Whether repo should be private
            license_type: License type (default: MIT)

        Returns:
            Dict containing validated and processed inputs
        """
        if not description or not description.strip():
            raise ValueError("Project description is required")

        processed = {
            "description": description.strip(),
            "tech_stack": tech_stack.strip() if tech_stack else None,
            "features": features or [],
            "repo_name": self._generate_repo_name(repo_name, description),
            "repo_description": repo_description or description[:100],
            "is_private": is_private,
            "license": license_type if license_type in self.valid_licenses else "MIT",
        }

        self._validate_repo_name(processed["repo_name"])

        return processed

    def _generate_repo_name(self, repo_name: Optional[str], description: str) -> str:
        """Generate a valid repository name."""
        if repo_name and repo_name.strip():
            return self._sanitize_repo_name(repo_name.strip())

        words = description.lower().split()[:3]
        name = "-".join(words)
        return self._sanitize_repo_name(name)

    def _sanitize_repo_name(self, name: str) -> str:
        """Sanitize repository name to meet GitHub requirements."""
        name = re.sub(r"[^a-zA-Z0-9-_.]", "-", name)
        name = re.sub(r"-+", "-", name)
        name = name.strip("-._")
        return name[:100] if name else "generated-project"

    def _validate_repo_name(self, name: str) -> None:
        """Validate repository name."""
        if not name:
            raise ValueError("Repository name cannot be empty")
        if len(name) > 100:
            raise ValueError("Repository name must be 100 characters or less")
        if not re.match(r"^[a-zA-Z0-9-_.]+$", name):
            raise ValueError(
                "Repository name can only contain alphanumeric characters, hyphens, underscores, and periods"
            )

    def extract_keywords(self, description: str) -> List[str]:
        """Extract keywords from project description for tech stack detection."""
        description_lower = description.lower()
        keywords = []

        keyword_map = {
            "web": ["web", "website", "webapp", "api", "rest", "http", "server"],
            "frontend": [
                "frontend",
                "front-end",
                "ui",
                "interface",
                "react",
                "vue",
                "angular",
            ],
            "backend": [
                "backend",
                "back-end",
                "api",
                "server",
                "database",
                "rest",
            ],
            "mobile": ["mobile", "ios", "android", "app", "native"],
            "cli": ["cli", "command-line", "command line", "terminal", "tool", "script"],
            "data": [
                "data",
                "analytics",
                "ml",
                "machine learning",
                "ai",
                "analysis",
            ],
            "devops": ["devops", "infrastructure", "deployment", "ci/cd", "docker"],
        }

        for category, words in keyword_map.items():
            # Use word boundaries to avoid partial matches
            import re
            for word in words:
                if re.search(r'\b' + re.escape(word) + r'\b', description_lower):
                    keywords.append(category)
                    break

        return keywords
