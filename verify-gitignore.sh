#!/bin/bash
# Script to verify .gitignore is working correctly

echo "🔍 Verifying .gitignore configuration..."
echo ""

# Initialize temporary git repo
git init > /dev/null 2>&1

# Check for sensitive files
echo "Checking for sensitive files that should be ignored:"
echo ""

ERRORS=0

# Check supabase.env (should NOT be tracked)
if git add -A -n 2>&1 | grep -q "add 'supabase.env'$"; then
    echo "❌ FAIL: supabase.env would be committed (contains secrets!)"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ PASS: supabase.env is properly ignored"
fi

# Check SSL directory (should NOT be tracked)
if git add -A -n 2>&1 | grep -q "add 'ssl/"; then
    echo "❌ FAIL: SSL files would be committed"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ PASS: SSL certificates are properly ignored"
fi

# Check node_modules (should NOT be tracked)
if [ -d "node_modules" ]; then
    if git add -A -n 2>&1 | grep -q "add 'node_modules/"; then
        echo "❌ FAIL: node_modules would be committed"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ PASS: node_modules is properly ignored"
    fi
else
    echo "⚠️  SKIP: node_modules doesn't exist yet"
fi

# Check Python cache (should NOT be tracked)
if git add -A -n 2>&1 | grep -q "__pycache__"; then
    echo "❌ FAIL: Python cache files would be committed"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ PASS: Python cache is properly ignored"
fi

echo ""
echo "Checking that template files ARE tracked:"
echo ""

# Check supabase.env.example (SHOULD be tracked)
if git add -A -n 2>&1 | grep -q "add 'supabase.env.example'"; then
    echo "✅ PASS: supabase.env.example will be tracked"
else
    echo "❌ FAIL: supabase.env.example is missing or ignored"
    ERRORS=$((ERRORS + 1))
fi

# Check source files (SHOULD be tracked)
if git add -A -n 2>&1 | grep -q "add 'src/"; then
    echo "✅ PASS: Source files will be tracked"
else
    echo "❌ FAIL: Source files are missing or ignored"
    ERRORS=$((ERRORS + 1))
fi

# Cleanup
rm -rf .git

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ SUCCESS: All checks passed!"
    echo "Your .gitignore is properly configured."
else
    echo "❌ FAILURE: $ERRORS check(s) failed"
    echo "Please review your .gitignore configuration."
    exit 1
fi

