# Deployment Plan: Zomato AI Recommender on Render + Vercel

## Overview
This document outlines the deployment steps for the Zomato AI Restaurant Recommender application with:
- Backend on Render
- Frontend on Vercel

## Prerequisites

- Python 3.10+
- Git and GitHub account
- Groq API key (for LLM recommendations)
- Node.js 18+ (for React frontend)
- Render account
- Vercel account

## Backend Deployment: Render

### Step 1: Prepare Repository
1. Push the project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Zomato AI Recommender"
   git remote add origin https://github.com/<YOUR_USERNAME>/zomato-ai-recommender.git
   git push -u origin main
   ```

2. Ensure the backend entry point is correct in `app/streamlit_app.py` or `app/main.py`.

3. Add any local secret files to `.gitignore`.

### Step 2: Configure Render Service
1. In Render, create a new Web Service.
2. Connect your GitHub repository.
3. Set the branch to `main`.
4. Configure the service:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.api:app --host 0.0.0.0 --port $PORT`

5. Add environment variables under Render service settings:
   - `GROQ_API_KEY` = `your_groq_api_key`
   - `STREAMLIT_SERVER_PORT` = `{{PORT}}` (optional: Render provides `$PORT` automatically)

### Step 3: Use Render Secrets
1. In Render, open the service dashboard.
2. Add the following Environment Variables:
   ```text
   GROQ_API_KEY=your_groq_api_key
   ```
3. If needed, add additional values for configuration.

### Step 4: Deploy and Validate
1. Trigger deployment in Render.
2. Wait for render logs to finish.
3. Visit the assigned Render URL to ensure the API responds successfully.
4. Validate that recommendations work and no API key errors appear.

### Render Notes
- Render provides the `$PORT` environment variable for HTTP services.
- For a backend API, the service must bind to `0.0.0.0`.
- Use `render.yaml` if you want an Infrastructure as Code deployment manifest.

## Frontend Deployment: Vercel

### Step 1: Prepare Frontend
1. Ensure `frontend/package.json` and `frontend/vite.config.ts` are up to date.
2. Confirm any API base URL configuration points to the Render backend.
3. If using environment-based API endpoints, add a `.env.production` or Vercel environment variables.

### Step 2: Create Vercel Project
1. In Vercel, click "New Project".
2. Import your GitHub repository.
3. Select the `frontend` directory as the root.
4. Configure the framework preset to `Vite` or `React`.
5. Set the build command:
   ```bash
   npm install
   npm run build
   ```
6. Set the output directory to:
   ```text
   dist
   ```

### Step 3: Configure Vercel Environment Variables
1. In Vercel Project Settings, add the backend API URL:
   - `VITE_API_BASE_URL` = `https://<your-render-service>.onrender.com`
2. Add any other frontend-specific values.

### Step 4: Deploy and Verify
1. Deploy the Vercel project.
2. Open the Vercel preview URL.
3. Verify the frontend loads and fetches recommendations from the Render backend.
4. Test the app end-to-end by submitting preferences and receiving results.

## Recommended Setup

### Backend on Render
- Service type: Web Service
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
- Environment variables: `GROQ_API_KEY`

### Frontend on Vercel
- Root directory: `frontend`
- Build command: `npm install && npm run build`
- Output directory: `dist`
- Env var: `VITE_API_BASE_URL`

## Configuration

### Streamlit Config File
Create `.streamlit/config.toml` for local testing:
```toml
[theme]
primaryColor = "#FF6334"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[client]
showErrorDetails = true

[server]
enableXsrfProtection = true
```

### Local Secrets
For local development, use `.env` or `.streamlit/secrets.toml` and add it to `.gitignore`:
```toml
GROQ_API_KEY = "your_groq_api_key"
``` 

## Data Management

### Pre-load Cache
Before deployment, ensure the data cache is built:
```bash
python -m data.loader --refresh
```

This creates:
- `data/cache/restaurants.parquet`
- `data/cache/cache_metadata.json`

### Cache Location
- Local: `data/cache/`
- Render: data should be built or refreshed during deploy, but cache persistence is not guaranteed between deploys
- Use a persistent storage solution or re-run `python -m data.loader --refresh` as needed

## Monitoring and Logging

### View Logs
```bash
# Render
View logs from the Render dashboard

# Vercel
View build and runtime logs from the Vercel dashboard
```

### Health Checks
```bash
curl https://<your-render-service>.onrender.com
```

## Scaling Considerations

- **Render**: auto scales with the selected plan
- **Vercel**: CDN-backed frontend for fast global delivery
- **Backend caching**: use Redis or persistent storage if API response latency is a concern

## Frontend Integration Notes

- Set `VITE_API_BASE_URL` to the Render backend URL in Vercel.
- Use relative paths in the React app only if the frontend and backend are proxied together.
- Confirm CORS is handled by the backend if the frontend and backend domains differ.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Groq API key not found | Set `GROQ_API_KEY` in Render environment variables |
| Backend URL incorrect | Update `VITE_API_BASE_URL` in Vercel env vars |
| Build fails | Check `frontend/package.json` and Vite config for missing paths |
| Cache file missing | Run `python -m data.loader --refresh` locally or regenerate during deployment |

## Rollback Plan

1. Keep previous commit or branch in git: `git tag v1.0.0`
2. Revert to the prior version: `git checkout v1.0.0`
3. Redeploy on Render and Vercel

## Security Checklist

- [ ] Groq API key stored in Render environment variables, not code
- [ ] Frontend secrets stored in Vercel environment variables
- [ ] SSL/TLS enabled on Render and Vercel endpoints
- [ ] CORS properly configured for cross-origin requests

## Post-Deployment Verification

1. Run demo scenarios:
   ```bash
   python scripts/demo_scenarios.py
   ```
2. Test the backend locally:
   ```bash
   python -m app.main recommend --location Bangalore --budget low
   ```
3. Verify frontend loads at the Vercel URL.
4. Confirm end-to-end: submit preferences → receive recommendations.

## Support and Monitoring

- Monitor Render logs for backend errors
- Monitor Vercel logs for frontend build and runtime issues
- Refresh the data cache periodically if input data changes


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
