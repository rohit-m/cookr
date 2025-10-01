# Version Control Guide

## ✅ Files INCLUDED in Git (Should be committed)

### Configuration Files
- `.gitignore` - Git ignore rules
- `.dockerignore` - Docker ignore rules (frontend & backend)
- `supabase.env.example` - Example environment variables template
- `docker-compose.yml` - Docker orchestration config
- `nginx.conf` - Nginx reverse proxy config
- `vite.config.js` - Vite configuration
- `package.json` - Node.js dependencies
- `package-lock.json` - Locked dependency versions

### Source Code
- `src/` - Vue3 frontend source code
- `backend/` - FastAPI backend source code
- `index.html` - Frontend entry point
- `Dockerfile` - Frontend Docker config
- `backend/Dockerfile` - Backend Docker config
- `backend/requirements.txt` - Python dependencies

### Scripts
- `generate-ssl.sh` - SSL certificate generation script
- `setup-domain.sh` - Domain setup helper script
- `Makefile` - Build/run commands

### Documentation
- `README.md` - Main documentation
- `SETUP_INSTRUCTIONS.md` - Setup guide
- Any other .md files you create

## ❌ Files EXCLUDED from Git (In .gitignore)

### Secret/Sensitive Files
- `supabase.env` - **Contains actual credentials** (never commit!)
- `.env` - Any environment files with secrets
- `.env.local`, `.env.*.local` - Local environment overrides

### SSL Certificates (Local Development)
- `ssl/` - Entire SSL directory
- `*.key` - Private keys
- `*.crt` - Certificates
- `*.pem` - PEM files

### Dependencies (Can be reinstalled)
- `node_modules/` - Node.js packages (run `npm install`)
- `venv/`, `env/`, `.venv/` - Python virtual environments

### Build Artifacts
- `dist/` - Frontend build output
- `build/` - Build directories
- `*.egg-info/` - Python package info

### Cache & Logs
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files
- `*.log` - Log files
- `.coverage` - Test coverage data
- `.pytest_cache/` - Pytest cache

### IDE & OS Files
- `.vscode/`, `.idea/` - IDE settings
- `.DS_Store` - macOS metadata
- `Thumbs.db` - Windows thumbnails
- `*.swp`, `*.swo` - Vim swap files

## 🔄 One-Time Setup Files

These files are generated once locally and not tracked:

1. **SSL Certificates** (`ssl/`)
   - Generated with: `./generate-ssl.sh`
   - Self-signed for local development
   - Each developer generates their own

2. **Environment Variables** (`supabase.env`)
   - Copy from: `supabase.env.example`
   - Fill in actual values
   - Never commit the real values!

## 📝 When Setting Up a New Clone

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd cookr

# 2. Install frontend dependencies
npm install

# 3. Generate SSL certificates
chmod +x generate-ssl.sh
./generate-ssl.sh

# 4. Setup environment variables
cp supabase.env.example supabase.env
# Edit supabase.env with your actual credentials

# 5. Add domains to hosts file
chmod +x setup-domain.sh
./setup-domain.sh
# Then manually add to /etc/hosts:
# 127.0.0.1  cookr.dev
# 127.0.0.1  api.cookr.dev

# 6. Start the application
docker-compose up --build
```

## 🛡️ Security Reminders

- ✅ **ALWAYS** check before committing sensitive files
- ✅ Use `git status` to review what will be committed
- ✅ Keep `supabase.env` in `.gitignore`
- ✅ Use `supabase.env.example` as a template (no real values)
- ❌ **NEVER** commit API keys, passwords, or certificates
- ❌ **NEVER** remove `supabase.env` from `.gitignore`

## 🔍 Check What Will Be Committed

Before committing, verify:

```bash
# See what files are tracked
git status

# See what would be committed
git add -A --dry-run

# Check if sensitive files are ignored
git check-ignore -v supabase.env ssl/
```

Expected output:
```
.gitignore:4:supabase.env    supabase.env
.gitignore:8:ssl/            ssl/
```

If these files show up in `git status`, **DO NOT COMMIT** - fix your `.gitignore` first!

