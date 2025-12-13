"""Main entry point for AI Code Generator."""
import os
import sys
from typing import Dict, List, Optional
import click
from dotenv import load_dotenv

from src.input_processor import InputProcessor
from src.tech_stack_selector import TechStackSelector
from src.architecture_planner import ArchitecturePlanner
from src.code_generator import CodeGenerator
from src.quality_assurance import QualityAssurance
from src.github_integration import GitHubIntegration
from src.git_operations import GitOperations
from src.response_formatter import ResponseFormatter


load_dotenv()


class AICodeGenerator:
    """Main AI Code Generator orchestrator."""

    def __init__(self):
        self.input_processor = InputProcessor()
        self.tech_stack_selector = TechStackSelector()
        self.architecture_planner = ArchitecturePlanner()
        self.code_generator = CodeGenerator()
        self.quality_assurance = QualityAssurance()
        self.response_formatter = ResponseFormatter()

    def generate(
        self,
        description: str,
        tech_stack: Optional[str] = None,
        features: Optional[List[str]] = None,
        repo_name: Optional[str] = None,
        repo_description: Optional[str] = None,
        is_private: bool = False,
        license_type: str = "MIT",
        github_token: Optional[str] = None,
        skip_github: bool = False,
    ) -> Dict:
        """
        Generate complete project and push to GitHub.

        Args:
            description: Natural language project description
            tech_stack: Preferred tech stack (optional)
            features: List of features to implement
            repo_name: GitHub repository name
            repo_description: Repository description
            is_private: Whether repo should be private
            license_type: License type
            github_token: GitHub token (optional, uses env var if not provided)
            skip_github: Skip GitHub creation (for testing)

        Returns:
            Dict containing generation results
        """
        try:
            click.echo("🚀 Starting AI Code Generator...\n")

            click.echo("📝 Step 1/7: Processing input...")
            project_info = self.input_processor.process_input(
                description=description,
                tech_stack=tech_stack,
                features=features,
                repo_name=repo_name,
                repo_description=repo_description,
                is_private=is_private,
                license_type=license_type,
            )
            click.echo(f"   ✓ Project name: {project_info['repo_name']}")

            click.echo("\n🔍 Step 2/7: Selecting tech stack...")
            keywords = self.input_processor.extract_keywords(description)
            stack_id = self.tech_stack_selector.select_stack(keywords, tech_stack)
            stack_info = self.tech_stack_selector.get_stack_info(stack_id)
            dependencies = self.tech_stack_selector.get_dependencies(stack_id)
            click.echo(f"   ✓ Selected: {stack_info['name']}")

            click.echo("\n🏗️  Step 3/7: Planning architecture...")
            architecture = self.architecture_planner.plan_architecture(
                stack_id, project_info["features"], description
            )
            click.echo(f"   ✓ Planned {len(architecture['files'])} files")

            click.echo("\n💻 Step 4/7: Generating code...")
            files = self.code_generator.generate_project(
                stack_id, architecture, project_info, dependencies
            )
            click.echo(f"   ✓ Generated {len(files)} files")

            click.echo("\n🔒 Step 5/7: Running quality checks...")
            is_valid, errors = self.quality_assurance.validate_project(files, stack_id)
            if not is_valid:
                click.echo("   ⚠️  Quality issues detected:")
                for error in errors:
                    click.echo(f"      - {error}")
                if not click.confirm("\n   Continue anyway?", default=True):
                    raise Exception("Quality validation failed")
            else:
                click.echo("   ✓ All quality checks passed")

            test_count = self.quality_assurance.count_test_files(files)
            coverage = self.quality_assurance.estimate_test_coverage(files)
            click.echo(f"   ✓ Test files: {test_count}, Estimated coverage: {coverage}%")

            if skip_github:
                click.echo("\n⏭️  Skipping GitHub integration (skip_github=True)")
                return {
                    "success": True,
                    "repo_info": None,
                    "project_info": project_info,
                    "files": files,
                    "message": "Code generated successfully (GitHub push skipped)",
                }

            click.echo("\n📦 Step 6/7: Creating GitHub repository...")
            github_integration = GitHubIntegration(token=github_token)

            if github_integration.check_repository_exists(project_info["repo_name"]):
                raise ValueError(
                    f"Repository '{project_info['repo_name']}' already exists. "
                    "Please choose a different name."
                )

            repo_info = github_integration.create_repository(
                repo_name=project_info["repo_name"],
                description=project_info["repo_description"],
                private=is_private,
                auto_init=False,
            )
            click.echo(f"   ✓ Created: {repo_info['url']}")

            click.echo("\n🔄 Step 7/7: Pushing code to GitHub...")
            git_ops = GitOperations()

            repo_path = git_ops.initialize_repository(project_info["repo_name"])
            click.echo("   ✓ Initialized local repository")

            git_ops.create_project_structure(repo_path, files)
            click.echo("   ✓ Created project structure")

            git_ops.commit_files(repo_path, "Initial commit: AI-generated project")
            click.echo("   ✓ Committed files")

            git_ops.add_remote(repo_path, repo_info["clone_url"])
            click.echo("   ✓ Added remote")

            git_ops.push_to_remote(repo_path, branch="main", force=True)
            click.echo("   ✓ Pushed to GitHub")

            topics = keywords + [stack_id.replace("-", ""), "ai-generated"]
            github_integration.add_topics(project_info["repo_name"], topics[:5])
            click.echo("   ✓ Added repository topics")

            git_ops.create_tag(repo_path, "v0.1.0", "Initial release")
            git_ops.push_tags(repo_path)

            github_integration.create_release(
                repo_name=project_info["repo_name"],
                tag_name="v0.1.0",
                release_name="Initial Release v0.1.0",
                body=f"🎉 Initial release of {project_info['repo_name']}\n\n"
                f"Generated by AI Code Generator\n\n"
                f"Tech Stack: {stack_info['name']}\n"
                f"Files: {len(files)}\n"
                f"Tests: {test_count}",
                prerelease=True,
            )
            click.echo("   ✓ Created release v0.1.0")

            click.echo("\n" + "=" * 80)
            response = self.response_formatter.format_response(
                repo_info=repo_info,
                project_info=project_info,
                stack_id=stack_id,
                file_count=len(files),
                test_count=test_count,
                repo_path=repo_path,
            )
            click.echo(response)

            return {
                "success": True,
                "repo_info": repo_info,
                "project_info": project_info,
                "stack_id": stack_id,
                "file_count": len(files),
                "test_count": test_count,
                "coverage": coverage,
                "message": "Project generated and pushed successfully!",
            }

        except Exception as e:
            error_response = self.response_formatter.format_error(
                str(e), [f"Error type: {type(e).__name__}"]
            )
            click.echo(error_response)
            return {"success": False, "error": str(e)}


@click.command()
@click.option(
    "--description",
    "-d",
    required=True,
    help="Natural language project description",
)
@click.option("--tech-stack", "-t", help="Preferred tech stack (optional)")
@click.option(
    "--features",
    "-f",
    multiple=True,
    help="Features to implement (can specify multiple)",
)
@click.option("--repo-name", "-n", help="Repository name (auto-generated if not provided)")
@click.option("--repo-description", help="Repository description")
@click.option("--private", is_flag=True, help="Make repository private")
@click.option("--license", default="MIT", help="License type (default: MIT)")
@click.option("--skip-github", is_flag=True, help="Skip GitHub operations (testing)")
def main(
    description: str,
    tech_stack: Optional[str],
    features: tuple,
    repo_name: Optional[str],
    repo_description: Optional[str],
    private: bool,
    license: str,
    skip_github: bool,
):
    """
    AI Code Generator - Generate production-ready code and push to GitHub.

    Example:
        python -m src.main -d "Build a REST API for todo management" -t "python-fastapi"
    """
    generator = AICodeGenerator()

    result = generator.generate(
        description=description,
        tech_stack=tech_stack,
        features=list(features) if features else None,
        repo_name=repo_name,
        repo_description=repo_description,
        is_private=private,
        license_type=license,
        skip_github=skip_github,
    )

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
