# Setup script for linting tools and development environment (Windows)
# Run: .\setup-linting.ps1

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  D&D Character Creation - Linting Setup (Windows)          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "❌ Error: Virtual environment not activated!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please activate your virtual environment first:" -ForegroundColor Yellow
    Write-Host "  Command: venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "If you get an execution policy error, run:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    exit 1
}

Write-Host "✓ Virtual environment active: $env:VIRTUAL_ENV" -ForegroundColor Green
Write-Host ""

# Install development dependencies
Write-Host "📦 Installing development dependencies..." -ForegroundColor Cyan
pip install -r requirements-dev.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Setup pre-commit hooks
Write-Host "🔧 Setting up pre-commit hooks..." -ForegroundColor Cyan
pre-commit install

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Pre-commit installation had issues, but continuing..." -ForegroundColor Yellow
}

Write-Host "✓ Pre-commit hooks configured!" -ForegroundColor Green
Write-Host ""

# Display setup summary
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Setup Complete! Available Commands:                       ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Format Code:" -ForegroundColor Yellow
Write-Host "  black src\ main.py" -ForegroundColor Cyan
Write-Host "  isort src\ main.py" -ForegroundColor Cyan
Write-Host ""

Write-Host "Check Code:" -ForegroundColor Yellow
Write-Host "  ruff check src\ main.py" -ForegroundColor Cyan
Write-Host "  flake8 src\ main.py" -ForegroundColor Cyan
Write-Host "  pylint src\ main.py" -ForegroundColor Cyan
Write-Host "  mypy src\ main.py" -ForegroundColor Cyan
Write-Host "  bandit -r src\" -ForegroundColor Cyan
Write-Host ""

Write-Host "Pre-commit:" -ForegroundColor Yellow
Write-Host "  pre-commit run --all-files     # Run all hooks" -ForegroundColor Cyan
Write-Host "  git commit                     # Auto-runs hooks" -ForegroundColor Cyan
Write-Host ""

Write-Host "Full Quality Check:" -ForegroundColor Yellow
Write-Host "  black src\ main.py; isort src\ main.py; ruff check --fix src\ main.py; flake8 src\ main.py; mypy src\ main.py; bandit -r src\" -ForegroundColor Cyan
Write-Host ""

Write-Host "More info: See LINTING.md" -ForegroundColor Gray
