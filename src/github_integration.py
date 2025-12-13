"""GitHub API integration module."""
import os
from typing import Dict, Optional
from github import Github, GithubException


class GitHubIntegration:
    """Handles GitHub API operations."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub integration.

        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable.")

        self.github = Github(self.token)
        self.user = self.github.get_user()

    def create_repository(
        self,
        repo_name: str,
        description: str,
        private: bool = False,
        auto_init: bool = False,
    ) -> Dict:
        """
        Create a new GitHub repository.

        Args:
            repo_name: Repository name
            description: Repository description
            private: Whether repository should be private
            auto_init: Whether to initialize with README

        Returns:
            Dict containing repository information

        Raises:
            GithubException: If repository creation fails
        """
        try:
            repo = self.user.create_repo(
                name=repo_name,
                description=description,
                private=private,
                auto_init=auto_init,
                has_issues=True,
                has_projects=True,
                has_wiki=True,
            )

            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "url": repo.html_url,
                "clone_url": repo.clone_url,
                "ssh_url": repo.ssh_url,
                "default_branch": repo.default_branch,
            }

        except GithubException as e:
            if e.status == 422:
                raise ValueError(f"Repository '{repo_name}' already exists or name is invalid")
            raise Exception(f"Failed to create repository: {e.data.get('message', str(e))}")

    def add_topics(self, repo_name: str, topics: list) -> None:
        """
        Add topics to a repository.

        Args:
            repo_name: Repository name
            topics: List of topic strings
        """
        try:
            repo = self.user.get_repo(repo_name)
            repo.replace_topics(topics)
        except GithubException as e:
            raise Exception(f"Failed to add topics: {e.data.get('message', str(e))}")

    def create_release(
        self,
        repo_name: str,
        tag_name: str,
        release_name: str,
        body: str,
        draft: bool = False,
        prerelease: bool = False,
    ) -> Dict:
        """
        Create a release for the repository.

        Args:
            repo_name: Repository name
            tag_name: Git tag for the release
            release_name: Release name
            body: Release description
            draft: Whether release is a draft
            prerelease: Whether release is a prerelease

        Returns:
            Dict containing release information
        """
        try:
            repo = self.user.get_repo(repo_name)
            release = repo.create_git_release(
                tag=tag_name,
                name=release_name,
                message=body,
                draft=draft,
                prerelease=prerelease,
            )

            return {
                "tag_name": release.tag_name,
                "name": release.title,
                "url": release.html_url,
            }

        except GithubException as e:
            raise Exception(f"Failed to create release: {e.data.get('message', str(e))}")

    def set_branch_protection(
        self, repo_name: str, branch: str = "main"
    ) -> None:
        """
        Configure branch protection rules.

        Args:
            repo_name: Repository name
            branch: Branch name to protect
        """
        try:
            repo = self.user.get_repo(repo_name)
            branch_obj = repo.get_branch(branch)

            branch_obj.edit_protection(
                strict=True,
                enforce_admins=False,
                required_approving_review_count=1,
            )

        except GithubException as e:
            if e.status == 404:
                pass
            else:
                print(f"Warning: Could not set branch protection: {e.data.get('message', str(e))}")

    def check_repository_exists(self, repo_name: str) -> bool:
        """
        Check if a repository exists.

        Args:
            repo_name: Repository name

        Returns:
            True if repository exists, False otherwise
        """
        try:
            self.user.get_repo(repo_name)
            return True
        except GithubException:
            return False

    def get_user_info(self) -> Dict:
        """
        Get authenticated user information.

        Returns:
            Dict containing user information
        """
        return {
            "login": self.user.login,
            "name": self.user.name,
            "email": self.user.email,
            "avatar_url": self.user.avatar_url,
        }
