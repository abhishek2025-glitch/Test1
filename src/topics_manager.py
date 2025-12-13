"""GitHub topics management module."""
import re
import time
from typing import Dict, List, Set, Optional, Tuple
from collections import Counter

# Conditional import for tech stack selector (optional)
try:
    from src.tech_stack_selector import TechStackSelector
    TECH_STACK_SELECTOR_AVAILABLE = True
except ImportError:
    TechStackSelector = None
    TECH_STACK_SELECTOR_AVAILABLE = False


class TopicsManager:
    """Manages GitHub repository topics for better discoverability."""

    def __init__(self):
        self.tech_stack_selector = TechStackSelector() if TECH_STACK_SELECTOR_AVAILABLE else None
        self.max_topics = 5  # GitHub's limit
        self.min_topics = 1
        
        # Topic suggestions for different project types
        self.topic_suggestions = {
            # AI/ML Projects
            "ai_projects": [
                "ai", "machine-learning", "llm", "nlp", "deep-learning", 
                "agents", "multi-agent", "artificial-intelligence", "neural-networks",
                "tensorflow", "pytorch", "scikit-learn", "data-science", "automation"
            ],
            
            # Automation & Workflows
            "automation": [
                "automation", "workflow-automation", "github-actions", 
                "orchestration", "devops", "cicd", "ci-cd", "workflow",
                "pipelines", "continuous-integration", "continuous-deployment"
            ],
            
            # Code Generation
            "code_generation": [
                "code-generation", "codegen", "code-generator", "scaffolding",
                "template-engine", "ai-generated", "automated-code", "boilerplate"
            ],
            
            # Backend APIs
            "backend": [
                "backend", "api", "rest-api", "rest", "api-development", 
                "server", "microservices", "backend-api", "web-api", "json-api"
            ],
            
            # Frontend
            "frontend": [
                "frontend", "react", "typescript", "javascript", "web", 
                "ui", "dashboard", "SPA", "single-page-application", "responsive"
            ],
            
            # CLI Tools
            "cli_tools": [
                "cli", "command-line", "terminal", "tool", "command-line-tool",
                "golang", "python", "script", "utility", "command"
            ],
            
            # Data Science
            "data_science": [
                "data-science", "analytics", "pandas", "data-analysis", 
                "data-visualization", "statistics", "big-data", "analysis"
            ],
            
            # DevOps
            "devops": [
                "devops", "docker", "kubernetes", "infrastructure", 
                "deployment", "monitoring", "logging", "containerization"
            ],
            
            # General Development
            "development": [
                "open-source", "programming", "software-development", 
                "coding", "project", "library", "framework", "tooling"
            ]
        }

    def generate_topics(
        self, 
        description: str, 
        tech_stack: Optional[str] = None,
        custom_topics: Optional[List[str]] = None,
        auto_detect: bool = True
    ) -> List[str]:
        """
        Generate relevant GitHub topics for a repository.
        
        Args:
            description: Project description
            tech_stack: Selected tech stack
            custom_topics: User-provided custom topics
            auto_detect: Whether to auto-detect topics from description
            
        Returns:
            List of 1-5 GitHub topics
        """
        all_topics = set()
        
        # Add custom topics first (user preference)
        if custom_topics:
            all_topics.update(self._sanitize_topics(custom_topics))
        
        # Auto-detect topics if enabled
        if auto_detect:
            detected_topics = self._detect_topics_from_description(description)
            all_topics.update(detected_topics)
            
            # Add tech stack specific topics
            if tech_stack:
                stack_topics = self._get_tech_stack_topics(tech_stack)
                all_topics.update(stack_topics)
        
        # Ensure we have at least one topic
        if not all_topics:
            all_topics.add("open-source")
        
        # Prioritize and limit topics
        prioritized_topics = self._prioritize_topics(list(all_topics))
        final_topics = prioritized_topics[:self.max_topics]
        
        return final_topics

    def suggest_topics(
        self, 
        description: str, 
        tech_stack: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Suggest topics with explanations for user selection.
        
        Args:
            description: Project description
            tech_stack: Selected tech stack
            category: Preferred topic category
            
        Returns:
            List of topic suggestions with metadata
        """
        suggestions = []
        
        # Auto-detect topics
        detected = self._detect_topics_from_description(description)
        
        for topic in detected:
            suggestions.append({
                "topic": topic,
                "source": "auto-detected",
                "confidence": "high" if self._is_core_topic(topic) else "medium",
                "category": self._get_topic_category(topic),
                "description": self._get_topic_description(topic)
            })
        
        # Add tech stack topics
        if tech_stack:
            stack_topics = self._get_tech_stack_topics(tech_stack)
            for topic in stack_topics:
                if topic not in [s["topic"] for s in suggestions]:
                    suggestions.append({
                        "topic": topic,
                        "source": "tech-stack",
                        "confidence": "high",
                        "category": "technology",
                        "description": f"Related to {tech_stack} technology"
                    })
        
        # Add category-specific suggestions
        if category and category in self.topic_suggestions:
            category_topics = self.topic_suggestions[category]
            for topic in category_topics:
                if topic not in [s["topic"] for s in suggestions]:
                    suggestions.append({
                        "topic": topic,
                        "source": "category",
                        "confidence": "medium",
                        "category": category,
                        "description": f"Popular topic for {category} projects"
                    })
        
        # Add general suggestions
        general_topics = ["open-source", "automation", "ai-generated", "programming"]
        for topic in general_topics:
            if topic not in [s["topic"] for s in suggestions]:
                suggestions.append({
                    "topic": topic,
                    "source": "general",
                    "confidence": "low",
                    "category": "general",
                    "description": "General topic for better discoverability"
                })
        
        return suggestions[:10]  # Return top 10 suggestions

    def validate_topics(self, topics: List[str]) -> Dict[str, any]:
        """
        Validate a list of GitHub topics.
        
        Args:
            topics: List of topics to validate
            
        Returns:
            Validation results with cleaned topics and errors
        """
        validation_result = {
            "original_topics": topics,
            "cleaned_topics": [],
            "invalid_topics": [],
            "duplicates_removed": 0,
            "truncated": False,
            "warnings": [],
            "errors": []
        }
        
        if not topics:
            validation_result["errors"].append("No topics provided")
            return validation_result
        
        # Clean and validate each topic
        seen_topics = set()
        for topic in topics:
            cleaned_topic = self._sanitize_single_topic(topic)
            
            if not cleaned_topic:
                validation_result["invalid_topics"].append(topic)
                continue
            
            # Check for duplicates
            if cleaned_topic in seen_topics:
                validation_result["duplicates_removed"] += 1
                continue
            
            # Validate topic format
            if not self._is_valid_topic_format(cleaned_topic):
                validation_result["invalid_topics"].append(topic)
                continue
            
            seen_topics.add(cleaned_topic)
            validation_result["cleaned_topics"].append(cleaned_topic)
        
        # Check limits
        if len(validation_result["cleaned_topics"]) > self.max_topics:
            validation_result["truncated"] = True
            validation_result["cleaned_topics"] = validation_result["cleaned_topics"][:self.max_topics]
            validation_result["warnings"].append(
                f"Top {self.max_topics} topics kept (GitHub limit)"
            )
        
        if len(validation_result["cleaned_topics"]) < self.min_topics:
            validation_result["errors"].append(
                f"Need at least {self.min_topics} valid topic(s)"
            )
        
        # Add warnings
        if validation_result["invalid_topics"]:
            validation_result["warnings"].append(
                f"Removed {len(validation_result['invalid_topics'])} invalid topic(s)"
            )
        
        return validation_result

    def _detect_topics_from_description(self, description: str) -> Set[str]:
        """Detect relevant topics from project description."""
        description_lower = description.lower()
        detected_topics = set()
        
        # Define keyword mappings
        keyword_mappings = {
            # AI/ML
            "ai": ["ai", "artificial intelligence", "machine learning", "ml", "neural"],
            "agents": ["agent", "agents", "multi-agent", "autonomous"],
            "llm": ["llm", "language model", "gpt", "bert", "transformer"],
            
            # Automation
            "automation": ["automation", "automated", "workflow", "pipeline"],
            "github-actions": ["github", "actions", "ci", "cd", "cicd"],
            "devops": ["devops", "deployment", "infrastructure", "docker"],
            
            # Development
            "api": ["api", "rest", "restful", "endpoint", "microservice"],
            "web": ["web", "website", "webapp", "http", "server"],
            "frontend": ["frontend", "ui", "interface", "react", "vue", "angular"],
            "cli": ["cli", "command", "terminal", "command-line"],
            "data-science": ["data", "analytics", "analysis", "statistics"],
            
            # Technologies
            "python": ["python", "django", "flask", "fastapi"],
            "nodejs": ["node", "nodejs", "express", "javascript"],
            "typescript": ["typescript", "ts"],
            "golang": ["golang", "go", "go-lang"],
            "react": ["react", "jsx", "tsx"],
        }
        
        for topic, keywords in keyword_mappings.items():
            if any(keyword in description_lower for keyword in keywords):
                detected_topics.add(topic)
        
        return detected_topics

    def _get_tech_stack_topics(self, tech_stack: str) -> Set[str]:
        """Get topics related to a specific tech stack."""
        stack_topics = set()
        stack_lower = tech_stack.lower()
        
        # Python stacks
        if "python" in stack_lower:
            stack_topics.update(["python", "api", "data-science"])
            if "fastapi" in stack_lower:
                stack_topics.add("fastapi")
            if "flask" in stack_lower:
                stack_topics.add("flask")
        
        # Node.js stacks
        elif "node" in stack_lower or "express" in stack_lower:
            stack_topics.update(["nodejs", "javascript", "api"])
            if "express" in stack_lower:
                stack_topics.add("express")
        
        # React stacks
        elif "react" in stack_lower:
            stack_topics.update(["react", "typescript", "frontend", "web"])
        
        # Go stacks
        elif "go" in stack_lower:
            stack_topics.update(["golang", "cli"])
        
        return stack_topics

    def _sanitize_topics(self, topics: List[str]) -> Set[str]:
        """Sanitize a list of topics."""
        return {
            self._sanitize_single_topic(topic) 
            for topic in topics 
            if self._sanitize_single_topic(topic)
        }

    def _sanitize_single_topic(self, topic: str) -> Optional[str]:
        """Sanitize a single topic."""
        if not topic:
            return None
        
        # Convert to lowercase and strip
        topic = topic.lower().strip()
        
        # Remove invalid characters
        topic = re.sub(r"[^a-z0-9-]", "-", topic)
        
        # Replace multiple hyphens with single
        topic = re.sub(r"-+", "-", topic)
        
        # Remove leading/trailing hyphens
        topic = topic.strip("-")
        
        # Check length (GitHub topics should be 1-35 characters)
        if len(topic) < 1 or len(topic) > 35:
            return None
        
        return topic

    def _is_valid_topic_format(self, topic: str) -> bool:
        """Check if topic meets GitHub requirements."""
        # GitHub topic format rules
        if len(topic) < 1 or len(topic) > 35:
            return False
        
        # Only lowercase letters, numbers, and hyphens
        if not re.match(r"^[a-z0-9-]+$", topic):
            return False
        
        # Can't start or end with hyphen
        if topic.startswith("-") or topic.endswith("-"):
            return False
        
        # Can't contain double hyphens
        if "--" in topic:
            return False
        
        return True

    def _is_core_topic(self, topic: str) -> bool:
        """Check if topic is a core/important topic."""
        core_topics = {
            "ai", "automation", "api", "python", "nodejs", "react", 
            "golang", "cli", "data-science", "machine-learning"
        }
        return topic in core_topics

    def _get_topic_category(self, topic: str) -> str:
        """Get the category of a topic."""
        for category, topics in self.topic_suggestions.items():
            if topic in topics:
                return category
        return "general"

    def _get_topic_description(self, topic: str) -> str:
        """Get a description for a topic."""
        descriptions = {
            "ai": "Artificial Intelligence and Machine Learning",
            "automation": "Automation and Workflow Orchestration",
            "api": "Application Programming Interface",
            "python": "Python Programming Language",
            "nodejs": "Node.js JavaScript Runtime",
            "react": "React JavaScript Library",
            "golang": "Go Programming Language",
            "cli": "Command Line Interface Tool",
            "data-science": "Data Science and Analytics",
            "github-actions": "GitHub Actions and CI/CD"
        }
        return descriptions.get(topic, f"Related to {topic}")

    def _prioritize_topics(self, topics: List[str]) -> List[str]:
        """Prioritize topics for better repository discoverability."""
        # Priority order (most important first)
        priority_order = [
            "ai", "automation", "python", "nodejs", "react", "golang", 
            "api", "cli", "data-science", "machine-learning", "open-source"
        ]
        
        # Sort by priority, then alphabetically
        topics_set = set(topics)
        prioritized = []
        
        for priority_topic in priority_order:
            if priority_topic in topics_set:
                prioritized.append(priority_topic)
                topics_set.remove(priority_topic)
        
        # Add remaining topics alphabetically
        remaining = sorted(list(topics_set))
        prioritized.extend(remaining)
        
        return prioritized

    def save_topics_report(
        self, 
        topics: List[str], 
        output_path: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """Save topics information to a file."""
        import json
        from pathlib import Path
        
        report_data = {
            "topics": topics,
            "count": len(topics),
            "validation": self.validate_topics(topics),
            "suggestions": self.suggest_topics("", category="all")[:5],
            "metadata": metadata or {},
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        }
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)