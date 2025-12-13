"""Code generation engine."""
import os
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, Template


class CodeGenerator:
    """Generates production-ready code from templates."""

    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        if os.path.exists(templates_dir):
            self.env = Environment(loader=FileSystemLoader(templates_dir))
        else:
            self.env = None

    def generate_project(
        self,
        stack_id: str,
        architecture: Dict,
        project_info: Dict,
        dependencies: Dict,
    ) -> Dict[str, str]:
        """
        Generate all project files.

        Args:
            stack_id: Tech stack identifier
            architecture: Architecture plan
            project_info: Project information
            dependencies: Tech stack dependencies

        Returns:
            Dict mapping file paths to content
        """
        files = {}

        if stack_id == "nodejs-express":
            files.update(self._generate_nodejs_express(project_info, dependencies))
        elif stack_id == "python-fastapi":
            files.update(self._generate_python_fastapi(project_info, dependencies))
        elif stack_id == "react-typescript":
            files.update(self._generate_react_typescript(project_info, dependencies))
        elif stack_id == "python-cli":
            files.update(self._generate_python_cli(project_info, dependencies))
        elif stack_id == "go-cli":
            files.update(self._generate_go_cli(project_info, dependencies))
        elif stack_id == "python-ml":
            files.update(self._generate_python_ml(project_info, dependencies))

        files[".gitignore"] = self._generate_gitignore(stack_id)
        files[".env.example"] = self._generate_env_example(stack_id)
        files["LICENSE"] = self._generate_license(project_info)
        files["README.md"] = self._generate_readme(
            stack_id, project_info, dependencies
        )
        files[".github/workflows/ci.yml"] = self._generate_ci_workflow(stack_id)

        return files

    def _generate_nodejs_express(
        self, project_info: Dict, dependencies: Dict
    ) -> Dict[str, str]:
        """Generate Node.js + Express project files."""
        files = {}

        package_json = {
            "name": project_info["repo_name"],
            "version": "0.1.0",
            "description": project_info["repo_description"],
            "main": "src/server.js",
            "scripts": {
                "start": "node src/server.js",
                "dev": "nodemon src/server.js",
                "test": "jest --coverage",
                "lint": "eslint src/",
            },
            "dependencies": dependencies["dependencies"],
            "devDependencies": dependencies["dev_dependencies"],
            "engines": {"node": ">=18.0.0"},
        }

        files["package.json"] = self._json_dumps(package_json)

        files["src/app.js"] = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const routes = require('./routes');
const errorHandler = require('./middleware/errorHandler');

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api', routes);

app.use(errorHandler);

module.exports = app;
'''

        files["src/server.js"] = '''require('dotenv').config();
const app = require('./app');
const logger = require('./utils/logger');

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});
'''

        files["src/routes/index.js"] = '''const express = require('express');
const router = express.Router();
const healthController = require('../controllers/healthController');

router.get('/health', healthController.checkHealth);

module.exports = router;
'''

        files["src/controllers/healthController.js"] = '''exports.checkHealth = (req, res) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
};
'''

        files["src/middleware/errorHandler.js"] = '''const logger = require('../utils/logger');

module.exports = (err, req, res, next) => {
  logger.error(err.stack);

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  res.status(statusCode).json({
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
};
'''

        files["src/utils/logger.js"] = '''const logger = {
  info: (message) => console.log(`[INFO] ${new Date().toISOString()} - ${message}`),
  error: (message) => console.error(`[ERROR] ${new Date().toISOString()} - ${message}`),
  warn: (message) => console.warn(`[WARN] ${new Date().toISOString()} - ${message}`)
};

module.exports = logger;
'''

        files["tests/unit/health.test.js"] = '''const request = require('supertest');
const app = require('../../src/app');

describe('Health Check', () => {
  test('GET /api/health should return 200', async () => {
    const response = await request(app).get('/api/health');
    expect(response.statusCode).toBe(200);
    expect(response.body).toHaveProperty('status', 'ok');
  });
});
'''

        files[".eslintrc.json"] = self._json_dumps(
            {
                "env": {"node": True, "es2021": True, "jest": True},
                "extends": "eslint:recommended",
                "parserOptions": {"ecmaVersion": 12},
                "rules": {"no-console": "off"},
            }
        )

        return files

    def _generate_python_fastapi(
        self, project_info: Dict, dependencies: Dict
    ) -> Dict[str, str]:
        """Generate Python + FastAPI project files."""
        files = {}

        deps = list(dependencies["dependencies"].items()) + list(
            dependencies["dev_dependencies"].items()
        )
        files["requirements.txt"] = "\n".join(f"{k}=={v}" for k, v in deps)

        files["src/main.py"] = '''"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import health
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
'''

        files["src/api/routes/health.py"] = '''"""Health check routes."""
from fastapi import APIRouter
from datetime import datetime
import time

router = APIRouter()

start_time = time.time()

@router.get("/health")
async def health_check():
    """Check application health."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": time.time() - start_time
    }
'''

        files["src/core/config.py"] = f'''"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "{project_info["repo_name"]}"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "{project_info["repo_description"]}"
    API_PREFIX: str = "/api"
    ALLOWED_HOSTS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
'''

        files["src/core/security.py"] = '''"""Security utilities."""
import secrets

def generate_secret_key(length: int = 32) -> str:
    """Generate a secure random secret key."""
    return secrets.token_urlsafe(length)
'''

        files["tests/conftest.py"] = '''"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)
'''

        files["tests/test_health.py"] = '''"""Test health check endpoint."""
def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
'''

        files["pytest.ini"] = '''[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --cov=src --cov-report=term-missing
'''

        files["src/__init__.py"] = ""
        files["src/api/__init__.py"] = ""
        files["src/api/routes/__init__.py"] = ""
        files["src/core/__init__.py"] = ""

        return files

    def _generate_react_typescript(
        self, project_info: Dict, dependencies: Dict
    ) -> Dict[str, str]:
        """Generate React + TypeScript project files."""
        files = {}

        package_json = {
            "name": project_info["repo_name"],
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview",
                "lint": "eslint src --ext ts,tsx",
            },
            "dependencies": dependencies["dependencies"],
            "devDependencies": dependencies["dev_dependencies"],
        }

        files["package.json"] = self._json_dumps(package_json)

        files["src/main.tsx"] = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''

        files["src/App.tsx"] = f'''import React from 'react'
import Header from './components/Header'

function App() {{
  return (
    <div className="App">
      <Header />
      <main>
        <h1>Welcome to {project_info["repo_name"]}</h1>
        <p>{project_info["repo_description"]}</p>
      </main>
    </div>
  )
}}

export default App
'''

        files["src/components/Header.tsx"] = '''import React from 'react'

const Header: React.FC = () => {
  return (
    <header>
      <nav>
        <h2>App Header</h2>
      </nav>
    </header>
  )
}

export default Header
'''

        files["src/vite-env.d.ts"] = '''/// <reference types="vite/client" />
'''

        files["index.html"] = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_info["repo_name"]}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''

        files["tsconfig.json"] = self._json_dumps(
            {
                "compilerOptions": {
                    "target": "ES2020",
                    "useDefineForClassFields": True,
                    "lib": ["ES2020", "DOM", "DOM.Iterable"],
                    "module": "ESNext",
                    "skipLibCheck": True,
                    "moduleResolution": "bundler",
                    "allowImportingTsExtensions": True,
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "noEmit": True,
                    "jsx": "react-jsx",
                    "strict": True,
                    "noUnusedLocals": True,
                    "noUnusedParameters": True,
                    "noFallthroughCasesInSwitch": True,
                },
                "include": ["src"],
                "references": [{"path": "./tsconfig.node.json"}],
            }
        )

        files["vite.config.ts"] = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
'''

        return files

    def _generate_python_cli(
        self, project_info: Dict, dependencies: Dict
    ) -> Dict[str, str]:
        """Generate Python CLI project files."""
        files = {}

        deps = list(dependencies["dependencies"].items()) + list(
            dependencies["dev_dependencies"].items()
        )
        files["requirements.txt"] = "\n".join(f"{k}=={v}" for k, v in deps)

        files["src/cli.py"] = f'''"""Command-line interface."""
import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option(version='0.1.0')
def cli():
    """{project_info["repo_description"]}"""
    pass

@cli.command()
@click.argument('name')
def hello(name):
    """Say hello to NAME."""
    console.print(f"[bold green]Hello, {{name}}![/bold green]")

if __name__ == '__main__':
    cli()
'''

        files["setup.py"] = f'''from setuptools import setup, find_packages

setup(
    name="{project_info["repo_name"]}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click==8.1.7",
        "rich==13.7.0",
    ],
    entry_points={{
        'console_scripts': [
            '{project_info["repo_name"]}=src.cli:cli',
        ],
    }},
)
'''

        files["tests/test_cli.py"] = '''"""Test CLI commands."""
from click.testing import CliRunner
from src.cli import cli

def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', 'World'])
    assert result.exit_code == 0
    assert 'Hello, World!' in result.output
'''

        files["src/__init__.py"] = ""

        return files

    def _generate_go_cli(
        self, project_info: Dict, dependencies: Dict
    ) -> Dict[str, str]:
        """Generate Go CLI project files."""
        files = {}

        files["go.mod"] = f'''module {project_info["repo_name"]}

go 1.21

require github.com/spf13/cobra v1.8.0
'''

        files["main.go"] = f'''package main

import "{project_info["repo_name"]}/cmd"

func main() {{
    cmd.Execute()
}}
'''

        files["cmd/root.go"] = f'''package cmd

import (
    "fmt"
    "os"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{{
    Use:   "{project_info["repo_name"]}",
    Short: "{project_info["repo_description"]}",
    Run: func(cmd *cobra.Command, args []string) {{
        fmt.Println("Hello from {project_info["repo_name"]}!")
    }},
}}

func Execute() {{
    if err := rootCmd.Execute(); err != nil {{
        fmt.Println(err)
        os.Exit(1)
    }}
}}
'''

        return files

    def _generate_python_ml(
        self, project_info: Dict, dependencies: Dict
    ) -> Dict[str, str]:
        """Generate Python ML/Data Science project files."""
        files = {}

        deps = list(dependencies["dependencies"].items()) + list(
            dependencies["dev_dependencies"].items()
        )
        files["requirements.txt"] = "\n".join(f"{k}=={v}" for k, v in deps)

        files["src/model.py"] = '''"""Machine learning model."""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class CustomModel(BaseEstimator, ClassifierMixin):
    """Custom ML model."""

    def __init__(self, param=1.0):
        self.param = param

    def fit(self, X, y):
        """Fit the model."""
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        """Make predictions."""
        return np.zeros(len(X), dtype=int)
'''

        files["src/train.py"] = '''"""Model training script."""
import numpy as np
from src.model import CustomModel

def train_model():
    """Train the model."""
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)

    model = CustomModel()
    model.fit(X, y)

    print("Model trained successfully!")
    return model

if __name__ == '__main__':
    train_model()
'''

        files["tests/test_model.py"] = '''"""Test ML model."""
import numpy as np
from src.model import CustomModel

def test_model_fit():
    model = CustomModel()
    X = np.random.rand(10, 5)
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    model.fit(X, y)
    assert hasattr(model, 'classes_')
'''

        files["src/__init__.py"] = ""

        return files

    def _generate_gitignore(self, stack_id: str) -> str:
        """Generate .gitignore for tech stack."""
        common = """# Environment variables
.env
*.env
!.env.example

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""

        if "nodejs" in stack_id or "react" in stack_id:
            return common + """
# Node
node_modules/
npm-debug.log
yarn-error.log
dist/
build/
.npm
"""
        elif "python" in stack_id:
            return common + """
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
"""
        elif "go" in stack_id:
            return common + """
# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
vendor/
"""
        return common

    def _generate_env_example(self, stack_id: str) -> str:
        """Generate .env.example file."""
        if "nodejs" in stack_id:
            return """PORT=3000
NODE_ENV=development
"""
        elif "python" in stack_id:
            return """DEBUG=True
LOG_LEVEL=INFO
"""
        return ""

    def _generate_license(self, project_info: Dict) -> str:
        """Generate LICENSE file."""
        return f"""MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    def _generate_readme(
        self, stack_id: str, project_info: Dict, dependencies: Dict
    ) -> str:
        """Generate README.md file."""
        runtime = dependencies.get("runtime", "")
        pkg_manager = dependencies.get("package_manager", "")

        setup_commands = {
            "nodejs-express": "npm install\nnpm run dev",
            "python-fastapi": "pip install -r requirements.txt\nuvicorn src.main:app --reload",
            "react-typescript": "npm install\nnpm run dev",
            "python-cli": "pip install -r requirements.txt\npython src/cli.py",
            "go-cli": "go mod download\ngo run main.go",
            "python-ml": "pip install -r requirements.txt\npython src/train.py",
        }

        test_commands = {
            "nodejs-express": "npm test",
            "python-fastapi": "pytest",
            "react-typescript": "npm test",
            "python-cli": "pytest",
            "go-cli": "go test ./...",
            "python-ml": "pytest",
        }

        return f"""# {project_info['repo_name']}

{project_info['repo_description']}

## Requirements

- {runtime}

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/{project_info['repo_name']}.git
cd {project_info['repo_name']}
```

2. Install dependencies and run:
```bash
{setup_commands.get(stack_id, 'See documentation')}
```

## Testing

Run tests with:
```bash
{test_commands.get(stack_id, 'See documentation')}
```

## Project Structure

```
.
├── src/          # Source code
├── tests/        # Test files
├── .github/      # GitHub workflows
└── README.md     # This file
```

## API Documentation

### Health Check
- **GET** `/api/health` - Check application health

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

{project_info['license']}
"""

    def _generate_ci_workflow(self, stack_id: str) -> str:
        """Generate GitHub Actions CI workflow."""
        if "nodejs" in stack_id or "react" in stack_id:
            return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm test

    - name: Build
      run: npm run build --if-present
"""
        elif "python" in stack_id:
            return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run linter
      run: |
        pip install pylint black
        black --check src/
        pylint src/

    - name: Run tests
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
"""
        elif "go" in stack_id:
            return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'

    - name: Build
      run: go build -v ./...

    - name: Test
      run: go test -v ./...
"""
        return ""

    def _json_dumps(self, obj: Dict) -> str:
        """Convert dict to formatted JSON string."""
        import json

        return json.dumps(obj, indent=2)
