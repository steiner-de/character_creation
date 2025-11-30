#!/bin/bash
# Setup script for linting tools and development environment
# Run: chmod +x setup-linting.sh && ./setup-linting.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  D&D Character Creation - Linting Setup                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Error: Virtual environment not activated!"
    echo ""
    echo "Please activate your virtual environment first:"
    echo "  Linux/macOS: source venv/bin/activate"
    echo "  Windows: venv\\Scripts\\activate.bat"
    exit 1
fi

echo "✓ Virtual environment active: $VIRTUAL_ENV"
echo ""

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -r requirements-dev.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

echo "✓ Dependencies installed successfully!"
echo ""

# Setup pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

if [ $? -ne 0 ]; then
    echo "⚠️  Pre-commit installation had issues, but continuing..."
fi

echo "✓ Pre-commit hooks configured!"
echo ""

# Display setup summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Setup Complete! Available Commands:                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Format Code:"
echo "  black src/ main.py"
echo "  isort src/ main.py"
echo ""
echo "Check Code:"
echo "  ruff check src/ main.py"
echo "  flake8 src/ main.py"
echo "  pylint src/ main.py"
echo "  mypy src/ main.py"
echo "  bandit -r src/"
echo ""
echo "Pre-commit:"
echo "  pre-commit run --all-files     # Run all hooks"
echo "  git commit                     # Auto-runs hooks"
echo ""
echo "Full Quality Check:"
echo "  black src/ main.py && isort src/ main.py && ruff check --fix src/ main.py && flake8 src/ main.py && mypy src/ main.py && bandit -r src/"
echo ""
echo "More info: See LINTING.md"
