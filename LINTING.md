# Code Linting & Formatting

Industry-standard Python linting tools maintain code quality.

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Black** | Code formatter | `black src/ main.py` |
| **isort** | Import sorter | `isort src/ main.py` |
| **Ruff** | Fast linter | `ruff check --fix src/ main.py` |
| **Flake8** | PEP 8 validation | `flake8 src/ main.py` |
| **Pylint** | Code analysis | `pylint src/ main.py` |
| **mypy** | Type checker | `mypy src/ main.py` |
| **Bandit** | Security scanner | `bandit -r src/` |
| **pre-commit** | Git hooks | `pre-commit run --all-files` |

## Installation

```bash
# Install all tools
pip install -r requirements-dev.txt

# Setup git hooks
pre-commit install
pre-commit run --all-files
```

## Quick Commands

### Format Code
```bash
black src/ main.py
isort src/ main.py
```

### Check Code
```bash
ruff check src/ main.py
flake8 src/ main.py
pylint src/ main.py
mypy src/ main.py
bandit -r src/
```

### Auto-Fix Issues
```bash
ruff check --fix src/ main.py
black src/ main.py
isort src/ main.py
```

### Run All Pre-commit Hooks
```bash
pre-commit run --all-files
```

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Black, isort, pylint, mypy, pytest settings |
| `.flake8` | Flake8 configuration |
| `ruff.toml` | Ruff linter configuration |
| `.editorconfig` | IDE formatting rules |
| `.pre-commit-config.yaml` | Git pre-commit hooks |
| `.vscode/settings.json` | VS Code settings |
| `.bandit` | Security checker settings |

## Code Style Standards

### Line Length: 100 characters
```python
# All lines ≤ 100 characters
```

### Import Order
```python
# 1. Standard library
import os
import sys

# 2. Third-party
from google.cloud import aiplatform
from dotenv import load_dotenv

# 3. Local
from src.logger import get_logger
```

### Naming Conventions
- **Functions/Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** `_leading_underscore`

### Type Hints
```python
from typing import Dict, List, Optional, Tuple

def process_data(
    items: List[str],
    validate: bool = True
) -> Dict[str, str]:
    """Process items with optional validation."""
    pass
```

### Docstrings (Google Style)
```python
def parse_template(template_text: str, validate: bool = True) -> dict:
    """Parse character template into JSON structure.
    
    Args:
        template_text: Plain text template content
        validate: Whether to validate structure (default: True)
        
    Returns:
        Dict with sections as keys and fields as nested dicts
        
    Raises:
        ValueError: If template is invalid and validate=True
    """
    pass
```

## Pre-commit Workflow

Hooks run automatically on `git commit`:
1. Check trailing whitespace
2. Check file endings
3. Validate YAML/JSON
4. Format with Black
5. Sort imports with isort
6. Run Flake8
7. Run Ruff
8. Type check with mypy
9. Security scan with Bandit

### Skip Pre-commit (Not Recommended)
```bash
git commit --no-verify
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| **Line too long** | `black src/` (auto-wraps) |
| **Unsorted imports** | `isort src/` |
| **Unused imports** | `ruff check --fix src/` |
| **Type errors** | Add type hints to functions |
| **Security warnings** | Review and fix (don't ignore) |

## VS Code Integration

### Recommended Extensions
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Black Formatter (ms-python.black-formatter)
- Ruff (charliermarsh.ruff)

### Install from Command Line
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
```

Auto-format on save is enabled in `.vscode/settings.json`

## Ignoring Rules

### Disable Specific Line
```python
# ruff: noqa: E501
very_long_line_that_cannot_be_split()
```

### Disable for Function
```python
# ruff: noqa: C901
def complex_function():  # Too complex
    pass
```

### Disable for File
```python
# ruff: noqa: F401
from unused_module import something  # API compatibility
```

### Security Issues (Never Ignore Without Reason)
```python
# bandit: disable=hardcoded_sql_string
# Reason: Test fixture only, not production
query = "SELECT * FROM users WHERE id = '1' OR '1'='1'"
```

## Best Practices

✅ **Always run before pushing:**
```bash
pre-commit run --all-files
```

✅ **Keep lines ≤ 100 characters**

✅ **Add type hints to all functions**

✅ **Write docstrings for public functions**

✅ **Use descriptive variable names**

✅ **Avoid magic numbers** (use constants instead)

## Contributing

All contributions must pass linting:

```bash
# 1. Format
black src/ main.py
isort src/ main.py

# 2. Auto-fix
ruff check --fix src/ main.py

# 3. Lint
flake8 src/ main.py
pylint src/ main.py

# 4. Type check
mypy src/ main.py

# 5. Security scan
bandit -r src/

# 6. Commit
git add .
git commit -m "Your message"
```

**No commits accepted unless all linters pass!**

## CI/CD Integration

GitHub Actions example (runs on every push/PR):
```yaml
- run: pip install -r requirements-dev.txt
- run: black --check src/ main.py
- run: isort --check-only src/ main.py
- run: ruff check src/ main.py
- run: flake8 src/ main.py
- run: mypy src/ main.py
- run: bandit -r src/
```

## Resources

- [Black](https://black.readthedocs.io/)
- [isort](https://pycqa.github.io/isort/)
- [Ruff](https://docs.astral.sh/ruff/)
- [Flake8](https://flake8.pycqa.org/)
- [Pylint](https://pylint.pycqa.org/)
- [mypy](https://mypy.readthedocs.io/)
- [Bandit](https://bandit.readthedocs.io/)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
