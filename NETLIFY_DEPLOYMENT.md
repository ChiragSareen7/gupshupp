# Netlify Deployment Guide

## Prerequisites

1. GitHub account
2. Netlify account (sign up at https://netlify.com)
3. Groq API key

## Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Ensure `.env` is in `.gitignore`** (already done)
   - Your API key should NOT be committed to Git

2. **Build the frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```
   This creates the `frontend/build` directory

3. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### Step 2: Create Netlify Configuration

Create `netlify.toml` in the root directory:

```toml
[build]
  command = "cd frontend && npm install && npm run build"
  functions = "netlify/functions"
  publish = "frontend/build"

[build.environment]
  NODE_VERSION = "18"
  PYTHON_VERSION = "3.11"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Step 3: Deploy on Netlify

1. **Go to Netlify Dashboard**
   - Visit https://app.netlify.com
   - Sign in or create account

2. **Add New Site**
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub" and authorize Netlify

3. **Select Repository**
   - Choose your repository from the list
   - Click "Connect"

4. **Configure Build Settings**
   - **Build command:** `cd frontend && npm install && npm run build`
   - **Publish directory:** `frontend/build`
   - **Functions directory:** `netlify/functions`

5. **Set Environment Variables**
   - Click "Show advanced" → "New variable"
   - Add variable:
     - **Key:** `GROQ_API_KEY`
     - **Value:** Your Groq API key
   - Click "Deploy site"

### Step 4: Wait for Deployment

- Netlify will:
  1. Install Node.js dependencies
  2. Build the React app
  3. Deploy Python functions
  4. Set up environment variables

- This takes 2-5 minutes

### Step 5: Verify Deployment

1. **Check Build Logs**
   - Go to "Deploys" tab
   - Click on the latest deploy
   - Check for any errors

2. **Test Your Site**
   - Visit your Netlify URL (e.g., `https://your-site.netlify.app`)
   - Test the chat interface
   - Test memory extraction
   - Test personality comparison

## Troubleshooting

### Build Fails

**Error: "Python version not found"**
- Ensure `runtime.txt` specifies Python version: `python-3.11`
- Or set `PYTHON_VERSION = "3.11"` in `netlify.toml`

**Error: "Module not found"**
- Check `requirements.txt` includes all dependencies
- Verify Python functions are in `netlify/functions/`

### Functions Not Working

**Error: "GROQ_API_KEY not set"**
- Go to Site Settings → Environment Variables
- Add `GROQ_API_KEY` with your API key
- Redeploy the site

**Error: "Function not found"**
- Check `netlify.toml` has `functions = "netlify/functions"`
- Verify function files have `.py` extension
- Ensure each function has a `handler` function

### Frontend Not Loading

**Error: "404 Not Found"**
- Check `publish` directory is `frontend/build`
- Verify build completed successfully
- Check redirects are configured in `netlify.toml`

## Environment Variables

Required environment variable:
- `GROQ_API_KEY`: Your Groq API key

Set in Netlify:
1. Site Settings → Environment Variables
2. Add variable
3. Redeploy

## Post-Deployment

### Update Frontend API URL

The frontend needs to know the Netlify URL. Update `frontend/src/App.js`:

```javascript
const API_BASE = process.env.REACT_APP_API_URL || '';
```

Then set `REACT_APP_API_URL` in Netlify environment variables to your Netlify site URL, or leave empty to use relative URLs (works when frontend and backend are on same domain).

### Custom Domain (Optional)

1. Go to Site Settings → Domain management
2. Add custom domain
3. Follow DNS configuration instructions

## Monitoring

- **Function Logs:** Functions → Select function → View logs
- **Build Logs:** Deploys → Select deploy → View logs
- **Analytics:** Site overview shows traffic and performance

## Updating Your Site

After making changes:

1. Push to GitHub
2. Netlify automatically detects changes
3. Triggers new build
4. Deploys automatically

Or manually trigger:
- Go to Deploys tab
- Click "Trigger deploy" → "Deploy site"

## Important Notes

- **Never commit `.env` file** - API keys should only be in Netlify environment variables
- **Function timeout:** Netlify Functions have a 10-second timeout (26 seconds for Pro)
- **Build time:** First build takes longer, subsequent builds are faster
- **Cold starts:** Functions may have cold start delays on first invocation

## Support

- Netlify Docs: https://docs.netlify.com
- Function Docs: https://docs.netlify.com/functions/overview/
- Python Functions: https://docs.netlify.com/functions/language-support/python/

