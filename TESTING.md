# Testing Guide

## Running Tests

### All Tests
```bash
pytest
```

### With Coverage
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

### Specific Test File
```bash
pytest tests/test_input_processor.py -v
```

### Quick Test Mode
```bash
pytest -q
```

## Test Structure

### Unit Tests
- `test_input_processor.py` - Input validation and processing
- `test_tech_stack_selector.py` - Tech stack selection logic
- `test_architecture_planner.py` - Architecture planning
- `test_code_generator.py` - Code generation
- `test_quality_assurance.py` - QA checks
- `test_git_operations.py` - Git operations
- `test_response_formatter.py` - Response formatting

### Integration Tests
Integration tests requiring GitHub credentials are marked with `@pytest.mark.integration` and can be run separately:

```bash
pytest -m integration
```

**Note:** Integration tests require a valid `GITHUB_TOKEN` environment variable.

## Coverage Goals

- **Overall Target:** 60%+
- **Core Modules:** 70%+
  - `input_processor.py`: 95%
  - `tech_stack_selector.py`: 100%
  - `architecture_planner.py`: 100%
  - `code_generator.py`: 74%
  - `quality_assurance.py`: 95%

## Testing Without GitHub

Use the `--skip-github` flag to test code generation without GitHub API:

```bash
python -m src.main -d "Build a REST API" --skip-github
```

## Demo Mode

Run the demo script to see the system in action:

```bash
python demo.py
```

This generates a complete project locally without pushing to GitHub.

## Continuous Integration

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs:
- Tests with coverage
- Linting (pylint, black)
- Security checks (bandit, safety)

## Writing New Tests

### Test Structure
```python
class TestModuleName:
    """Test cases for ModuleName."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.instance = ModuleName()
    
    def test_feature_name(self):
        """Test specific feature."""
        result = self.instance.method()
        assert result == expected
```

### Best Practices
1. One assertion per test when possible
2. Use descriptive test names
3. Test both success and failure cases
4. Mock external dependencies (GitHub API, etc.)
5. Clean up resources in teardown methods

## Troubleshooting

### Import Errors
Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Coverage Too Low
Focus on:
1. Adding tests for uncovered branches
2. Testing error conditions
3. Testing edge cases

### Test Failures
1. Check error messages carefully
2. Run individual failing test with `-v` flag
3. Use `--pdb` to drop into debugger on failure
