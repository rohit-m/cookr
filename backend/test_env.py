#!/usr/bin/env python3
"""Quick script to test if environment variables are loading"""
import os

print("=" * 50)
print("Environment Variable Check")
print("=" * 50)

# TikTok variables
tiktok_client_key = os.getenv("TIKTOK_CLIENT_KEY")
tiktok_client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
tiktok_redirect_uri = os.getenv("TIKTOK_REDIRECT_URI")

print(f"\nTIKTOK_CLIENT_KEY: {'✓ Set' if tiktok_client_key else '✗ Not set'}")
if tiktok_client_key:
    print(f"  Value: {tiktok_client_key[:10]}... (length: {len(tiktok_client_key)})")

print(f"\nTIKTOK_CLIENT_SECRET: {'✓ Set' if tiktok_client_secret else '✗ Not set'}")
if tiktok_client_secret:
    print(f"  Value: {tiktok_client_secret[:10]}... (length: {len(tiktok_client_secret)})")

print(f"\nTIKTOK_REDIRECT_URI: {tiktok_redirect_uri or '✗ Not set'}")

print("\n" + "=" * 50)
print("All environment variables:")
print("=" * 50)
for key in sorted(os.environ.keys()):
    if 'TIKTOK' in key or 'SUPABASE' in key:
        print(f"  {key}")

