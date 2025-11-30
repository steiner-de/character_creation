# Code Quality & Standards

This document outlines the code quality standards, linting infrastructure, and best practices for the D&D Character Creation system.

## Overview

The project uses a comprehensive suite of tools to maintain high code quality, consistency, and security:

| Tool | Purpose | Check | Fix |
|------|---------|-------|-----|
| **Black** | Code formatting | ✓ | ✓ |
| **isort** | Import organization | ✓ | ✓ |
| **Ruff** | Fast linting | ✓ | ✓ |
| **Flake8** | PEP 8 compliance | ✓ | - |
| **Pylint** | Code analysis | ✓ | - |
| **mypy** | Type checking | ✓ | - |
| **Bandit** | Security scanning | ✓ | - |
| **pre-commit** | Git automation | ✓ (on commit) | ✓ |

## Quick Start

### 1. Install Development Tools
```bash
# Using the setup script
./setup-linting.sh          # Linux/macOS
.\setup-linting.ps1         # Windows (PowerShell)

# Or manually
pip install -r requirements-dev.txt
pre-commit install
```

### 2. Format Your Code
```bash
black src/ main.py
isort src/ main.py
```

### 3. Check Your Code
```bash
ruff check src/ main.py
flake8 src/ main.py
mypy src/ main.py
bandit -r src/
```

### 4. Commit (Hooks Run Automatically)
```bash
git add .
git commit -m "Your message"
```

## Project Standards

### Line Length: 100 characters
All code and comments should respect the 100-character line limit. Black enforces this automatically.

### Python Version: 3.10+
All code must be compatible with Python 3.10 or higher.

### Code Style: PEP 8
Follow [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) with the exceptions noted below.

### Import Organization
Follow isort conventions (3 groups):
```python
# 1. Standard library
import os
import sys
from typing import Dict, List

# 2. Third-party
from google.cloud import aiplatform
from dotenv import load_dotenv

# 3. First-party/Local
from src.logger import get_logger
from src.gdocs import create_services
```

## Code Structure Requirements

### 1. Type Hints
All functions must have type hints:

```python
# ✓ Good
def parse_template(template: str, validate: bool = True) -> dict:
    """Parse template into structure."""
    pass

# ✗ Bad
def parse_template(template, validate=True):
    """Parse template into structure."""
    pass
```

### 2. Docstrings
Public functions/classes must have docstrings (Google format):

```python
def generate_character(
    template: str,
    character_inputs: Dict[str, str],
    use_json: bool = False
) -> Tuple[str, dict]:
    """Generate a D&D character from template.
    
    Uses Gemini AI to fill the template with generated content
    based on character specifications.
    
    Args:
        template: Google Doc template ID or text
        character_inputs: Dict with Name, Age, Occupation, etc.
        use_json: If True, output structured JSON (default: False)
        
    Returns:
        Tuple of (google_doc_url, character_json) if use_json=True,
        otherwise (google_doc_url, None)
        
    Raises:
        ValueError: If template is invalid
        PermissionError: If cannot access Google Docs
        
    Example:
        >>> inputs = {"Name": "Aragorn", "Age": "Adult"}
        >>> url, data = generate_character(template_id, inputs, use_json=True)
        >>> print(data['Basic Info']['Name'])
        "Aragorn"
    """
```

### 3. Naming Conventions
```python
# Functions and variables: snake_case
def create_character():
    pass

MAX_LEVEL = 20

# Classes: PascalCase
class CharacterGenerator:
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_MODEL = "gemini-2.5-flash"

# Private/Internal: _leading_underscore
def _internal_helper():
    pass
```

### 4. Error Handling
```python
# ✓ Specific exceptions
try:
    data = json.loads(response)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON response: {e}")
    raise ValueError("Gemini response was not valid JSON") from e

# ✗ Bare except
except:
    pass
```

### 5. Logging
Use the centralized logger:

```python
from src.logger import get_logger

logger = get_logger(__name__)

logger.debug("Parsing template with validate=True")
logger.info(f"Created character: {name}")
logger.warning("Template missing optional field: Age")
logger.error(f"Failed to access Google Doc: {doc_id}")
```

## Configuration Files

### pyproject.toml
Central configuration for Black, isort, Pylint, mypy, pytest, and coverage.

### .flake8
Flake8 linting rules (max 100 chars, ignore E501, W503, E203).

### ruff.toml
Ruff fast linter configuration with comprehensive rule set.

### .pre-commit-config.yaml
Git pre-commit hooks that run automatically on commit.

### .editorconfig
Cross-editor formatting rules for consistent formatting in any IDE.

### .vscode/settings.json
VS Code specific settings for Black, Pylint, Flake8 integration.

## Pre-commit Workflow

### What Hooks Do
Automatically run on every `git commit`:
1. Check trailing whitespace
2. Check file endings
3. Validate YAML/JSON files
4. Format code with Black
5. Organize imports with isort
6. Lint with Flake8
7. Lint with Ruff
8. Type check with mypy
9. Security scan with Bandit

### If Hook Fails
The commit is blocked and you must fix the issues:

```bash
# Hook failed? See the error
# Fix the issue
black src/ main.py
isort src/ main.py
ruff check --fix src/ main.py

# Try again
git commit -m "Your message"
```

### Bypass Hooks (Emergency Only)
```bash
git commit --no-verify
```

**⚠️ Never merge with `--no-verify` enabled!**

## Development Workflow

### 1. Make Your Changes
Write code in your preferred IDE (VS Code recommended).

### 2. Format Code
```bash
black src/ main.py
isort src/ main.py
```

### 3. Check for Issues
```bash
ruff check src/ main.py
flake8 src/ main.py
pylint src/ main.py
mypy src/ main.py
bandit -r src/
```

### 4. Auto-Fix What You Can
```bash
ruff check --fix src/ main.py
```

### 5. Review and Commit
```bash
git add .
git commit -m "Feature: Add JSON export functionality"
# Pre-commit hooks run automatically
```

### 6. Push
```bash
git push
```

## Common Issues & Solutions

### Issue: Line Too Long
```python
# ✗ Too long (exceeds 100 chars)
result = very_long_function_name(arg1, arg2, arg3, arg4, arg5, arg6, arg7)

# ✓ Split across lines
result = very_long_function_name(
    arg1, arg2, arg3, arg4,
    arg5, arg6, arg7
)
```

**Fix**: Run `black src/`

### Issue: Unsorted Imports
```python
# ✗ Wrong order
from src.logger import get_logger
import os
from google.cloud import aiplatform

# ✓ Correct order
import os

from google.cloud import aiplatform

from src.logger import get_logger
```

**Fix**: Run `isort src/`

### Issue: Type Errors
```python
# ✗ No type hints
def parse_json(data):
    return json.loads(data)

# ✓ With type hints
def parse_json(data: str) -> dict:
    return json.loads(data)
```

**Fix**: Add type hints and run `mypy src/`

### Issue: Unused Import
```python
# ✗ Not used
import json
from datetime import datetime

# ✓ Removed
import json
```

**Fix**: Run `ruff check --fix src/`

### Issue: Security Warning from Bandit
```bash
# See the warning
bandit -r src/

# Example: Hardcoded secrets
# ✗ Bad
API_KEY = "abc123xyz789"

# ✓ Good
API_KEY = os.getenv("GEMINI_API_KEY")
```

**Fix**: Never commit secrets - use environment variables!

## Best Practices

### 1. Type Hints First
Write type hints as you write code:

```python
from typing import Dict, List, Optional

def generate_dnd_class(
    species: str,
    desired_class: str,
    level: int = 1
) -> Dict[str, str]:
    """Generate D&D class details."""
    pass
```

### 2. Docstrings for Public APIs
Every public function needs a docstring:

```python
def flatten_json_for_text(data: dict) -> str:
    """Convert JSON structure back to readable text for Google Docs."""
    pass
```

### 3. Meaningful Variable Names
```python
# ✗ Unclear
d = create_doc(t)

# ✓ Clear
character_doc = create_doc(template_id)
```

### 4. Avoid Magic Numbers
```python
# ✗ Magic number
if level > 20:
    raise ValueError("Level too high")

# ✓ Named constant
MAX_CHARACTER_LEVEL = 20
if level > MAX_CHARACTER_LEVEL:
    raise ValueError(f"Level exceeds maximum: {MAX_CHARACTER_LEVEL}")
```

### 5. Use Logging, Not Print
```python
# ✗ Not visible in logs
print(f"Creating character: {name}")

# ✓ Logged and trackable
logger.info(f"Creating character: {name}")
```

### 6. Specific Exceptions
```python
# ✗ Too broad
except Exception:
    pass

# ✓ Specific
except (json.JSONDecodeError, ValueError) as e:
    logger.error(f"Invalid character data: {e}")
    raise
```

## Performance Considerations

### Run Time for Checks
- **Black**: ~200ms on full codebase
- **isort**: ~100ms on full codebase
- **Ruff**: ~50ms on full codebase (fastest!)
- **Flake8**: ~300ms on full codebase
- **mypy**: ~1-2s on full codebase
- **Bandit**: ~200ms on full codebase
- **All together**: ~3-5 seconds

These are all acceptable for pre-commit hooks.

## VS Code Setup

### Recommended Extensions
1. **Python** (ms-python.python) - Core Python support
2. **Pylance** (ms-python.vscode-pylance) - Fast type checking
3. **Black Formatter** (ms-python.black-formatter) - Black integration
4. **Ruff** (charliermarsh.ruff) - Ruff integration
5. **autoDocstring** (njpwerner.autodocstring) - Auto-docstrings

### Auto-Format on Save
Configured in `.vscode/settings.json`:
- Black formatting: Enabled
- isort import sorting: Enabled
- Linting on save: Enabled
- Format on paste: Enabled

### Install Extensions
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
code --install-extension njpwerner.autodocstring
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - run: pip install -r requirements-dev.txt
      
      - name: Format check
        run: black --check src/ main.py
      
      - name: Import sort check
        run: isort --check-only src/ main.py
      
      - name: Linting
        run: |
          ruff check src/ main.py
          flake8 src/ main.py
          pylint src/ main.py
      
      - name: Type checking
        run: mypy src/ main.py
      
      - name: Security scan
        run: bandit -r src/
```

## Exceptions and Disabling Rules

### Disable Specific Line
```python
# ruff: noqa: E501
very_long_line_that_cannot_be_broken_without_compromising_readability()
```

### Disable for Function
```python
# pylint: disable=too-complex
def complex_algorithm():
    pass
```

### Never Disable (Security)
Never disable Bandit security checks without strong justification and comments:

```python
# WARNING: Using insecure deserialization - only for test data
# bandit: disable=insecure-pickle
test_data = pickle.loads(untrusted_data)
```

## Resources

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Type Hints Guide](https://typing.readthedocs.io/)

## Summary

The code quality infrastructure is designed to:
- ✅ Maintain consistent formatting across the project
- ✅ Catch bugs early through type checking
- ✅ Identify security issues before deployment
- ✅ Make code reviews faster and focused
- ✅ Reduce time spent on style discussions

**All commits must pass all checks before merging!**

For detailed information on each tool, see `LINTING.md`.
