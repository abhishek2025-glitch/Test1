# 🤖 GitHub-Native AI Code Generator with Config File Support

**Generate production-ready code from configuration files - no local setup required!**

This enhanced version supports two powerful configuration formats that work directly through GitHub's web interface on any device, including mobile phones.

## 📋 Configuration File Formats

### Format A: Separate Files (Recommended for simple projects)

```
prompts/
├── my-project.txt                # Your project prompt
└── my-project.config.json        # Configuration settings
```

### Format B: Single YAML File (Recommended for complex projects)

```
prompts/
└── my-project.yaml               # Combined config + prompt
```

## 📱 Mobile-Friendly Usage

### Option A - Using YAML (Recommended for most users):

1. **Go to** `prompts/` folder on GitHub.com
2. **Tap** "Add file" → "Create new file"
3. **Name**: `my-project.yaml`
4. **Paste** the YAML template with your settings
5. **Commit** your changes
6. **GitHub Actions runs automatically** ✨
7. **Check PR** for generated code

### Option B - Using Separate Files (for advanced users):

1. **Create** `my-project.txt` with your prompt
2. **Create** `my-project.config.json` with settings
3. **Commit** both files
4. **GitHub Actions runs automatically** ✨
5. **Check PR** for generated code

## 🎯 Configuration Templates

### JSON Configuration Template

**File**: `my-project.config.json`

```json
{
  "repoName": "my-awesome-project",
  "visibility": "public",
  "description": "Multi-agent AI automation system",
  "topics": ["ai", "multi-agent", "automation", "github-actions"],
  "autoValidate": true,
  "author": "your-username",
  "license": "MIT"
}
```

**Corresponding prompt file**: `my-project.txt`

```
Build a sophisticated multi-agent AI system that:
- Coordinates multiple autonomous AI agents
- Triggers and manages GitHub Actions workflows
- Automates deployment and testing pipelines
- Handles general coding tasks and refactoring
- Monitors repository health and code quality
- Integrates with GitHub APIs for full automation

[Continue with your detailed specifications...]
```

### YAML Configuration Template

**File**: `my-project.yaml`

```yaml
# Project Configuration
repoName: my-awesome-project
visibility: public
description: "Multi-agent AI automation system"

# GitHub Topics for discoverability
topics:
  - ai
  - multi-agent
  - automation
  - github-actions
  - workflow-automation
  - code-generation
  - orchestration

# Optional Settings
author: your-username
license: MIT
autoValidate: true

# Project Prompt (supports 3000+ lines)
prompt: |
  Build a sophisticated multi-agent AI system that:
  - Coordinates multiple autonomous AI agents
  - Triggers and manages GitHub Actions workflows
  - Automates deployment and testing pipelines
  - Handles general coding tasks and refactoring
  - Monitors repository health and code quality
  - Integrates with GitHub APIs for full automation
  
  [Continue with your detailed specifications...]
```

## 🔧 Configuration Options

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `repoName` | string | ✅ | GitHub repository name | `"my-project"` |
| `visibility` | string | ❌ | Public or private repository | `"public"` or `"private"` |
| `description` | string | ❌ | Repository description | `"My awesome project"` |
| `topics` | array | ❌ | GitHub topics for discoverability | `["ai", "automation"]` |
| `autoValidate` | boolean | ❌ | Auto-validate configuration | `true` |
| `author` | string | ❌ | Author username | `"your-username"` |
| `license` | string | ❌ | License type | `"MIT"` |
| `prompt` | string | ✅* | Project description prompt | *(in YAML format only)* |

*Required for YAML format, optional for JSON format (use separate .txt file)

## 🚀 Auto-Generated Features

### Repository Name Validation
- ✅ **Checks uniqueness** on your GitHub account
- ✅ **Validates naming conventions** (alphanumeric, hyphens, underscores)
- ✅ **Suggests alternatives** if name is taken:
  - Append timestamp: `my-project-1734067200`
  - Append counter: `my-project-2`, `my-project-3`
  - Suggest variants: `awesome-my-project`

### GitHub Topics System
Automatically applies topics for better discoverability:
- **AI Projects**: `ai`, `machine-learning`, `agents`, `automation`
- **APIs**: `api`, `rest`, `backend`, `fastapi`
- **Frontend**: `react`, `typescript`, `frontend`, `web`
- **DevOps**: `github-actions`, `ci-cd`, `automation`, `devops`
- **CLI Tools**: `cli`, `command-line`, `tool`, `golang`

### Visibility & Access Control
- **`"public"`**: Everyone can see, fork, clone
- **`"private"`**: Only you/collaborators can access

## 📁 File Structure

Your generated repository will include:

```
my-project/
├── src/                    # Source code
├── tests/                  # Test files (70%+ coverage)
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD
├── .gitignore             # Comprehensive ignore rules
├── .env.example           # Environment variable template
├── README.md              # Complete documentation
├── LICENSE                # License (configurable)
└── [config files]         # Framework-specific configs
```

## 🎨 Example Projects

### Multi-Agent AI System

**File**: `prompts/multi-agent-ai.yaml`

```yaml
repoName: multi-agent-orchestrator
visibility: public
description: "Multi-agent AI system for GitHub automation"

topics:
  - ai
  - multi-agent
  - automation
  - github-actions
  - orchestration

prompt: |
  Build a sophisticated multi-agent AI system that coordinates multiple 
  autonomous AI agents for GitHub Actions automation and workflow management.
  
  ## Core Features
  - Agent coordination and task distribution
  - GitHub Actions integration
  - Repository management automation
  - Code quality and testing automation
  - Deployment and operations automation
  
  ## Technical Requirements
  - Microservices architecture
  - Event-driven communication
  - OAuth2 and JWT authentication
  - Horizontal and vertical scaling
  - Comprehensive monitoring
  
  Build this as a production-ready, enterprise-grade system.
```

### FastAPI Task Manager

**Files**: `prompts/task-api.txt` + `prompts/task-api.config.json`

**Config** (`task-api.config.json`):
```json
{
  "repoName": "fastapi-task-manager",
  "visibility": "public",
  "description": "Modern REST API for task management with FastAPI",
  "topics": ["api", "fastapi", "python", "task-manager", "rest"]
}
```

**Prompt** (`task-api.txt`):
```
Build a modern REST API for a task management application using FastAPI.

Core Features:
- User registration and authentication with JWT
- CRUD operations for tasks with categorization
- Priority levels, due dates, and status tracking
- Task assignment and collaboration features
- Search, filtering, and pagination
- Email notifications and file attachments

Technical Requirements:
- Async/await support with proper error handling
- SQLAlchemy ORM with PostgreSQL
- OpenAPI/Swagger documentation
- Redis caching and background tasks
- Rate limiting and security measures
- Comprehensive testing and monitoring

Build this as a production-ready application.
```

## 🔍 Troubleshooting

### Configuration Validation
- ✅ **File format validation**: JSON/YAML syntax checking
- ✅ **Required field checking**: repoName validation
- ✅ **Value validation**: visibility, license types
- ✅ **Topic validation**: GitHub topic format rules

### Repository Name Issues
- **Name taken**: Automatic alternative suggestions
- **Invalid format**: Auto-sanitization with warnings
- **Reserved names**: Clear error messages with fixes

### GitHub API Limitations
- **Rate limiting**: Automatic retry with exponential backoff
- **Token permissions**: Clear error messages for missing scopes
- **Network issues**: Graceful degradation with retry logic

## 📊 Generated Output

Each generation creates:
- ✅ **Pull Request** with generated code
- ✅ **Workflow artifacts** with detailed logs
- ✅ **Repository validation** report
- ✅ **Code quality** metrics and test coverage
- ✅ **Deployment** instructions and documentation

## 🎯 Success Metrics

- ⚡ **Speed**: 10x faster project initialization
- 🏗️ **Quality**: 70%+ test coverage, security scanning
- 📚 **Documentation**: Complete README, API docs, guides
- 🔒 **Security**: No hardcoded secrets, environment-based config
- 🚀 **Deployment**: One-click deployment with proper CI/CD

## 💡 Pro Tips

1. **Use descriptive repo names**: They become part of your brand
2. **Add relevant topics**: Improves discoverability on GitHub
3. **Be specific in prompts**: More detail = better generated code
4. **Use YAML for complex projects**: Supports embedded prompts
5. **Test before committing**: Use `--skip-github` for dry runs

## 🆘 Support

- 📖 **Examples**: Check `prompts/examples/` folder
- 🔧 **Validation**: Use the built-in config validator
- 📱 **Mobile-friendly**: Works perfectly on phone browsers
- 🚀 **Auto-trigger**: GitHub Actions runs automatically on commits

---

**🎉 Ready to generate? Create your first configuration file in the `prompts/` directory!**

*Generated by GitHub Actions AI Code Generator - No local setup required*