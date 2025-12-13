"""Tests for AI Code Generator module."""
import os
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.ai_code_generator import AICodeGenerator


class TestAICodeGenerator:
    """Test cases for AICodeGenerator class."""

    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenRouter API key is required"):
                AICodeGenerator()

    def test_init_with_api_key(self):
        """Test successful initialization with API key."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            assert generator.api_key == "test-key"
            assert generator.model == "deepseek/deepseek-chat"

    def test_init_with_custom_model(self):
        """Test initialization with custom model."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator(model="deepseek/deepseek-coder")
            assert generator.model == "deepseek/deepseek-coder"

    def test_init_with_env_model(self):
        """Test initialization with model from environment."""
        with patch.dict(os.environ, {
            "OPENROUTER_API_KEY": "test-key",
            "LLM_MODEL": "anthropic/claude-3-opus"
        }):
            generator = AICodeGenerator()
            assert generator.model == "anthropic/claude-3-opus"

    def test_init_with_legacy_openai_key(self):
        """Test warning when legacy OpenAI key is present."""
        with patch.dict(os.environ, {
            "OPENROUTER_API_KEY": "test-key",
            "OPENAI_API_KEY": "old-key"
        }):
            with patch('src.ai_code_generator.logger.warning') as mock_warning:
                generator = AICodeGenerator()
                mock_warning.assert_called_once()
                assert "legacy OPENAI_API_KEY" in mock_warning.call_args[0][0]

    def test_supported_models(self):
        """Test supported models mapping."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            models = generator.get_supported_models()
            assert "deepseek-chat" in models
            assert "deepseek-coder" in models
            assert models["deepseek-chat"] == "deepseek/deepseek-chat"

    @pytest.mark.asyncio
    async def test_generate_code_with_templates_fallback(self):
        """Test fallback to template generation when AI fails."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            # Mock template generator
            template_gen = Mock()
            template_gen.generate_project.return_value = {
                "main.py": "print('hello')",
                "README.md": "# Test Project"
            }
            generator.set_template_generator(template_gen)
            
            # Test template fallback
            result = await generator.generate_code(
                "test description", 
                "python-cli", 
                ["feature1"], 
                use_ai=False
            )
            
            assert "main.py" in result
            assert "README.md" in result
            template_gen.generate_project.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_code_with_ai_success(self):
        """Test successful AI code generation."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            # Mock template generator
            template_gen = Mock()
            generator.set_template_generator(template_gen)
            
            # Mock successful AI response
            mock_response = '''{
                "files": {
                    "main.py": "print('hello from AI')",
                    "test.py": "assert True"
                },
                "description": "AI generated project",
                "features_implemented": ["feature1"]
            }'''
            
            with patch.object(generator, '_generate_with_ai', return_value={
                "main.py": "print('hello from AI')",
                "test.py": "assert True"
            }):
                result = await generator.generate_code(
                    "test description", 
                    "python-cli", 
                    ["feature1"], 
                    use_ai=True
                )
                
                assert "main.py" in result
                assert "test.py" in result
                assert result["main.py"] == "print('hello from AI')"

    @pytest.mark.asyncio
    async def test_generate_code_ai_fallback_to_templates(self):
        """Test fallback to templates when AI generation fails."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            # Mock template generator
            template_gen = Mock()
            template_gen.generate_project.return_value = {
                "main.py": "print('from template')"
            }
            generator.set_template_generator(template_gen)
            
            # Mock AI failure
            with patch.object(generator, '_generate_with_ai', side_effect=Exception("API failed")):
                result = await generator.generate_code(
                    "test description", 
                    "python-cli", 
                    ["feature1"], 
                    use_ai=True
                )
                
                # Should fallback to templates
                assert "main.py" in result
                assert result["main.py"] == "print('from template')"

    def test_build_code_generation_prompt(self):
        """Test prompt building for code generation."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            prompt = generator._build_code_generation_prompt(
                "Build a todo API",
                "python-fastapi", 
                ["CRUD", "authentication"]
            )
            
            assert "Build a todo API" in prompt
            assert "python-fastapi" in prompt
            assert "CRUD" in prompt
            assert "authentication" in prompt
            assert "JSON response" in prompt

    def test_parse_ai_response_valid_json(self):
        """Test parsing valid JSON response from AI."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            response = '''Some text before
{
    "files": {
        "main.py": "print('hello')",
        "test.py": "assert True"
    },
    "description": "Test project"
}
Some text after'''
            
            result = generator._parse_ai_response(response)
            
            assert "main.py" in result
            assert "test.py" in result
            assert result["main.py"] == "print('hello')"

    def test_parse_ai_response_fallback_parsing(self):
        """Test fallback parsing when JSON is invalid."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            response = "This is just plain text without JSON"
            
            with patch.object(generator, '_fallback_parse_response') as mock_fallback:
                mock_fallback.return_value = {"generated_code.txt": response}
                
                result = generator._parse_ai_response(response)
                
                mock_fallback.assert_called_once_with(response)

    def test_fallback_parse_response_with_code_blocks(self):
        """Test fallback parsing with code blocks."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            response = '''Here is some code:

```python
def hello():
    print("Hello World")
```

And some more:

```javascript
console.log("Hello");
```
'''
            
            result = generator._fallback_parse_response(response)
            
            assert "main.py" in result
            assert "Hello World" in result["main.py"]

    def test_fallback_parse_response_plain_text(self):
        """Test fallback parsing with plain text."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            response = "This is just plain text without any code blocks"
            
            result = generator._fallback_parse_response(response)
            
            assert "generated_code.txt" in result
            assert "plain text" in result["generated_code.txt"]

    def test_get_stack_dependencies(self):
        """Test getting dependencies for different stacks."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            # Test Python FastAPI
            deps = generator._get_stack_dependencies("python-fastapi")
            assert "dependencies" in deps
            assert "fastapi" in deps["dependencies"]
            
            # Test Node.js Express
            deps = generator._get_stack_dependencies("nodejs-express")
            assert "express" in deps["dependencies"]
            
            # Test unknown stack
            deps = generator._get_stack_dependencies("unknown-stack")
            assert "dependencies" in deps
            assert len(deps["dependencies"]) == 0

    def test_validate_api_key_success(self):
        """Test successful API key validation."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            with patch('httpx.Client') as mock_client:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_client.return_value.__enter__.return_value.get.return_value = mock_response
                
                result = generator.validate_api_key()
                assert result is True

    def test_validate_api_key_failure(self):
        """Test failed API key validation."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            with patch('httpx.Client') as mock_client:
                mock_response = Mock()
                mock_response.status_code = 401
                mock_client.return_value.__enter__.return_value.get.return_value = mock_response
                
                result = generator.validate_api_key()
                assert result is False

    def test_generate_with_templates(self):
        """Test template-based generation."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            
            # Mock template generator
            template_gen = Mock()
            template_gen.generate_project.return_value = {
                "main.py": "print('template result')"
            }
            generator.set_template_generator(template_gen)
            
            result = generator._generate_with_templates(
                "test description",
                "python-cli", 
                ["feature1"]
            )
            
            assert "main.py" in result
            assert result["main.py"] == "print('template result')"
            template_gen.generate_project.assert_called_once()

    def test_generate_with_templates_no_fallback(self):
        """Test template generation without fallback generator."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            generator = AICodeGenerator()
            # Don't set template generator
            
            with pytest.raises(ValueError, match="No template generator available"):
                generator._generate_with_templates(
                    "test description",
                    "python-cli", 
                    ["feature1"]
                )