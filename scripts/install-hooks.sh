#!/bin/bash
# Install git hooks for ontology validation
#
# Usage:
#   ./scripts/install-hooks.sh          # Install simple hook
#   ./scripts/install-hooks.sh --full   # Install pre-commit framework

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [ "$1" == "--full" ]; then
    echo "Installing pre-commit framework..."

    # Check if pre-commit is installed
    if ! command -v pre-commit &> /dev/null; then
        echo "Installing pre-commit..."
        pip install pre-commit
    fi

    cd "$REPO_ROOT"
    pre-commit install

    echo ""
    echo "✅ Pre-commit framework installed"
    echo ""
    echo "Hooks enabled:"
    echo "  - trailing-whitespace"
    echo "  - end-of-file-fixer"
    echo "  - check-yaml"
    echo "  - black (code formatting)"
    echo "  - flake8 (linting)"
    echo "  - validate-ontologies"
    echo ""
    echo "Run 'pre-commit run --all-files' to check all files"
    exit 0
fi

# Simple hook installation (default)
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing simple pre-commit hook..."

cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook: validate ontology integrity

echo "Running ontology validation..."

python3 scripts/validate.py
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo ""
    echo "❌ Commit blocked: validation failed"
    echo "Fix the issues above and try again."
    exit 1
fi

echo "✅ Validation passed"
exit 0
EOF

chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Simple hook installed"
echo ""
echo "For full pre-commit framework (black, flake8, etc.), run:"
echo "  ./scripts/install-hooks.sh --full"
