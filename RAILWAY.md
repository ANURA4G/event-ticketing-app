# Railway Deployment Guide

## Files Created for Railway

- ✅ `Procfile` - Tells Railway how to start the app
- ✅ `railway.toml` - Railway-specific configuration
- ✅ `requirements.txt` - Python dependencies (includes gunicorn)
- ✅ `.python-version` - Specifies Python 3.11
- ✅ `.gitignore` - Excludes unnecessary files from git

## Quick Deploy to Railway

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Ready for Railway deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Use the `Procfile` to start gunicorn
   - Assign a public URL

### Step 3: Access Your App

- Railway will provide a URL like: `https://your-app.railway.app`
- Login with: `adminmkce` / `hackfest-2k26`

## Configuration Details

### Procfile
```
web: cd app && gunicorn app:app
```

### railway.toml
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "cd app && gunicorn app:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## Important Notes

### Storage
- **JSON Files**: Work perfectly for ~75 teams
- **Ephemeral**: Files persist during runtime but may reset on redeployment
- **For Production**: Consider Railway's PostgreSQL addon for permanent storage

### Environment Variables
- No environment variables required for basic deployment
- Railway automatically provides `PORT` variable

### Domain
- Free `.railway.app` subdomain included
- Can add custom domain in Railway dashboard

## Admin Credentials

- **Username**: `adminmkce`
- **Password**: `hackfest-2k26`

## Features Included

- ✅ Admin-only authentication
- ✅ On-demand PDF/QR generation (no file storage)
- ✅ Team code (HF26XXXXX) for manual entry backup
- ✅ Mobile camera flip for QR scanning
- ✅ College name and team leader email fields
- ✅ Team size: 2-4 members
- ✅ Supports 75+ teams with JSON storage

## Troubleshooting

### If deployment fails:
1. Check Railway build logs
2. Verify all files are committed to git
3. Ensure `requirements.txt` is in root directory
4. Check that `app/app.py` exists

### If app doesn't start:
1. Check Railway deployment logs
2. Verify gunicorn is in `requirements.txt`
3. Ensure `Procfile` has correct path

## Monitoring

- View logs in Railway dashboard
- Monitor memory and CPU usage
- Set up alerts for downtime

## Scaling

Railway automatically handles:
- Load balancing
- Auto-scaling based on traffic
- Zero-downtime deployments

