# ArtiSANs MVP Deployment Guide

## Overview
Deploy ArtiSANs MVP (Nigeria-based artisan marketplace) for the Lagos beta launch.

## Architecture
- **Frontend**: Next.js 14 → **Cloudflare Pages**
- **Backend**: Django 4.2 + DRF → **Render**
- **Database**: SQLite (MVP, zero cost)

---

## Frontend Deployment (Cloudflare Pages)

### Prerequisites:
- Cloudflare account (free tier available)
- `@cloudflare/next-on-pages` for Next.js compatibility

### Steps:

1. **Install Cloudflare Pages adapter:**
```bash
cd frontend
npm install -D @cloudflare/next-on-pages
```

2. **Update package.json scripts:**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "npx @cloudflare/next-on-pages",
    "deploy": "wrangler pages deploy .vercel/output/static"
  }
}
```

3. **Push code to GitHub**

4. **Deploy via Cloudflare Dashboard:**
   - Go to [pages.cloudflare.com](https://pages.cloudflare.com)
   - Click "Create a project" → "Connect to Git"
   - Select your repo
   - Set configuration:
     - **Framework**: Next.js (Static/Hybrid)
     - **Build command**: `npm run build`
     - **Build output directory**: `.vercel/output/static`
   - Add environment variables:
     - `NEXT_PUBLIC_API_URL`: Your Render backend URL
     - `NODE_VERSION`: `18`

5. **Alternative: Deploy via Wrangler CLI:**
```bash
cd frontend
npm install -g wrangler
wrangler login
npm run build
wrangler pages deploy .vercel/output/static --project-name=artisans-frontend
```

### Note:
Cloudflare Pages has some limitations with Next.js SSR features. If you need full SSR support, consider Vercel instead.

---

## Backend Deployment (Render)

### Steps:

1. **Push code to GitHub** (already prepared with `render.yaml`)

2. **Deploy via Render Dashboard:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml`
   - Set root directory: `backend`
   - Click "Create Web Service"

3. **Environment Variables** (auto-set by render.yaml, but verify):
   - `SECRET_KEY`: Auto-generated (or set manually)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render domain
   - `CORS_ALLOWED_ORIGINS`: Your Cloudflare Pages domain
   - `DATABASE_ENGINE`: `django.db.backends.sqlite3`
   - `JWT_SECRET_KEY`: Auto-generated

4. **Post-Deploy:**
   Render automatically runs:
   ```bash
   pip install -r requirements.txt
   python Artisans/manage.py migrate
   python Artisans/manage.py collectstatic --noinput
   gunicorn Artisans.wsgi:application
   ```

---

## Database Strategy (SQLite for MVP)

### Pros:
- Zero cost
- No setup required
- Sufficient for ~50 Lagos beta users

### Cons:
- File-based (needs backup strategy)
- Limited write concurrency

### Backup Strategy:
```bash
# On Render, use shell access or add to build command:
cp Artisans/db.sqlite3 Artisans/db.sqlite3.backup-$(date +%Y%m%d)
```

### Future Upgrade to PostgreSQL:
When scaling beyond MVP, uncomment `psycopg2-binary` in requirements.txt and update settings.

---

## Pre-Launch Checklist

### Backend (Render):
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` is secure
- [ ] `ALLOWED_HOSTS` includes Render domain
- [ ] `CORS_ALLOWED_ORIGINS` includes Cloudflare Pages domain
- [ ] Migrations applied
- [ ] Static files collected
- [ ] Paystack/Flutterwave configured (test mode for beta)

### Frontend (Cloudflare):
- [ ] `NEXT_PUBLIC_API_URL` points to Render backend
- [ ] Build succeeds
- [ ] All pages render correctly
- [ ] Authentication works
- [ ] Job posting/bidding/reviews work

### Testing (Lagos Beta):
- [ ] Register as artisan (test Lagos address)
- [ ] Register as client
- [ ] Post a job
- [ ] Place a bid
- [ ] Accept bid & complete job
- [ ] Leave review
- [ ] Test payment flow (small amount)

---

## Monitoring

### Cloudflare Pages:
- Built-in analytics
- Real-time logs via dashboard

### Render:
- Built-in logs and metrics
- Email alerts for downtime

---

## Cost Estimate (Lagos Beta - 50 Users)

| Service | Cost |
|---------|------|
| Cloudflare Pages | $0 (Free tier) |
| Render (Web Service) | $0-7/month (Starter plan) |
| SQLite Database | $0 |
| Paystack | 1.5% + ₦100/transaction |

**Total: ~$7/month or less**

---

## Quick Deploy Commands

### Backend to Render:
```bash
cd backend
git add .
git commit -m "Prepare backend for Render deployment"
git push origin main
# Then deploy via Render dashboard
```

### Frontend to Cloudflare:
```bash
cd frontend
npm install -D @cloudflare/next-on-pages
npm run build
wrangler pages deploy .vercel/output/static --project-name=artisans-frontend
```

---

## Resources
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Render Docs](https://render.com/docs)
- [Next.js on Cloudflare](https://developers.cloudflare.com/pages/framework-guides/deploy-a-nextjs-site/)
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
