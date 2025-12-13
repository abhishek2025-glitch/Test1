# Contributing to AI Code Generator

Thank you for your interest in contributing to the AI Code Generator project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-code-generator.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Create a `.env` file based on `.env.example`

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting: `black .`
- Run Pylint for linting: `pylint src/`
- Type hints are encouraged

### Testing
- Write unit tests for all new features
- Maintain 70%+ code coverage
- Run tests: `pytest tests/ -v --cov=src`

### Commit Messages
- Use clear, descriptive commit messages
- Format: `<type>: <description>`
- Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Process

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make your changes and commit them
3. Write/update tests
4. Ensure all tests pass
5. Update documentation if needed
6. Push to your fork and submit a pull request
7. Wait for code review

## Adding New Tech Stack Templates

To add support for a new tech stack:

1. Create template files in `templates/[stack_name]/`
2. Update `tech_stack_selector.py` with the new stack detection logic
3. Update `code_generator.py` to handle the new stack
4. Add tests for the new stack
5. Update README with the new stack support

## Reporting Issues

- Check existing issues before creating new ones
- Provide detailed reproduction steps
- Include error messages and logs
- Specify your environment (OS, Python version, etc.)

## Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing!
