#!/bin/bash

# Script to add cookr.dev domains to /etc/hosts

echo "Setting up cookr.dev domains..."

# Check if cookr.dev already exists in hosts file
if grep -q "cookr.dev" /etc/hosts; then
    echo "✓ cookr.dev already configured in /etc/hosts"
else
    echo "Adding cookr.dev domains to /etc/hosts (requires sudo)..."
    echo ""
    echo "Please run these commands manually:"
    echo ""
    echo "  echo '127.0.0.1       cookr.dev' | sudo tee -a /etc/hosts"
    echo "  echo '127.0.0.1       api.cookr.dev' | sudo tee -a /etc/hosts"
    echo ""
    echo "Or edit /etc/hosts manually and add:"
    echo "  127.0.0.1       cookr.dev"
    echo "  127.0.0.1       api.cookr.dev"
fi

echo ""
echo "After adding to hosts file, you can access:"
echo "  Frontend: https://cookr.dev"
echo "  Backend:  https://api.cookr.dev"
