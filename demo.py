#!/usr/bin/env python3
"""Demo script for AI Code Generator."""
import sys
from src.main import AICodeGenerator


def run_demo():
    """Run a demo generation without GitHub push."""
    print("=" * 80)
    print("AI CODE GENERATOR - DEMO MODE")
    print("=" * 80)
    print("\nThis demo generates a sample project without pushing to GitHub.")
    print("To push to GitHub, remove --skip-github and set GITHUB_TOKEN.\n")

    generator = AICodeGenerator()

    result = generator.generate(
        description="Build a REST API for managing a todo list with CRUD operations",
        tech_stack="python-fastapi",
        features=["user authentication", "data validation"],
        repo_name="demo-todo-api",
        skip_github=True,
    )

    if result["success"]:
        print("\n✅ Demo completed successfully!")
        print(f"Generated {result.get('file_count', 'N/A')} files")
        print(f"Test files: {result.get('test_count', 'N/A')}")
        print("\nCheck generated_projects/demo-todo-api/ for the generated code")
    else:
        print(f"\n❌ Demo failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    run_demo()
