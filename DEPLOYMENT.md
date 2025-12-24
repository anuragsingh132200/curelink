# Deployment Guide for Disha AI Health Coach

## Quick Start with Docker Compose

The fastest way to get the application running:

```bash
# 1. Clone and navigate to project
cd curelink

# 2. Set your API key in .env
# Edit .env and add your GEMINI_API_KEY or OPENAI_API_KEY

# 3. Start everything
docker-compose up --build

# 4. Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Production Deployment

### Option 1: Render.com (Free Tier Available)

#### Step 1: Prepare Your Repository
Push your code to GitHub.

#### Step 2: Deploy Backend

1. Go to [render.com](https://render.com) and create account
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `disha-backend`
   - **Environment**: `Python`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. Add Environment Variables:
   ```
   GEMINI_API_KEY=your_key_here
   LLM_PROVIDER=gemini
   LLM_MODEL=gemini-2.0-flash-exp
   DATABASE_URL=<from PostgreSQL addon>
   REDIS_URL=<from Redis addon>
   ENVIRONMENT=production
   ```

6. Click "Create Web Service"

#### Step 3: Add Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it `disha-db`
3. Copy the "Internal Database URL"
4. Add it to backend environment variables as `DATABASE_URL`

#### Step 4: Add Redis

1. Click "New +" → "Redis"
2. Name it `disha-redis`
3. Copy the "Internal Redis URL"
4. Add it to backend environment variables as `REDIS_URL`

#### Step 5: Deploy Frontend

1. Click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name**: `disha-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`

4. Add Environment Variables:
   ```
   REACT_APP_API_URL=<your-backend-url>
   REACT_APP_WS_URL=<your-backend-ws-url>
   ```
   Example: `https://disha-backend.onrender.com`

5. Click "Create Static Site"

### Option 2: Railway.app

#### Backend + Database

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Add PostgreSQL database (automatically adds DATABASE_URL)
5. Add Redis database (automatically adds REDIS_URL)
6. Configure environment variables
7. Railway auto-detects Python and deploys

#### Frontend on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set:
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. Add environment variables:
   ```
   REACT_APP_API_URL=<railway-backend-url>
   REACT_APP_WS_URL=<railway-backend-ws-url>
   ```

### Option 3: AWS (Production)

#### Using ECS + RDS + ElastiCache

1. **Create RDS PostgreSQL Instance**
   ```bash
   aws rds create-db-instance \
     --db-instance-identifier disha-db \
     --db-instance-class db.t3.micro \
     --engine postgres \
     --master-username admin \
     --master-user-password <password> \
     --allocated-storage 20
   ```

2. **Create ElastiCache Redis**
   ```bash
   aws elasticache create-cache-cluster \
     --cache-cluster-id disha-redis \
     --engine redis \
     --cache-node-type cache.t3.micro \
     --num-cache-nodes 1
   ```

3. **Build and Push Docker Images**
   ```bash
   # Backend
   cd backend
   docker build -t disha-backend .
   docker tag disha-backend:latest <ecr-repo-url>/disha-backend:latest
   docker push <ecr-repo-url>/disha-backend:latest

   # Frontend
   cd ../frontend
   docker build -t disha-frontend .
   docker tag disha-frontend:latest <ecr-repo-url>/disha-frontend:latest
   docker push <ecr-repo-url>/disha-frontend:latest
   ```

4. **Create ECS Task Definitions and Services**
   - Use AWS Console or CloudFormation
   - Configure task definitions with environment variables
   - Set up Application Load Balancer
   - Configure Auto Scaling

5. **Deploy Frontend to S3 + CloudFront**
   ```bash
   cd frontend
   npm run build
   aws s3 sync build/ s3://disha-frontend/
   # Configure CloudFront distribution
   ```

## Environment Configuration

### Development
```env
ENVIRONMENT=development
DATABASE_URL=postgresql://curelink:curelink_password@localhost:5432/curelink_db
REDIS_URL=redis://localhost:6379
```

### Production
```env
ENVIRONMENT=production
DATABASE_URL=<production-database-url>
REDIS_URL=<production-redis-url>
SECRET_KEY=<strong-random-secret-key>
```

## Health Checks

The application provides health check endpoints:

- **Backend**: `GET /health` → `{"status": "healthy"}`
- **API Docs**: `/docs` (Swagger UI)

## Monitoring

### Logs

**Render.com**: View logs in the dashboard
**Railway**: Click on service → Logs tab
**AWS**: CloudWatch Logs

### Metrics to Monitor

- API response times
- Database connection pool
- Redis connection status
- LLM API latency
- WebSocket connections
- Error rates

## Troubleshooting

### Database Connection Issues

1. Check DATABASE_URL format:
   ```
   postgresql://user:password@host:port/database
   ```

2. Verify database is running:
   ```bash
   pg_isready -h <host> -p <port>
   ```

3. Check migrations:
   ```bash
   alembic current
   alembic upgrade head
   ```

### WebSocket Connection Fails

1. Verify WS URL format:
   - Development: `ws://localhost:8000`
   - Production: `wss://your-domain.com` (use WSS for HTTPS)

2. Check CORS settings in backend

3. Verify load balancer WebSocket support (if using one)

### LLM API Issues

1. Verify API key is set correctly
2. Check API key has sufficient credits
3. Monitor rate limits
4. Check error logs for specific API errors

### Frontend Not Loading

1. Check build output:
   ```bash
   cd frontend
   npm run build
   ```

2. Verify environment variables are set

3. Check browser console for errors

4. Verify API URL is accessible from browser

## SSL/HTTPS

### Render.com
- Automatic SSL certificates
- HTTPS enabled by default

### Vercel
- Automatic SSL certificates
- Custom domains supported

### AWS
- Use AWS Certificate Manager
- Configure CloudFront with SSL
- Add certificate to Load Balancer

## Scaling Considerations

### Database
- Connection pooling (already configured)
- Read replicas for heavy read workloads
- Increase instance size as needed

### Backend
- Horizontal scaling with multiple instances
- Load balancer distributes traffic
- Stateless design allows easy scaling

### Redis
- Increase memory as needed
- Consider Redis Cluster for high availability

### Frontend
- CDN distribution (CloudFront, Vercel Edge)
- Static assets cached at edge locations
- Gzip compression enabled

## Backup and Recovery

### Database Backups

**Automatic** (Render/Railway):
- Daily automated backups
- Point-in-time recovery

**Manual**:
```bash
pg_dump -h <host> -U <user> -d <database> > backup.sql
```

**Restore**:
```bash
psql -h <host> -U <user> -d <database> < backup.sql
```

### Redis Persistence

Configure Redis persistence in production:
```
# redis.conf
save 900 1
save 300 10
save 60 10000
```

## Security Best Practices

1. **Never commit secrets**:
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use strong SECRET_KEY**:
   ```python
   import secrets
   secrets.token_urlsafe(32)
   ```

3. **Enable HTTPS**:
   - Use SSL certificates
   - Redirect HTTP to HTTPS

4. **Database security**:
   - Use strong passwords
   - Limit access by IP
   - Enable SSL connections

5. **API rate limiting**:
   - Implement rate limiting
   - Monitor for abuse

6. **CORS configuration**:
   - Set specific allowed origins in production
   - Don't use `allow_origins=["*"]`

## Cost Optimization

### Free Tier Options
- **Render.com**: Free web services (with limitations)
- **Railway**: $5 free credit monthly
- **Vercel**: Free for personal projects
- **Netlify**: Free tier available

### Tips
1. Use free tiers for demo/development
2. Monitor usage to avoid overages
3. Set up billing alerts
4. Scale down during low traffic
5. Use spot instances (AWS)
6. Optimize database queries
7. Implement caching aggressively

## Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger Render Deploy
        run: |
          curl https://api.render.com/deploy/srv-xxx
```

### Render Auto-Deploy
- Enabled by default
- Deploys on every push to main branch
- Can disable for manual deploys

## Support

For deployment issues:
- Check service status pages
- Review documentation
- Contact platform support
- Check community forums

---

Good luck with your deployment! 🚀
