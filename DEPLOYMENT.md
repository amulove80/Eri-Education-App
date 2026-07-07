# Deployment Guide

This guide covers deploying the Kalshi Trading Platform to various hosting platforms.

## 🚀 Quick Deploy Options

### Vercel (Recommended)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy to Vercel**
- Visit [vercel.com](https://vercel.com)
- Import your GitHub repository
- Add environment variables in Vercel dashboard
- Deploy

3. **Environment Variables**
Add these in Vercel dashboard:
```
KALSHI_EMAIL=your_email
KALSHI_PASSWORD=your_password
```

### Netlify

1. **Build Settings**
- Build command: `npm run build`
- Publish directory: `.next`

2. **Deploy**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

2. **Build and Run**
```bash
docker build -t kalshi-trading-platform .
docker run -p 3000:3000 \
  -e KALSHI_EMAIL=your_email \
  -e KALSHI_PASSWORD=your_password \
  kalshi-trading-platform
```

### Self-Hosted (VPS)

1. **Requirements**
- Ubuntu 20.04+ or similar
- Node.js 18+
- Nginx (optional)
- SSL certificate (recommended)

2. **Setup**
```bash
# Clone repository
git clone <your-repo-url>
cd kalshi-trading-platform

# Install dependencies
npm install

# Build production
npm run build

# Set environment variables
cp .env.example .env.local
nano .env.local

# Run with PM2
npm install -g pm2
pm2 start npm --name kalshi-platform -- start
pm2 save
pm2 startup
```

3. **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 🔒 Security Considerations

### Environment Variables
- Never commit `.env.local` to git
- Use secure secret management
- Rotate credentials regularly

### HTTPS
- Always use HTTPS in production
- Use Let's Encrypt for free SSL
- Enable HSTS headers

### API Security
- Store credentials encrypted
- Use secure session management
- Implement rate limiting

## 📊 Monitoring

### Health Checks
Add a health endpoint for monitoring:

```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString() 
  });
}
```

### Logging
- Use structured logging
- Monitor error rates
- Track API response times

### Alerts
Set up alerts for:
- API failures
- High risk scores
- Daily loss limits exceeded
- System errors

## 🔄 Updates

### Continuous Deployment
```bash
# Pull latest changes
git pull origin main

# Install dependencies
npm install

# Rebuild
npm run build

# Restart
pm2 restart kalshi-platform
```

### Rollback
```bash
# Revert to previous version
git checkout <previous-commit-hash>
npm install
npm run build
pm2 restart kalshi-platform
```

## 🎯 Performance Optimization

### Caching
- Enable Next.js caching
- Cache market data (with short TTL)
- Use CDN for static assets

### Database (Optional)
For production, consider adding a database:
- PostgreSQL for trade history
- Redis for caching
- Time-series DB for metrics

## 📈 Scaling

### Horizontal Scaling
- Use load balancer
- Multiple app instances
- Shared session storage

### Vertical Scaling
- Increase server resources
- Optimize queries
- Enable compression

## 🧪 Testing Production

Before going live:
1. Test with small amounts
2. Verify all API connections
3. Check risk limits work
4. Monitor first trades closely
5. Have rollback plan ready

## 📞 Production Checklist

- [ ] Environment variables configured
- [ ] HTTPS enabled
- [ ] API credentials valid
- [ ] Risk limits configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Documentation updated
- [ ] Team trained
- [ ] Tested with real data
- [ ] Rollback plan ready

## ⚠️ Important Notes

- **Start Small**: Begin with minimal capital
- **Monitor Closely**: Watch first trades carefully
- **Have Backup**: Keep backup of configurations
- **Stay Updated**: Keep dependencies updated
- **Security First**: Never expose credentials

---

Good luck with your deployment! Remember to trade responsibly.
