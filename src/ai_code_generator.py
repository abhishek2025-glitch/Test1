"""AI-powered code generation using OpenRouter API."""
import os
import json
import logging
import time
import asyncio
import httpx
from typing import Dict, List, Optional, Tuple
from jinja2 import Environment, FileSystemLoader, Template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AICodeGenerator:
    """AI-powered code generator using OpenRouter API."""

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize AI code generator.

        Args:
            model: LLM model to use (defaults to deepseek/deepseek-chat)
            api_key: OpenRouter API key (uses env var if not provided)
        """
        self.model = model or os.getenv("LLM_MODEL", "deepseek/deepseek-chat")
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Check for legacy OpenAI key and warn user
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            logger.warning(
                "Found legacy OPENAI_API_KEY. Please use OPENROUTER_API_KEY instead. "
                "OpenAI API is no longer supported."
            )

        self.base_url = "https://api.openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ai-code-generator",
            "X-Title": "AI Code Generator"
        }

        # Available models mapping
        self.supported_models = {
            "deepseek-chat": "deepseek/deepseek-chat",
            "deepseek-coder": "deepseek/deepseek-coder",
            "claude-opus": "anthropic/claude-3-opus",
            "gpt-4": "openai/gpt-4",
            "llama-2": "meta-llama/llama-2-70b-chat"
        }

        # Fallback to templates if AI generation fails
        self.template_generator = None

    def set_template_generator(self, template_generator):
        """Set fallback template generator."""
        self.template_generator = template_generator

    async def generate_code(
        self, 
        description: str, 
        stack_id: str, 
        features: List[str],
        use_ai: bool = True
    ) -> Dict[str, str]:
        """
        Generate code using AI or fallback to templates.

        Args:
            description: Project description
            stack_id: Tech stack identifier
            features: List of features to implement
            use_ai: Whether to use AI generation (fallback to templates if False)

        Returns:
            Dict mapping file paths to content
        """
        try:
            if use_ai:
                logger.info(f"Generating code using AI model: {self.model}")
                return await self._generate_with_ai(description, stack_id, features)
            else:
                logger.info("Using template-based generation")
                return self._generate_with_templates(description, stack_id, features)
        except Exception as e:
            logger.error(f"AI generation failed: {e}. Falling back to templates.")
            if self.template_generator:
                return self._generate_with_templates(description, stack_id, features)
            else:
                raise

    async def _generate_with_ai(
        self, description: str, stack_id: str, features: List[str]
    ) -> Dict[str, str]:
        """Generate code using OpenRouter API."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            prompt = self._build_code_generation_prompt(description, stack_id, features)
            
            response = await self._make_api_request(client, prompt)
            return self._parse_ai_response(response)

    def _generate_with_templates(
        self, description: str, stack_id: str, features: List[str]
    ) -> Dict[str, str]:
        """Generate code using template system."""
        if not self.template_generator:
            raise ValueError("No template generator available for fallback")
        
        # Create minimal project info for template generation
        project_info = {
            "repo_name": description.lower().replace(" ", "-")[:50],
            "repo_description": description,
            "features": features,
            "license": "MIT"
        }
        
        # Get dependencies for the stack
        # This would normally come from tech_stack_selector
        dependencies = self._get_stack_dependencies(stack_id)
        
        # Generate project files using templates
        files = self.template_generator.generate_project(
            stack_id, {}, project_info, dependencies
        )
        
        return files

    def _build_code_generation_prompt(
        self, description: str, stack_id: str, features: List[str]
    ) -> str:
        """Build comprehensive prompt for code generation."""
        model_instructions = {
            "deepseek/deepseek-chat": "You are a helpful coding assistant. Generate clean, production-ready code.",
            "deepseek/deepseek-coder": "You are a senior software engineer specialized in code generation. Generate efficient, well-documented code.",
            "anthropic/claude-3-opus": "You are an expert software architect. Generate robust, scalable code solutions.",
            "openai/gpt-4": "You are an experienced developer. Generate high-quality, maintainable code.",
            "meta-llama/llama-2-70b-chat": "You are a skilled programmer. Generate clean, functional code."
        }

        base_instruction = model_instructions.get(
            self.model, "You are a helpful coding assistant. Generate clean, production-ready code."
        )

        prompt = f"""{base_instruction}

Generate a complete {stack_id} project based on the following requirements:

Project Description: {description}
Features to implement: {', '.join(features)}
Tech Stack: {stack_id}

Please provide a JSON response with the following structure:
{{
    "files": {{
        "filename1": "file content here",
        "filename2": "file content here"
    }},
    "description": "Brief description of what was generated",
    "features_implemented": ["feature1", "feature2"]
}}

Generate all necessary files including:
- Main application files
- Configuration files
- Test files
- README.md
- .gitignore
- Requirements/package files
- Environment example file
- CI/CD configuration

Ensure code follows best practices, includes proper error handling, and is production-ready."""

        return prompt

    async def _make_api_request(self, client: httpx.AsyncClient, prompt: str) -> str:
        """Make request to OpenRouter API with retry logic."""
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 4000,
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "stream": False
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                elif response.status_code == 429:
                    # Rate limit hit, wait and retry
                    logger.warning(f"Rate limit hit, retrying in {retry_delay}s")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"API request failed: {response.status_code} - {response.text}")
                    if attempt == max_retries - 1:
                        raise Exception(f"API request failed: {response.status_code}")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2

            except Exception as e:
                logger.error(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(retry_delay)
                retry_delay *= 2

    def _parse_ai_response(self, response: str) -> Dict[str, str]:
        """Parse AI response and extract code files."""
        try:
            # Try to extract JSON from the response
            # Look for JSON content between triple backticks or at the end
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = response[json_start:json_end]
                parsed_response = json.loads(json_content)
                
                if "files" in parsed_response:
                    return parsed_response["files"]
            
            # Fallback: look for code blocks and create basic structure
            logger.warning("Could not parse JSON from AI response, using fallback parsing")
            return self._fallback_parse_response(response)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return self._fallback_parse_response(response)

    def _fallback_parse_response(self, response: str) -> Dict[str, str]:
        """Fallback parsing for non-JSON AI responses."""
        files = {}
        
        # Try to extract code blocks
        import re
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', response, re.DOTALL)
        
        if code_blocks:
            # If we have code blocks, create basic files
            files["main.py"] = code_blocks[0] if code_blocks else "# Generated code"
            files["README.md"] = f"# Generated Project\n\n{response[:500]}..."
        else:
            # Create a single file with the response
            files["generated_code.txt"] = response
            
        return files

    def _get_stack_dependencies(self, stack_id: str) -> Dict:
        """Get dependencies for a tech stack."""
        # This would normally come from tech_stack_selector
        # For now, return basic dependencies
        basic_dependencies = {
            "python-fastapi": {
                "dependencies": {"fastapi": "0.104.1", "uvicorn": "0.24.0"},
                "dev_dependencies": {"pytest": "7.4.3", "black": "23.12.1"}
            },
            "nodejs-express": {
                "dependencies": {"express": "^4.18.2"},
                "dev_dependencies": {"jest": "^29.7.0"}
            },
            "react-typescript": {
                "dependencies": {"react": "^18.2.0"},
                "dev_dependencies": {"typescript": "^5.3.3"}
            }
        }
        return basic_dependencies.get(stack_id, {"dependencies": {}, "dev_dependencies": {}})

    def get_supported_models(self) -> Dict[str, str]:
        """Get list of supported models."""
        return self.supported_models.copy()

    def validate_api_key(self) -> bool:
        """Validate that the API key works."""
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False