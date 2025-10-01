#!/bin/bash

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Generate self-signed SSL certificate for cookr.dev
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/cookr.dev.key \
  -out ssl/cookr.dev.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=cookr.dev" \
  -addext "subjectAltName=DNS:cookr.dev,DNS:api.cookr.dev,DNS:*.cookr.dev"

echo "✓ SSL certificates generated in ./ssl directory"
echo "  - ssl/cookr.dev.crt"
echo "  - ssl/cookr.dev.key"

