from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
import httpx
import secrets
import hashlib
import base64
import json
from urllib.parse import urlencode, quote

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TikTok OAuth configuration
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", "https://api.cookr.dev/auth/tiktok/callback")

# TikTok OAuth endpoints
TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
TIKTOK_USER_INFO_URL = "https://open.tiktokapis.com/v2/user/info/"

# Store state tokens and code verifiers (in production, use Redis or database)
auth_states = {}

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables"""
    return {
        "tiktok_client_key_set": bool(TIKTOK_CLIENT_KEY),
        "tiktok_client_key_value": TIKTOK_CLIENT_KEY,
        "tiktok_client_secret_set": bool(TIKTOK_CLIENT_SECRET),
        "tiktok_redirect_uri": TIKTOK_REDIRECT_URI,
        "auth_url": TIKTOK_AUTH_URL,
        "token_url": TIKTOK_TOKEN_URL,
    }

@app.get("/debug/callback")
async def debug_callback(code: str = None, state: str = None, error: str = None, error_description: str = None):
    """Debug endpoint to see all callback parameters"""
    return {
        "code": code,
        "state": state,
        "error": error,
        "error_description": error_description,
        "state_exists": state in auth_states if state else False,
    }

def generate_code_verifier():
    """Generate a code verifier for PKCE"""
    return secrets.token_urlsafe(32)

def generate_code_challenge(verifier):
    """Generate a code challenge from the verifier"""
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).decode().rstrip('=')
    return challenge

# TikTok OAuth endpoints
@app.get("/auth/tiktok")
async def tiktok_auth():
    """Initiate TikTok OAuth flow with PKCE"""
    if not TIKTOK_CLIENT_KEY:
        raise HTTPException(
            status_code=500, 
            detail=f"TikTok client key not configured. Check supabase.env file and restart Docker containers."
        )
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Generate PKCE code verifier and challenge
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    # Store state and verifier together
    auth_states[state] = {
        "verifier": code_verifier,
        "timestamp": None  # Can add timestamp for expiry
    }
    
    # Build authorization URL with PKCE
    params = {
        "client_key": TIKTOK_CLIENT_KEY,
        "scope": "user.info.basic,video.list",  # Adjust scopes as needed
        "response_type": "code",
        "redirect_uri": TIKTOK_REDIRECT_URI,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    
    auth_url = f"{TIKTOK_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

@app.get("/auth/tiktok/callback")
async def tiktok_callback(code: str, state: str):
    """Handle TikTok OAuth callback with PKCE and redirect to search view"""
    # Verify state
    if state not in auth_states:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # Get code verifier
    state_data = auth_states[state]
    code_verifier = state_data["verifier"]
    
    # Remove used state
    del auth_states[state]
    
    # Exchange code for access token with PKCE
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            TIKTOK_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_key": TIKTOK_CLIENT_KEY,
                "client_secret": TIKTOK_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": TIKTOK_REDIRECT_URI,
                "code_verifier": code_verifier
            }
        )
        
        # Log the response for debugging
        print(f"TikTok token response status: {token_response.status_code}")
        print(f"TikTok token response body: {token_response.text}")
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=token_response.status_code,
                detail=f"Failed to get access token: {token_response.text}"
            )
        
        token_data = token_response.json()
        print(f"Token data structure: {token_data}")
        
        # TikTok returns access_token directly or in a data object
        access_token = token_data.get("access_token") or token_data.get("data", {}).get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=400, 
                detail=f"No access token received. Response: {token_data}"
            )
        
        # Get user info
        user_response = await client.get(
            TIKTOK_USER_INFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            params={"fields": "open_id,union_id,avatar_url,display_name"}
        )
        
        if user_response.status_code != 200:
            raise HTTPException(
                status_code=user_response.status_code,
                detail=f"Failed to get user info: {user_response.text}"
            )
        
        user_data = user_response.json()
        user_info = user_data.get("data", {}).get("user", {})
        
        # Store user in Supabase (optional)
        if supabase:
            try:
                supabase.table("tiktok_users").upsert({
                    "open_id": user_info.get("open_id"),
                    "display_name": user_info.get("display_name"),
                    "avatar_url": user_info.get("avatar_url"),
                    "access_token": access_token,  # In production, encrypt this!
                }).execute()
            except Exception as e:
                print(f"Error storing user: {e}")
        
        # Redirect to the search view with access token and user data
        frontend_url = os.getenv("FRONTEND_URL", "https://cookr.dev")
        user_json = quote(json.dumps(user_info))
        redirect_url = f"{frontend_url}/search?access_token={access_token}&user={user_json}"
        
        return RedirectResponse(url=redirect_url)

# Supabase connection
from supabase import create_client, Client

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

@app.get("/supabase-test")
async def supabase_test():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    # Example query
    data = supabase.table("recipes").select("*").execute()
    return {"data": data}

@app.get("/tiktok/search")
async def tiktok_search(query: str):
    """
    Search TikTok videos endpoint
    This is a placeholder - implement with TikTok Video Query API
    Reference: https://developers.tiktok.com/doc/content-query-api-get-videos/
    """
    # TODO: Implement actual TikTok Video Query API integration
    # For now, return a mock response
    return {
        "videos": [
            {
                "id": "example1",
                "title": f"Example cooking video for: {query}",
                "cover_image_url": "https://via.placeholder.com/300x400",
                "view_count": 150000,
                "like_count": 25000,
            },
            {
                "id": "example2",
                "title": f"How to cook {query} - Easy recipe",
                "cover_image_url": "https://via.placeholder.com/300x400",
                "view_count": 89000,
                "like_count": 12000,
            }
        ],
        "message": "This is a mock response. Implement TikTok Video Query API for real results."
    }

