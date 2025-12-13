"""Repository name validation and management module."""
import time
from typing import Dict, List, Optional, Tuple

# Conditional imports for GitHub API (optional)
try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    Github = None
    GithubException = None
    GITHUB_AVAILABLE = False

try:
    from src.github_integration import GitHubIntegration
    GITHUB_INTEGRATION_AVAILABLE = True
except ImportError:
    GitHubIntegration = None
    GITHUB_INTEGRATION_AVAILABLE = False


class RepositoryValidator:
    """Validates repository names and suggests alternatives."""

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize repository validator.
        
        Args:
            github_token: GitHub Personal Access Token for API access
        """
        if not GITHUB_INTEGRATION_AVAILABLE:
            raise ImportError("GitHub integration not available. Install PyGithub for full functionality.")
        
        self.github_integration = GitHubIntegration(token=github_token)
        self.checked_names = set()
        self.suggestions_cache = {}
        self.offline_mode = False  # Set to True if GitHub API is not available

    def validate_repo_name(
        self, 
        repo_name: str, 
        user_login: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Validate a repository name and provide suggestions if needed.
        
        Args:
            repo_name: Repository name to validate
            user_login: GitHub username (optional, will use authenticated user if not provided)
            
        Returns:
            Dict with validation results and suggestions
        """
        validation_result = {
            "original_name": repo_name,
            "is_valid": False,
            "exists": False,
            "suggestions": [],
            "timestamp": int(time.time()),
            "user": user_login or self.github_integration.user.login,
            "status": "unknown"
        }
        
        try:
            # Check if repository already exists
            repo_exists = self.github_integration.check_repository_exists(repo_name)
            validation_result["exists"] = repo_exists
            
            # Check if name is technically valid (format, length, etc.)
            is_technically_valid = self._check_technical_validity(repo_name)
            
            if repo_exists:
                validation_result["status"] = "exists"
                validation_result["suggestions"] = self._generate_suggestions(repo_name)
                validation_result["is_valid"] = False
            elif not is_technically_valid:
                validation_result["status"] = "invalid_format"
                validation_result["suggestions"] = self._generate_format_suggestions(repo_name)
                validation_result["is_valid"] = False
            else:
                validation_result["status"] = "valid"
                validation_result["is_valid"] = True
                # Add timestamp suggestion as alternative
                timestamp_suggestion = f"{repo_name}-{int(time.time())}"
                validation_result["suggestions"].append({
                    "name": timestamp_suggestion,
                    "reason": "timestamp_suffix",
                    "available": True
                })
            
            # Cache the result
            self.checked_names.add(repo_name)
            self.suggestions_cache[repo_name] = validation_result
            
        except GithubException as e:
            validation_result["status"] = "api_error"
            validation_result["error"] = str(e)
            validation_result["is_valid"] = False
            
        except Exception as e:
            validation_result["status"] = "validation_error"
            validation_result["error"] = str(e)
            validation_result["is_valid"] = False
        
        return validation_result

    def validate_multiple_names(
        self, 
        repo_names: List[str], 
        user_login: Optional[str] = None
    ) -> Dict[str, Dict]:
        """
        Validate multiple repository names at once.
        
        Args:
            repo_names: List of repository names to validate
            user_login: GitHub username (optional)
            
        Returns:
            Dict mapping repo names to validation results
        """
        results = {}
        
        for repo_name in repo_names:
            results[repo_name] = self.validate_repo_name(repo_name, user_login)
        
        return results

    def _check_technical_validity(self, repo_name: str) -> bool:
        """
        Check if a repository name meets GitHub's technical requirements.
        
        Args:
            repo_name: Repository name to check
            
        Returns:
            True if name is technically valid, False otherwise
        """
        import re
        
        if not repo_name or len(repo_name) < 3:
            return False
        
        if len(repo_name) > 100:
            return False
        
        # Check for valid characters (alphanumeric, hyphens, underscores, periods)
        if not re.match(r"^[a-zA-Z0-9-_.]+$", repo_name):
            return False
        
        # Check for reserved names
        reserved_names = {
            "github", "git", "about", "api", "blog", "careers", "community",
            "dashboard", "downloads", "explore", "features", "help", "join",
            "login", "logout", "new", "notifications", "organizations", "pricing",
            "pulls", "repositories", "settings", "site", "stars", "timeline",
            "trending", "users", "watching"
        }
        
        if repo_name.lower() in reserved_names:
            return False
        
        # Can't start or end with special characters
        if repo_name.startswith(('-', '.', '_')) or repo_name.endswith(('-', '.', '_')):
            return False
        
        return True

    def _generate_suggestions(self, original_name: str) -> List[Dict[str, any]]:
        """
        Generate alternative repository names when the original is taken.
        
        Args:
            original_name: The original repository name
            
        Returns:
            List of suggestion dictionaries
        """
        suggestions = []
        
        # 1. Timestamp-based suggestions
        current_timestamp = int(time.time())
        suggestions.append({
            "name": f"{original_name}-{current_timestamp}",
            "reason": "timestamp_suffix",
            "available": None  # Will be checked
        })
        
        # 2. Simple counter-based suggestions
        for i in range(2, 6):  # Try up to 5 alternatives
            counter_name = f"{original_name}-{i}"
            suggestions.append({
                "name": counter_name,
                "reason": "counter_suffix",
                "available": None  # Will be checked
            })
        
        # 3. Variant suggestions
        variants = self._generate_name_variants(original_name)
        for variant in variants[:3]:  # Limit to 3 variants
            suggestions.append({
                "name": variant,
                "reason": "name_variant",
                "available": None  # Will be checked
            })
        
        # Check availability of suggestions
        return self._check_suggestions_availability(suggestions)

    def _generate_format_suggestions(self, original_name: str) -> List[Dict[str, any]]:
        """
        Generate suggestions for technically invalid names.
        
        Args:
            original_name: The invalid repository name
            
        Returns:
            List of suggestion dictionaries
        """
        suggestions = []
        
        # Clean up the name
        import re
        cleaned = re.sub(r"[^a-zA-Z0-9-_.]", "-", original_name)
        cleaned = re.sub(r"-+", "-", cleaned)
        cleaned = cleaned.strip("-._")
        
        if cleaned and len(cleaned) >= 3:
            suggestions.append({
                "name": cleaned,
                "reason": "cleaned_format",
                "available": None
            })
        
        # If too long, suggest truncations
        if len(original_name) > 100:
            truncated = original_name[:39]  # Reasonable length
            suggestions.append({
                "name": truncated,
                "reason": "truncated",
                "available": None
            })
        
        # If too short, suggest with keywords
        if len(original_name) < 3:
            suggestions.append({
                "name": f"my-{original_name}",
                "reason": "prefixed",
                "available": None
            })
            suggestions.append({
                "name": f"{original_name}-project",
                "reason": "suffixed",
                "available": None
            })
        
        return suggestions

    def _generate_name_variants(self, name: str) -> List[str]:
        """
        Generate variant names from the original.
        
        Args:
            name: Original repository name
            
        Returns:
            List of variant names
        """
        variants = []
        
        # Replace hyphens with underscores
        variants.append(name.replace('-', '_'))
        variants.append(name.replace('_', '-'))
        
        # Remove hyphens/underscores
        variants.append(name.replace('-', '').replace('_', ''))
        
        # Add common suffixes
        variants.append(f"{name}-app")
        variants.append(f"{name}-tool")
        variants.append(f"{name}-lib")
        variants.append(f"{name}-service")
        variants.append(f"awesome-{name}")
        variants.append(f"super-{name}")
        variants.append(f"my-{name}")
        
        # Remove duplicates and invalid ones
        unique_variants = []
        for variant in variants:
            if variant not in unique_variants and self._check_technical_validity(variant):
                unique_variants.append(variant)
        
        return unique_variants[:5]  # Limit to 5 variants

    def _check_suggestions_availability(
        self, 
        suggestions: List[Dict[str, any]]
    ) -> List[Dict[str, any]]:
        """
        Check the availability of suggested repository names.
        
        Args:
            suggestions: List of suggestion dictionaries
            
        Returns:
            List with availability status updated
        """
        for suggestion in suggestions:
            try:
                name = suggestion["name"]
                exists = self.github_integration.check_repository_exists(name)
                suggestion["available"] = not exists
            except Exception:
                suggestion["available"] = None  # Unable to check
        
        # Sort by availability (available first) and reason
        suggestions.sort(key=lambda x: (
            not x.get("available", False),  # Available first
            x["reason"]  # Then by reason
        ))
        
        return suggestions

    def get_validation_summary(self, validation_results: Dict[str, Dict]) -> Dict[str, any]:
        """
        Get a summary of validation results for reporting.
        
        Args:
            validation_results: Results from validate_multiple_names
            
        Returns:
            Summary dictionary
        """
        total_count = len(validation_results)
        valid_count = sum(1 for r in validation_results.values() if r["is_valid"])
        exists_count = sum(1 for r in validation_results.values() if r["exists"])
        invalid_count = total_count - valid_count
        
        all_suggestions = []
        for result in validation_results.values():
            all_suggestions.extend(result.get("suggestions", []))
        
        return {
            "total_repositories": total_count,
            "valid_available": valid_count,
            "already_exists": exists_count,
            "invalid_format": invalid_count,
            "total_suggestions": len(all_suggestions),
            "available_suggestions": len([s for s in all_suggestions if s.get("available")]),
            "timestamp": int(time.time())
        }

    def save_validation_report(
        self, 
        validation_results: Dict[str, Dict], 
        output_path: str
    ) -> None:
        """
        Save validation results to a JSON file.
        
        Args:
            validation_results: Results from validation
            output_path: Path to save the report
        """
        import json
        from pathlib import Path
        
        report_data = {
            "validation_results": validation_results,
            "summary": self.get_validation_summary(validation_results),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)