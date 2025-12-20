#!/bin/bash
# Install git hooks for ontology validation

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing pre-commit hook..."

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

echo "✅ Hooks installed successfully"
