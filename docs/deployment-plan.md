# Deployment Plan: Zomato AI Recommender on Streamlit

## Overview
This document outlines the steps to deploy the Zomato AI Restaurant Recommender application on Streamlit (both Streamlit Cloud and self-hosted options).

## Prerequisites

- Python 3.10+
- Git and GitHub account (for Streamlit Cloud)
- Groq API key (for LLM recommendations)
- Node.js 18+ (optional, for React frontend)

## Option 1: Streamlit Cloud Deployment (Recommended)

### Step 1: Prepare Repository
1. Push the project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Zomato AI Recommender"
   git remote add origin https://github.com/<YOUR_USERNAME>/zomato-ai-recommender.git
   git push -u origin main
   ```

2. Create `.streamlit/secrets.toml` for local testing (add to `.gitignore`):
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

### Step 2: Deploy on Streamlit Cloud
1. Visit [Streamlit Cloud](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub account and select the repository
4. Choose branch: `main`
5. Set app path: `app/streamlit_app.py`
6. Click "Deploy"

### Step 3: Configure Secrets in Streamlit Cloud
1. After deployment, go to app Settings (gear icon)
2. Select "Secrets"
3. Add your environment variables:
   ```
   GROQ_API_KEY = "your_groq_api_key"
   ```

## Option 2: Docker Deployment (Self-Hosted)

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download and cache data
RUN python -m data.loader --refresh

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  zomato-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./data/cache:/app/data/cache
    restart: unless-stopped
```

### Step 3: Build and Run
```bash
# Build image
docker build -t zomato-ai-recommender .

# Run container
docker run -e GROQ_API_KEY="your_key" -p 8501:8501 zomato-ai-recommender

# Or use docker-compose
docker-compose up -d
```

## Option 3: Traditional Server Deployment (VPS/EC2)

### Step 1: SSH into Server
```bash
ssh user@your_server_ip
```

### Step 2: Clone and Setup
```bash
git clone https://github.com/<YOUR_USERNAME>/zomato-ai-recommender.git
cd zomato-ai-recommender
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Download Data Cache
```bash
python -m data.loader --refresh
```

### Step 4: Configure Environment Variables
```bash
export GROQ_API_KEY="your_groq_api_key"
```

### Step 5: Run Streamlit with Systemd (Linux)

Create `/etc/systemd/system/zomato-app.service`:
```ini
[Unit]
Description=Zomato AI Recommender
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/zomato-ai-recommender
Environment="PATH=/home/ubuntu/zomato-ai-recommender/venv/bin"
Environment="GROQ_API_KEY=your_groq_api_key"
ExecStart=/home/ubuntu/zomato-ai-recommender/venv/bin/streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable zomato-app
sudo systemctl start zomato-app
```

### Step 6: Reverse Proxy with Nginx
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Configuration

### Streamlit Config File
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6334"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[client]
showErrorDetails = true

[server]
port = 8501
enableXsrfProtection = true
```

### Performance Tuning
```toml
[client]
toolbarMode = "minimal"

[logger]
level = "warning"

[server]
maxUploadSize = 200
enableCORS = true
```

## Data Management

### Pre-load Cache
Before deployment, ensure the data cache is built:
```bash
python -m data.loader --refresh
```

This creates:
- `data/cache/restaurants.parquet` (~51k restaurants)
- `data/cache/cache_metadata.json` (stats and thresholds)

### Cache Location
- Local: `data/cache/`
- Docker: Mount as volume to persist across restarts
- Cloud: Auto-downloads on first run (slower startup)

## Monitoring and Logging

### View Logs
```bash
# Systemd
sudo journalctl -u zomato-app -f

# Docker
docker logs -f container_id

# Streamlit Cloud
View in app Settings → Logs
```

### Health Checks
```bash
curl http://localhost:8501
```

## Scaling Considerations

- **Single Instance**: Suitable for < 100 concurrent users
- **Load Balancer**: Use Nginx/HAProxy for multiple instances
- **Database Caching**: Cache recommendations in Redis for frequent queries
- **CDN**: Serve static assets via CloudFront or Netlify

## Frontend Integration

If deploying the React frontend (`frontend/`):

1. Build React app:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. Serve static files from a CDN or separate server
3. Configure API proxy to Streamlit backend at `/api`
4. Deploy frontend to Vercel, Netlify, or AWS S3 + CloudFront

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Groq API key not found | Set `GROQ_API_KEY` in environment or `.streamlit/secrets.toml` |
| Cache file missing | Run `python -m data.loader --refresh` |
| Slow recommendations | Increase `top_n_recommendations` in settings, check LLM timeout |
| High memory usage | Reduce `max_candidates` in config settings |

## Rollback Plan

1. Keep previous deployment version in git: `git tag v1.0.0`
2. Revert to previous version: `git checkout v1.0.0`
3. Re-deploy or restart service
4. For Streamlit Cloud: Select branch/commit in Settings

## Security Checklist

- [ ] Groq API key stored in secrets, not code
- [ ] Nginx/reverse proxy enabled
- [ ] SSL/TLS certificate installed
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Data cache secured (read-only for app process)

## Post-Deployment Verification

1. Run demo scenarios:
   ```bash
   python scripts/demo_scenarios.py
   ```

2. Test CLI:
   ```bash
   python -m app.main recommend --location Bangalore --budget low
   ```

3. Verify Streamlit UI loads at `https://your_domain.com`

4. Test end-to-end: Submit preferences → receive recommendations

## Support and Monitoring

- **Monitoring**: Set up alerts for failed LLM requests (logs)
- **Updates**: Regularly run `python -m data.loader --refresh` (weekly/monthly)
- **Maintenance**: Monitor Groq API usage and billing
