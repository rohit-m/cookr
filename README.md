## Need a non-localhost url for Tiktok to allow redirect back from oAuth
1. **Generate SSL certificates (one-time setup):**
   ```bash
   chmod +x generate-ssl.sh
   ./generate-ssl.sh
   ```

2. **Setup local domain (one-time setup):**
   ```bash
   chmod +x setup-domain.sh
   ./setup-domain.sh
   ```
   
   Then manually add to `/etc/hosts`:
   ```
   127.0.0.1       cookr.dev
   127.0.0.1       api.cookr.dev
   ```

3. **Start the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the app:**
   - Frontend: https://cookr.dev
   - Backend API: https://api.cookr.dev
   - API Docs: https://api.cookr.dev/docs