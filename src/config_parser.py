"""Configuration file parsing module for JSON and YAML formats."""
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

# Conditional import for YAML (optional)
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    yaml = None
    YAML_AVAILABLE = False


@dataclass
class ProjectConfig:
    """Configuration for a single project generation."""
    repo_name: str
    visibility: str = "public"
    description: str = ""
    topics: List[str] = None
    auto_validate: bool = True
    author: str = ""
    license: str = "MIT"
    prompt: str = ""
    
    def __post_init__(self):
        """Post-initialization processing."""
        if self.topics is None:
            self.topics = []
        self.visibility = self.visibility.lower()
        self.auto_validate = bool(self.auto_validate)


class ConfigParser:
    """Parser for project configuration files."""

    def __init__(self):
        self.valid_visibilities = ["public", "private"]
        self.valid_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC"]
        self.reserved_names = {
            "github", "git", "about", "api", "blog", "careers", "community",
            "dashboard", "downloads", "explore", "features", "help", "join",
            "login", "logout", "new", "notifications", "organizations", "pricing",
            "pulls", "repositories", "settings", "site", "stars", "timeline",
            "trending", "users", "watching"
        }

    def parse_project_config(
        self, config_path: str, prompt_path: Optional[str] = None
    ) -> ProjectConfig:
        """
        Parse project configuration from files.
        
        Args:
            config_path: Path to configuration file (.json or .yaml)
            prompt_path: Path to prompt file (.txt), optional for YAML with embedded prompt
            
        Returns:
            ProjectConfig object with parsed configuration
            
        Raises:
            ValueError: If configuration is invalid
            FileNotFoundError: If required files don't exist
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        file_ext = config_path.suffix.lower()
        
        if file_ext == ".json":
            return self._parse_json_config(config_path, prompt_path)
        elif file_ext in [".yaml", ".yml"]:
            if not YAML_AVAILABLE:
                raise ValueError("YAML support not available. Please install PyYAML: pip install PyYAML")
            return self._parse_yaml_config(config_path)
        else:
            raise ValueError(f"Unsupported configuration file format: {file_ext}")

    def _parse_json_config(self, config_path: Path, prompt_path: Optional[str]) -> ProjectConfig:
        """Parse JSON configuration with separate prompt file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
        
        # Load prompt from separate file if specified
        prompt_content = ""
        if prompt_path:
            prompt_path = Path(prompt_path)
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
        elif "prompt" in config_data:
            prompt_content = config_data["prompt"]
        else:
            raise ValueError("Prompt content not found - specify prompt file or include in config")
        
        return self._validate_and_create_config(config_data, prompt_content, config_path.name)

    def _parse_yaml_config(self, config_path: Path) -> ProjectConfig:
        """Parse YAML configuration with embedded prompt."""
        if not YAML_AVAILABLE:
            raise ValueError("YAML support not available. Please install PyYAML: pip install PyYAML")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {config_path}: {e}")
        
        if not isinstance(config_data, dict):
            raise ValueError(f"YAML file {config_path} must contain a dictionary")
        
        # Extract prompt from YAML
        prompt_content = config_data.get("prompt", "")
        if not prompt_content:
            raise ValueError("Prompt content not found in YAML configuration")
        
        return self._validate_and_create_config(config_data, prompt_content, config_path.name)

    def _validate_and_create_config(
        self, config_data: dict, prompt_content: str, config_file: str
    ) -> ProjectConfig:
        """Validate configuration data and create ProjectConfig."""
        # Extract configuration values
        repo_name = config_data.get("repoName") or config_data.get("repo_name")
        if not repo_name:
            raise ValueError("Repository name (repoName) is required")
        
        # Clean and validate repo name
        repo_name = self._sanitize_repo_name(repo_name)
        self._validate_repo_name(repo_name)
        
        # Validate other fields
        visibility = config_data.get("visibility", "public")
        if visibility not in self.valid_visibilities:
            raise ValueError(f"Invalid visibility '{visibility}'. Must be one of: {self.valid_visibilities}")
        
        topics = config_data.get("topics", [])
        if not isinstance(topics, list):
            raise ValueError("Topics must be a list")
        
        license_type = config_data.get("license", "MIT")
        if license_type not in self.valid_licenses:
            raise ValueError(f"Invalid license '{license_type}'. Must be one of: {self.valid_licenses}")
        
        auto_validate = config_data.get("autoValidate", True)
        author = config_data.get("author", "")
        description = config_data.get("description", "")
        
        return ProjectConfig(
            repo_name=repo_name,
            visibility=visibility,
            description=description,
            topics=topics,
            auto_validate=auto_validate,
            author=author,
            license=license_type,
            prompt=prompt_content
        )

    def _sanitize_repo_name(self, name: str) -> str:
        """Sanitize repository name to meet GitHub requirements."""
        # Remove special characters, keep alphanumeric, hyphens, underscores, periods
        name = re.sub(r"[^a-zA-Z0-9-_.]", "-", name)
        # Replace multiple consecutive hyphens with single hyphen
        name = re.sub(r"-+", "-", name)
        # Remove leading/trailing special characters
        name = name.strip("-._")
        # Limit length (GitHub allows up to 100 characters, but 39 is more user-friendly)
        return name[:39] if name else "generated-project"

    def _validate_repo_name(self, name: str) -> None:
        """Validate repository name against GitHub rules."""
        if not name:
            raise ValueError("Repository name cannot be empty")
        
        if len(name) < 3:
            raise ValueError("Repository name must be at least 3 characters")
        
        if len(name) > 100:
            raise ValueError("Repository name must be 100 characters or less")
        
        if name.lower() in self.reserved_names:
            raise ValueError(f"Repository name '{name}' is reserved and cannot be used")
        
        if not re.match(r"^[a-zA-Z0-9-_.]+$", name):
            raise ValueError(
                "Repository name can only contain alphanumeric characters, hyphens, underscores, and periods"
            )

    def find_prompt_files(self, prompts_dir: str) -> List[Tuple[str, Optional[str], str]]:
        """
        Find all prompt configuration files in a directory.
        
        Returns:
            List of tuples: (config_path, prompt_path, file_type)
            where file_type is 'yaml', 'json', or 'invalid'
        """
        prompts_path = Path(prompts_dir)
        if not prompts_path.exists():
            raise FileNotFoundError(f"Prompts directory not found: {prompts_dir}")
        
        files_found = []
        
        # Find YAML files with embedded prompts
        for yaml_file in prompts_path.glob("*.yaml"):
            files_found.append((str(yaml_file), None, "yaml"))
        for yml_file in prompts_path.glob("*.yml"):
            files_found.append((str(yml_file), None, "yaml"))
        
        # Find JSON config files and their corresponding prompt files
        for json_file in prompts_path.glob("*.config.json"):
            # Look for corresponding .txt file
            base_name = json_file.stem.replace(".config", "")
            txt_file = json_file.parent / f"{base_name}.txt"
            
            if txt_file.exists():
                files_found.append((str(json_file), str(txt_file), "json"))
            else:
                # Also check if prompt is embedded in JSON
                files_found.append((str(json_file), None, "json"))
        
        return sorted(files_found)

    def validate_config_file(self, config_path: str) -> Dict[str, Union[bool, List[str]]]:
        """
        Validate a configuration file without fully parsing it.
        
        Returns:
            Dict with 'valid' boolean and 'errors' list of issues
        """
        result = {"valid": True, "errors": []}
        
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                result["valid"] = False
                result["errors"].append(f"File not found: {config_path}")
                return result
            
            file_ext = config_path.suffix.lower()
            
            if file_ext == ".json":
                try:
                    with open(config_path, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    result["valid"] = False
                    result["errors"].append(f"Invalid JSON: {e}")
            
            elif file_ext in [".yaml", ".yml"]:
                try:
                    with open(config_path, 'r') as f:
                        yaml.safe_load(f)
                except yaml.YAMLError as e:
                    result["valid"] = False
                    result["errors"].append(f"Invalid YAML: {e}")
            else:
                result["valid"] = False
                result["errors"].append(f"Unsupported file format: {file_ext}")
        
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Validation error: {e}")
        
        return result