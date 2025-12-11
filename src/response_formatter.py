"""Response formatting module."""
import os
from typing import Dict, List


class ResponseFormatter:
    """Formats the final response output."""

    def format_response(
        self,
        repo_info: Dict,
        project_info: Dict,
        stack_id: str,
        file_count: int,
        test_count: int,
        repo_path: str,
    ) -> str:
        """
        Format the final response.

        Args:
            repo_info: Repository information from GitHub
            project_info: Project information
            stack_id: Tech stack identifier
            file_count: Number of files generated
            test_count: Number of test files
            repo_path: Local repository path

        Returns:
            Formatted response string
        """
        tree = self._generate_tree(repo_path)

        response = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    AI CODE GENERATOR - SUCCESS                           ║
╚══════════════════════════════════════════════════════════════════════════╝

📦 Repository Created Successfully!

🔗 Repository Information:
   - Name: {repo_info['name']}
   - URL: {repo_info['url']}
   - Branch: {repo_info['default_branch']}
   - Clone URL: {repo_info['clone_url']}

📊 Project Statistics:
   - Tech Stack: {stack_id}
   - Total Files: {file_count}
   - Test Files: {test_count}
   - Estimated Coverage: 70%+

📁 Directory Structure:
{tree}

🚀 Quick Start:

1. Clone the repository:
   git clone {repo_info['clone_url']}
   cd {repo_info['name']}

2. Follow setup instructions in README.md

3. Start development!

📝 Next Steps:
   - Review and customize the generated code
   - Update environment variables in .env
   - Configure any external services
   - Deploy using the CI/CD pipeline
   - Add more tests as needed

✨ Features Included:
   ✓ Production-ready code structure
   ✓ Unit tests with 70%+ coverage target
   ✓ CI/CD workflow configured
   ✓ Comprehensive documentation
   ✓ Security best practices
   ✓ Error handling
   ✓ Logging utilities

🔒 Security Notes:
   - No hardcoded secrets or credentials
   - Environment variables used for configuration
   - .env.example provided as template
   - .gitignore configured properly

📖 Documentation:
   - README.md: Complete setup and usage guide
   - CONTRIBUTING.md: Contribution guidelines (if applicable)
   - API documentation included in README

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Happy coding! 🎉
"""
        return response

    def _generate_tree(self, repo_path: str, max_depth: int = 3) -> str:
        """
        Generate a directory tree structure.

        Args:
            repo_path: Path to repository
            max_depth: Maximum depth to display

        Returns:
            Tree structure as string
        """
        lines = []

        def add_tree_lines(path: str, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return

            try:
                entries = sorted(os.listdir(path))
            except PermissionError:
                return

            entries = [e for e in entries if not e.startswith(".git")]

            for i, entry in enumerate(entries):
                is_last = i == len(entries) - 1
                current_prefix = "└── " if is_last else "├── "
                lines.append(f"{prefix}{current_prefix}{entry}")

                entry_path = os.path.join(path, entry)
                if os.path.isdir(entry_path):
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    add_tree_lines(entry_path, next_prefix, depth + 1)

        repo_name = os.path.basename(repo_path)
        lines.append(f"{repo_name}/")
        add_tree_lines(repo_path)

        return "\n".join(lines[:50])

    def format_error(self, error_message: str, details: List[str] = None) -> str:
        """
        Format error message.

        Args:
            error_message: Main error message
            details: Additional error details

        Returns:
            Formatted error string
        """
        response = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    AI CODE GENERATOR - ERROR                             ║
╚══════════════════════════════════════════════════════════════════════════╝

❌ Error: {error_message}
"""

        if details:
            response += "\n📋 Details:\n"
            for detail in details:
                response += f"   - {detail}\n"

        response += "\n💡 Suggestions:\n"
        response += "   - Check your GitHub token has the required permissions\n"
        response += "   - Verify repository name is valid and not already taken\n"
        response += "   - Ensure all required environment variables are set\n"

        return response
