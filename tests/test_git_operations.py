"""Tests for git operations module."""
import pytest
import tempfile
import os
from src.git_operations import GitOperations


class TestGitOperations:
    """Test cases for GitOperations."""

    def test_initialize_repository(self):
        """Test repository initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            git_ops = GitOperations(base_dir=tmpdir)
            repo_path = git_ops.initialize_repository("test-repo")

            assert os.path.exists(repo_path)
            assert os.path.exists(os.path.join(repo_path, ".git"))

    def test_create_project_structure(self):
        """Test creating project files and directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            git_ops = GitOperations(base_dir=tmpdir)
            repo_path = git_ops.initialize_repository("test-repo")

            files = {
                "README.md": "# Test Project",
                "src/main.py": "print('hello')",
                "tests/test_main.py": "def test(): pass",
            }

            git_ops.create_project_structure(repo_path, files)

            assert os.path.exists(os.path.join(repo_path, "README.md"))
            assert os.path.exists(os.path.join(repo_path, "src", "main.py"))
            assert os.path.exists(os.path.join(repo_path, "tests", "test_main.py"))

            with open(os.path.join(repo_path, "README.md")) as f:
                assert f.read() == "# Test Project"

    def test_commit_files(self):
        """Test committing files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            git_ops = GitOperations(base_dir=tmpdir)
            repo_path = git_ops.initialize_repository("test-repo")

            files = {"README.md": "# Test"}
            git_ops.create_project_structure(repo_path, files)
            git_ops.commit_files(repo_path, "Initial commit")

    def test_get_file_count(self):
        """Test counting files in repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            git_ops = GitOperations(base_dir=tmpdir)
            repo_path = git_ops.initialize_repository("test-repo")

            files = {
                "README.md": "# Test",
                "src/main.py": "print('hello')",
                "tests/test_main.py": "def test(): pass",
            }
            git_ops.create_project_structure(repo_path, files)

            count = git_ops.get_file_count(repo_path)
            assert count == 3

    def test_cleanup(self):
        """Test repository cleanup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            git_ops = GitOperations(base_dir=tmpdir)
            repo_path = git_ops.initialize_repository("test-repo")

            assert os.path.exists(repo_path)
            
            git_ops.cleanup(repo_path)
            assert not os.path.exists(repo_path)
