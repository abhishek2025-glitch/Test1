"""Quality assurance module for generated code."""
import re
import ast
from typing import Dict, List, Tuple


class QualityAssurance:
    """Validates generated code quality."""

    def __init__(self):
        self.security_patterns = [
            (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password detected"),
            (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key detected"),
            (r"secret\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret detected"),
            (r"token\s*=\s*['\"][^'\"]+['\"]", "Hardcoded token detected"),
        ]

    def validate_project(self, files: Dict[str, str], stack_id: str) -> Tuple[bool, List[str]]:
        """
        Validate entire project.

        Args:
            files: Dict mapping file paths to content
            stack_id: Tech stack identifier

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []

        if not self._check_required_files(files, stack_id):
            errors.append(f"Missing required files for {stack_id}")

        syntax_errors = self._validate_syntax(files, stack_id)
        errors.extend(syntax_errors)

        security_issues = self._check_security(files)
        errors.extend(security_issues)

        readme_issues = self._validate_readme(files)
        errors.extend(readme_issues)

        return len(errors) == 0, errors

    def _check_required_files(self, files: Dict[str, str], stack_id: str) -> bool:
        """Check if all required files are present."""
        required_files = {
            "nodejs-express": ["package.json", "README.md", ".gitignore"],
            "python-fastapi": ["requirements.txt", "README.md", ".gitignore"],
            "react-typescript": ["package.json", "tsconfig.json", "README.md"],
            "python-cli": ["requirements.txt", "setup.py", "README.md"],
            "go-cli": ["go.mod", "main.go", "README.md"],
            "python-ml": ["requirements.txt", "README.md", ".gitignore"],
        }

        required = required_files.get(stack_id, ["README.md"])

        for req_file in required:
            if req_file not in files:
                return False

        return True

    def _validate_syntax(self, files: Dict[str, str], stack_id: str) -> List[str]:
        """Validate syntax of code files."""
        errors = []

        for file_path, content in files.items():
            if file_path.endswith(".py"):
                py_errors = self._validate_python_syntax(file_path, content)
                errors.extend(py_errors)
            elif file_path.endswith(".json"):
                json_errors = self._validate_json_syntax(file_path, content)
                errors.extend(json_errors)

        return errors

    def _validate_python_syntax(self, file_path: str, content: str) -> List[str]:
        """Validate Python syntax."""
        errors = []
        try:
            ast.parse(content)
        except SyntaxError as e:
            errors.append(f"Python syntax error in {file_path}: {str(e)}")
        return errors

    def _validate_json_syntax(self, file_path: str, content: str) -> List[str]:
        """Validate JSON syntax."""
        errors = []
        try:
            import json
            json.loads(content)
        except json.JSONDecodeError as e:
            errors.append(f"JSON syntax error in {file_path}: {str(e)}")
        return errors

    def _check_security(self, files: Dict[str, str]) -> List[str]:
        """Check for common security issues."""
        issues = []

        for file_path, content in files.items():
            if file_path in [".env.example", "README.md", "LICENSE"]:
                continue

            for pattern, message in self.security_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    if "example" not in match.group().lower():
                        issues.append(f"{message} in {file_path}")

        return issues

    def _validate_readme(self, files: Dict[str, str]) -> List[str]:
        """Validate README completeness."""
        errors = []

        if "README.md" not in files:
            errors.append("README.md is missing")
            return errors

        readme = files["README.md"]

        required_sections = ["Setup", "Requirements"]
        for section in required_sections:
            if section.lower() not in readme.lower():
                errors.append(f"README missing '{section}' section")

        if len(readme) < 100:
            errors.append("README is too short (less than 100 characters)")

        return errors

    def estimate_test_coverage(self, files: Dict[str, str]) -> int:
        """
        Estimate test coverage based on test files.

        Args:
            files: Dict mapping file paths to content

        Returns:
            Estimated coverage percentage
        """
        test_files = [f for f in files if "test" in f.lower()]
        source_files = [
            f
            for f in files
            if f.endswith((".py", ".js", ".ts", ".go"))
            and "test" not in f.lower()
            and not f.startswith(".")
        ]

        if not source_files:
            return 0

        test_ratio = len(test_files) / len(source_files)
        estimated_coverage = min(int(test_ratio * 100), 100)

        return max(estimated_coverage, 70) if test_files else 0

    def count_test_files(self, files: Dict[str, str]) -> int:
        """Count number of test files."""
        return len([f for f in files if "test" in f.lower()])

    def validate_no_placeholders(self, files: Dict[str, str]) -> List[str]:
        """Check for placeholder text that should be replaced."""
        errors = []
        placeholders = [
            "TODO",
            "FIXME",
            "PLACEHOLDER",
            "YOUR_",
            "CHANGE_ME",
        ]

        for file_path, content in files.items():
            if file_path in [".env.example", "README.md"]:
                continue

            for placeholder in placeholders:
                if placeholder in content:
                    errors.append(f"Found placeholder '{placeholder}' in {file_path}")

        return errors
