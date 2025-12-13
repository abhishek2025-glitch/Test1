# AI Code Generator GitHub Auto-Push System

🚀 **Generate production-ready code from natural language descriptions and automatically push to GitHub!**

An intelligent AI-powered code generation system that uses OpenRouter API with DeepSeek and other LLMs to transform project descriptions into fully functional, tested, and documented code repositories. The system supports both AI-powered generation and template-based fallback, automatically creates GitHub repositories, generates clean architecture code, runs quality checks, and pushes everything with proper CI/CD configuration.

## ✨ Features

- 🧠 **Natural Language Input**: Describe your project in plain English
- 🎯 **Smart Tech Stack Selection**: Automatically selects the best stack for your needs
- 🏗️ **Clean Architecture**: Generates well-structured, maintainable code
- 🧪 **Built-in Testing**: Includes unit tests with 70%+ coverage target
- 📚 **Complete Documentation**: Generates README, API docs, and contribution guidelines
- 🔒 **Security First**: No hardcoded secrets, environment variable configuration
- 🔄 **CI/CD Ready**: Auto-generated GitHub Actions workflows
- 🐙 **GitHub Integration**: Creates repo, pushes code, adds topics, creates releases
- ✅ **Quality Assurance**: Validates syntax, runs security checks, ensures best practices

## 📋 Requirements

- Python 3.9+
- OpenRouter API Key (optional, enables AI-powered generation)
- GitHub Personal Access Token (with `repo` scope)
- Git installed locally

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-generator.git
cd ai-code-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your API keys:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Get OpenRouter API Key (optional, for AI generation):**
1. Go to https://openrouter.ai/keys
2. Create an account and generate an API key
3. Copy the key to your `.env` file as `OPENROUTER_API_KEY`
4. Choose your preferred model (defaults to `deepseek/deepseek-chat`)

**Get GitHub Personal Access Token (required):**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy the token to your `.env` file

### 3. Generate Your First Project

```bash
# Basic usage (template-based)
python -m src.main -d "Build a REST API for todo management"

# With OpenRouter AI generation (requires OPENROUTER_API_KEY)
python -m src.main -d "Build a REST API for todo management" --llm-model deepseek/deepseek-chat

# With specific LLM model
python -m src.main -d "Build a web API" --llm-model anthropic/claude-3-opus

# With specific tech stack
python -m src.main -d "Build a REST API" -t "python-fastapi"

# With features
python -m src.main -d "Build a web API" -f "user authentication" -f "data validation"

# Custom repository name
python -m src.main -d "Build a CLI tool" -n "my-awesome-cli"

# Private repository
python -m src.main -d "Build an API" --private

# Template-only mode (no AI)
python -m src.main -d "Build a CLI tool" --no-ai
```

## 🎯 Supported Tech Stacks

| Stack | Use Case | Generated Files |
|-------|----------|----------------|
| **Node.js + Express** | REST APIs, Web Services | Express server, routes, middleware, tests |
| **Python + FastAPI** | Modern APIs, Async services | FastAPI app, routes, config, async tests |
| **React + TypeScript** | Frontend applications | React components, TypeScript config, Vite |
| **Python CLI** | Command-line tools | Click-based CLI, rich output, commands |
| **Go CLI** | High-performance CLIs | Cobra-based CLI, Go modules |
| **Python ML/Data** | Data science, ML projects | Model scripts, notebooks, data pipelines |

## 📖 Usage Examples

### Example 1: Simple REST API

```bash
python -m src.main \
  -d "Create a REST API for managing books with CRUD operations" \
  -t "python-fastapi" \
  -n "book-api"
```

**Generates:**
- FastAPI application with health check
- CRUD endpoint structure
- Pydantic models
- Unit tests with pytest
- Docker configuration
- CI/CD pipeline
- Complete README

### Example 2: React Frontend

```bash
python -m src.main \
  -d "Build a modern dashboard for analytics visualization" \
  -t "react-typescript" \
  -f "charts" -f "data tables"
```

**Generates:**
- React + TypeScript setup
- Component structure
- TypeScript configurations
- Build system (Vite)
- Test setup
- CI/CD workflow

### Example 3: CLI Tool

```bash
python -m src.main \
  -d "Create a command-line tool for file processing" \
  -t "python-cli" \
  -n "file-processor"
```

**Generates:**
- Click-based CLI interface
- Command structure
- Rich console output
- Setup.py for installation
- Tests and documentation

## 🤖 AI-Powered Code Generation

The system now supports AI-powered code generation using OpenRouter API with multiple LLM models:

### Available LLM Models

| Model | Use Case | Cost | Quality |
|-------|----------|------|---------|
| **deepseek/deepseek-chat** (default) | General code generation | Low | Good |
| **deepseek/deepseek-coder** | Specialized code generation | Low | Very Good |
| **anthropic/claude-3-opus** | Premium quality generation | High | Excellent |
| **openai/gpt-4** | Premium general purpose | High | Excellent |
| **meta-llama/llama-2-70b-chat** | Open source alternative | Low | Good |

### AI Generation Features

- **Natural Language Processing**: Converts project descriptions into structured code
- **Context Awareness**: Understands tech stack requirements and features
- **Code Quality**: Generates production-ready, well-documented code
- **Fallback System**: Automatically falls back to templates if AI fails
- **Rate Limiting**: Handles API limits with retry logic
- **Cost Effective**: Uses cost-effective DeepSeek models by default

### Environment Variables

```bash
# Required for AI generation
OPENROUTER_API_KEY=sk-or-...

# Optional model selection (defaults to deepseek/deepseek-chat)
LLM_MODEL=deepseek/deepseek-coder

# Legacy OpenAI key (will show warning to migrate)
OPENAI_API_KEY=sk-...  # ⚠️ Deprecated
```

### Cost Comparison

| Model | Cost per 1K tokens | Monthly cost estimate* |
|-------|-------------------|----------------------|
| deepseek/deepseek-chat | ~$0.0014 | $5-15 |
| deepseek/deepseek-coder | ~$0.0014 | $5-15 |
| anthropic/claude-3-opus | ~$0.015 | $50-150 |
| openai/gpt-4 | ~$0.03 | $100-300 |

*Based on typical usage patterns for code generation

## 🔧 Command-Line Options

```
Options:
  -d, --description TEXT       Project description (required)
  -t, --tech-stack TEXT        Preferred tech stack
  -f, --features TEXT          Features to implement (multiple)
  -n, --repo-name TEXT         Repository name (auto-generated if not provided)
  --repo-description TEXT      Repository description
  --private                    Make repository private
  --license TEXT               License type (default: MIT)
  --skip-github                Skip GitHub operations (for testing)
  --llm-model TEXT             LLM model to use (default: deepseek/deepseek-chat)
  --no-ai                      Use template-based generation only (no AI)
  --help                       Show this message and exit
```

## 🏗️ Architecture

```
ai-code-generator/
├── src/
│   ├── main.py                    # Entry point and orchestrator
│   ├── input_processor.py         # Input validation and parsing
│   ├── tech_stack_selector.py     # Intelligent stack selection
│   ├── architecture_planner.py    # Project structure planning
│   ├── code_generator.py          # Template-based code generation engine
│   ├── ai_code_generator.py       # AI-powered code generation using OpenRouter
│   ├── quality_assurance.py       # Quality checks and validation
│   ├── github_integration.py      # GitHub API operations
│   ├── git_operations.py          # Local git operations
│   └── response_formatter.py      # Output formatting
├── tests/                         # Comprehensive test suite
│   ├── test_ai_code_generator.py  # AI generator tests (new)
│   └── ...                        # Other test files
├── templates/                     # Code templates (fallback system)
├── generated_projects/            # Output directory (gitignored)
└── requirements.txt               # Python dependencies (includes httpx)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_input_processor.py

# Run with verbose output
pytest -v
```

**Test Coverage:** 70%+ maintained across all modules

## 🔒 Security

- ✅ No hardcoded secrets or credentials
- ✅ Environment variables for all sensitive data
- ✅ Security pattern detection in generated code
- ✅ Automatic .gitignore generation
- ✅ .env.example templates provided
- ✅ GitHub token validation

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests before committing
pytest

# Format code
black src/ tests/

# Lint code
pylint src/
```

## 📝 Generated Project Structure

When you generate a project, you get:

```
your-project/
├── src/                    # Source code
├── tests/                  # Test files (70%+ coverage)
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD
├── .gitignore             # Comprehensive ignore rules
├── .env.example           # Environment variable template
├── README.md              # Complete documentation
├── LICENSE                # MIT license (default)
├── package.json           # Dependencies (Node.js)
├── requirements.txt       # Dependencies (Python)
└── [config files]         # ESLint, TypeScript, pytest, etc.
```

## 🎯 Tech Stack Intelligence

The system automatically selects the best tech stack based on keywords:

- **"web", "api", "rest"** → Node.js/Express or Python/FastAPI
- **"frontend", "ui", "react"** → React + TypeScript
- **"mobile", "app"** → React Native (future)
- **"cli", "command-line"** → Python CLI or Go CLI
- **"data", "ml", "analytics"** → Python ML stack

## 🐛 Troubleshooting

### GitHub Token Issues

```bash
# Verify token has correct scopes
# Required: repo, workflow

# Check token in .env file
cat .env | grep GITHUB_TOKEN
```

### Repository Already Exists

```bash
# Use a different name
python -m src.main -d "Your description" -n "different-name"

# Or delete the existing repo on GitHub first
```

### Git Push Failures

```bash
# Ensure git is installed
git --version

# Check GitHub credentials
git credential-helper
```

## 🗺️ Roadmap

- [ ] Add more tech stack templates (Django, Flask, Vue, Angular)
- [ ] Support for microservices architecture
- [ ] Database schema generation and migrations
- [ ] Docker and Kubernetes configuration
- [ ] Terraform infrastructure as code
- [ ] Custom template support
- [ ] AI-powered code optimization
- [ ] Integration with other git platforms (GitLab, Bitbucket)
- [ ] Web UI interface
- [ ] VS Code extension

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Built with:
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API wrapper
- [GitPython](https://github.com/gitpython-developers/GitPython) - Git operations
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [pytest](https://pytest.org/) - Testing framework

## 📧 Support

- 🐛 [Report bugs](https://github.com/yourusername/ai-code-generator/issues)
- 💡 [Request features](https://github.com/yourusername/ai-code-generator/issues)
- 📖 [Documentation](https://github.com/yourusername/ai-code-generator/wiki)

---

**Made with ❤️ by the AI Code Generator Team**

⭐ Star us on GitHub if you find this useful!
