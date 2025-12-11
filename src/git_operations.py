"""Git operations module."""
import os
import shutil
from typing import Dict
from git import Repo, GitCommandError


class GitOperations:
    """Handles local git operations."""

    def __init__(self, base_dir: str = "generated_projects"):
        """
        Initialize git operations.

        Args:
            base_dir: Base directory for generated projects
        """
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def initialize_repository(self, repo_name: str) -> str:
        """
        Initialize a local git repository.

        Args:
            repo_name: Repository name

        Returns:
            Path to the initialized repository
        """
        repo_path = os.path.join(self.base_dir, repo_name)

        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        os.makedirs(repo_path)
        Repo.init(repo_path)

        return repo_path

    def create_project_structure(
        self, repo_path: str, files: Dict[str, str]
    ) -> None:
        """
        Create project files and directories.

        Args:
            repo_path: Path to repository
            files: Dict mapping file paths to content
        """
        for file_path, content in files.items():
            full_path = os.path.join(repo_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

    def commit_files(self, repo_path: str, message: str = "Initial commit") -> None:
        """
        Stage and commit all files.

        Args:
            repo_path: Path to repository
            message: Commit message
        """
        try:
            repo = Repo(repo_path)
            repo.git.add(A=True)
            repo.index.commit(message)
        except GitCommandError as e:
            raise Exception(f"Failed to commit files: {str(e)}")

    def add_remote(self, repo_path: str, remote_url: str, name: str = "origin") -> None:
        """
        Add remote to repository.

        Args:
            repo_path: Path to repository
            remote_url: Remote repository URL
            name: Remote name
        """
        try:
            repo = Repo(repo_path)

            if name in [remote.name for remote in repo.remotes]:
                repo.delete_remote(name)

            repo.create_remote(name, remote_url)
        except GitCommandError as e:
            raise Exception(f"Failed to add remote: {str(e)}")

    def push_to_remote(
        self,
        repo_path: str,
        branch: str = "main",
        remote: str = "origin",
        force: bool = False,
    ) -> None:
        """
        Push commits to remote repository.

        Args:
            repo_path: Path to repository
            branch: Branch name
            remote: Remote name
            force: Whether to force push
        """
        try:
            repo = Repo(repo_path)

            current_branch = repo.active_branch
            if current_branch.name != branch:
                if branch not in repo.heads:
                    repo.create_head(branch)
                repo.heads[branch].checkout()

            repo.git.push(remote, branch, force=force, set_upstream=True)

        except GitCommandError as e:
            raise Exception(f"Failed to push to remote: {str(e)}")

    def create_tag(self, repo_path: str, tag_name: str, message: str = "") -> None:
        """
        Create a git tag.

        Args:
            repo_path: Path to repository
            tag_name: Tag name
            message: Tag message
        """
        try:
            repo = Repo(repo_path)
            repo.create_tag(tag_name, message=message)
        except GitCommandError as e:
            raise Exception(f"Failed to create tag: {str(e)}")

    def push_tags(self, repo_path: str, remote: str = "origin") -> None:
        """
        Push tags to remote.

        Args:
            repo_path: Path to repository
            remote: Remote name
        """
        try:
            repo = Repo(repo_path)
            repo.git.push(remote, "--tags")
        except GitCommandError as e:
            raise Exception(f"Failed to push tags: {str(e)}")

    def get_file_count(self, repo_path: str) -> int:
        """
        Count files in repository.

        Args:
            repo_path: Path to repository

        Returns:
            Number of files
        """
        count = 0
        for root, dirs, files in os.walk(repo_path):
            if ".git" in root:
                continue
            count += len(files)
        return count

    def cleanup(self, repo_path: str) -> None:
        """
        Remove local repository directory.

        Args:
            repo_path: Path to repository
        """
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
