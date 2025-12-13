# 🚀 GitHub-Native AI Code Generator - Config File Usage Guide

## Quick Start (Mobile-Friendly)

### Step 1: Create Configuration File

**Option A - YAML (Recommended):**
1. Go to `prompts/` folder on GitHub.com
2. Tap "Add file" → "Create new file"
3. Name: `my-awesome-project.yaml`
4. Copy and paste this template:

```yaml
# Project Configuration
repoName: my-awesome-project
visibility: public
description: "My amazing project description"

# GitHub Topics for discoverability
topics:
  - ai
  - automation
  - python
  - github-actions

# Optional Settings
author: your-username
license: MIT
autoValidate: true

# Your project description (supports 3000+ lines)
prompt: |
  Build a sophisticated AI system that:
  - Implements advanced machine learning algorithms
  - Provides REST API endpoints for data processing
  - Includes comprehensive testing and documentation
  - Supports real-time data analysis and visualization
  - Handles user authentication and authorization
  - Implements proper error handling and logging
  
  Technical Requirements:
  - Use Python with FastAPI for the API
  - Implement PostgreSQL database integration
  - Add Redis caching for performance
  - Include Docker containerization
  - Set up CI/CD with GitHub Actions
  - Generate comprehensive API documentation
  - Implement proper security measures
  
  Build this as a production-ready application.
```

**Option B - JSON (Separate Files):**
1. Create `my-awesome-project.config.json`:

```json
{
  "repoName": "my-awesome-project",
  "visibility": "public", 
  "description": "My amazing project description",
  "topics": ["ai", "automation", "python", "fastapi"],
  "autoValidate": true,
  "author": "your-username",
  "license": "MIT"
}
```

2. Create `my-awesome-project.txt` with your prompt

### Step 2: Commit and Generate

1. **Commit** the configuration file(s)
2. **GitHub Actions** automatically starts
3. **Check** the Pull Request for generated code
4. **Review** the generated repository

## 📋 Configuration Reference

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `repoName` | string | ✅ | GitHub repository name | `"my-awesome-project"` |
| `visibility` | string | ❌ | Repository visibility | `"public"` or `"private"` |
| `description` | string | ❌ | Repository description | `"Amazing AI system"` |
| `topics` | array | ❌ | GitHub topics | `["ai", "automation"]` |
| `autoValidate` | boolean | ❌ | Auto-validate config | `true` |
| `author` | string | ❌ | Author username | `"your-username"` |
| `license` | string | ❌ | License type | `"MIT"` |
| `prompt` | string | ✅* | Project description | *(YAML only)* |

*Required for YAML format, use separate .txt file for JSON format

## 🎯 Smart Features

### Repository Name Validation
- ✅ **Auto-check** if name exists on your GitHub
- ✅ **Suggest alternatives** if taken:
  - `my-project-1734067200` (timestamp)
  - `my-project-2` (counter)
  - `awesome-my-project` (variant)
- ✅ **Format validation** (alphanumeric, hyphens, underscores)
- ✅ **Reserved name detection** (github, git, etc.)

### GitHub Topics Auto-Generation
```yaml
# Automatic topics based on your description
topics: 
  - ai                    # If description mentions AI/ML
  - automation            # If mentions automation
  - github-actions        # If mentions workflows
  - fastapi              # If mentions FastAPI
  - python               # If mentions Python
```

### Visibility Control
- **`"public"`**: Everyone can see and fork
- **`"private"`**: Only collaborators access

## 📱 Mobile Usage Examples

### Multi-Agent AI System
```yaml
repoName: multi-agent-orchestrator
visibility: public
description: "AI agents coordinating GitHub automation"

topics:
  - ai
  - multi-agent
  - automation
  - github-actions

prompt: |
  Build a multi-agent AI system that coordinates multiple
  autonomous agents for repository management, issue tracking,
  and automated code generation. Include workflow automation,
  testing frameworks, and deployment pipelines.
```

### FastAPI Task Manager
```json
{
  "repoName": "fastapi-task-manager",
  "visibility": "public",
  "description": "Modern task management API with FastAPI",
  "topics": ["api", "fastapi", "python", "task-manager"]
}
```

**Separate file**: `fastapi-task-manager.txt`
```
Build a REST API for task management with FastAPI including
user authentication, CRUD operations, search/filtering,
and real-time notifications. Use PostgreSQL database
with SQLAlchemy ORM and implement proper error handling.
```

### React Dashboard
```json
{
  "repoName": "analytics-dashboard",
  "visibility": "public", 
  "description": "Analytics dashboard with React and TypeScript",
  "topics": ["react", "typescript", "dashboard", "analytics"]
}
```

## 🛠️ Advanced Configuration

### Custom Repository Name Suggestions
If your preferred name is taken, the system will:
1. **Check availability** automatically
2. **Suggest alternatives** with reasoning
3. **Use the best available** option
4. **Report suggestions** in PR comments

### Auto-Generated Topics
Based on your prompt, topics are automatically generated:
- **AI/ML**: `ai`, `machine-learning`, `agents`, `automation`
- **APIs**: `api`, `rest`, `fastapi`, `backend`
- **Frontend**: `react`, `typescript`, `ui`, `dashboard`
- **CLI**: `cli`, `command-line`, `tool`, `automation`
- **DevOps**: `github-actions`, `ci-cd`, `deployment`

### Quality Assurance
- ✅ **Configuration validation** before processing
- ✅ **Repository name uniqueness** checking
- ✅ **GitHub API rate limiting** handling
- ✅ **Error recovery** and retry logic
- ✅ **Comprehensive logging** in workflow artifacts

## 📊 Generated Output

Each generation creates:

### 1. Pull Request
- **Branch**: `generated/ai-code-{timestamp}`
- **Title**: `🤖 Generated: {repo-name}`
- **Description**: Complete summary with metrics
- **Artifacts**: Detailed logs and reports

### 2. Repository
- **Full project structure** with source code
- **Comprehensive tests** (70%+ coverage)
- **CI/CD workflows** (GitHub Actions)
- **Documentation** (README, API docs)
- **Deployment configs** (Docker, requirements)

### 3. Workflow Artifacts
- **generation-result.json**: Full generation details
- **repo-suggestions.json**: Name alternatives if needed
- **validation-report.json**: Configuration validation
- **code-quality-report.txt**: Test coverage and metrics

## 🎉 Success Examples

### Before (Manual Setup)
❌ Hours of boilerplate creation
❌ Repetitive configuration
❌ Manual testing setup
❌ CI/CD pipeline creation
❌ Documentation writing

### After (Config-Driven)
✅ **2 minutes** to create configuration
✅ **10x faster** project initialization
✅ **90% less** boilerplate code
✅ **100% automated** testing setup
✅ **Complete CI/CD** with zero config

## 🆘 Troubleshooting

### Common Issues

**YAML files not processing?**
- Ensure PyYAML is available in workflow
- Check YAML syntax (indentation matters)
- Verify `prompt:` field is present

**Repository name conflicts?**
- System automatically suggests alternatives
- Check suggestions in PR description
- Manual override by choosing different name

**No topics generated?**
- Add keywords to description for auto-detection
- Manually specify topics in config
- Check topic format (lowercase, no spaces)

### Validation Errors
- **Missing repoName**: Repository name is required
- **Invalid visibility**: Must be "public" or "private"
- **Long prompt**: Prompts support 3000+ lines
- **Invalid topics**: Check GitHub topic format rules

## 📱 Pro Tips

1. **Be descriptive**: Detailed prompts generate better code
2. **Use keywords**: Help auto-detect topics and tech stack
3. **Mobile-friendly**: Works perfectly on phone browsers
4. **Batch processing**: Multiple configs in one push
5. **Validation first**: Check config before committing

---

**🎯 Ready to generate? Create your first config file and watch the magic happen!**

*Generated by GitHub Actions AI Code Generator - No local setup required*