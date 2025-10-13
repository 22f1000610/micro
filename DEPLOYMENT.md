# GitHub Pages Deployment Guide

## Quick Deployment Steps

### Method 1: GitHub Web Interface (Easiest)
1. Create a new repository on GitHub (or use existing)
2. Upload these files:
   - `index.html`
   - `subtopics.json`
3. Go to repository Settings → Pages
4. Select branch (main/master) and root folder
5. Click Save
6. Your site will be live at: `https://username.github.io/repo-name/`

### Method 2: Git Command Line
```bash
# Initialize git (if not already)
git init

# Add files
git add index.html subtopics.json README.md

# Commit
git commit -m "Deploy microeconomics notes"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/username/repo-name.git

# Push to GitHub
git push -u origin main

# Enable GitHub Pages in repository settings
```

## Files Required for Deployment
- ✅ `index.html` (17KB) - Main application
- ✅ `subtopics.json` (4MB) - Content data

## Optional Files
- `README.md` - Documentation
- `DEPLOYMENT.md` - This file
- `.gitignore` - To exclude backup files

### Sample .gitignore
```
index_old.html
index_chapter_version.html
chapters.json
parse_*.py
*.log
__pycache__/
```

## Testing Locally Before Deployment

### Using Python HTTP Server
```bash
# Start server
python3 -m http.server 8080

# Open in browser
# http://localhost:8080/index.html
```

### Using Node.js (if installed)
```bash
# Install simple server
npm install -g http-server

# Start server
http-server -p 8080

# Open http://localhost:8080
```

## Performance Expectations

### After Deployment
- **First Load**: ~4.1MB (index.html + subtopics.json)
- **Subsequent Visits**: Cached (instant load)
- **Content Load**: ~50KB per subtopic switch
- **Images**: Loaded on-demand via lazy loading

### Optimization Tips
1. **Enable Caching**: GitHub Pages automatically caches static files
2. **CDN**: Content is served via GitHub's CDN for fast global access
3. **HTTPS**: Automatically enabled for secure access

## Custom Domain (Optional)

If you want to use a custom domain like `notes.yourdomain.com`:

1. Add a `CNAME` file to your repository:
   ```
   notes.yourdomain.com
   ```

2. Configure DNS:
   - Add a CNAME record pointing to: `username.github.io`
   - Or use A records for apex domain (see GitHub docs)

3. Update GitHub Pages settings with your custom domain

## Troubleshooting

### Issue: Content not loading
- **Check**: Browser console for errors
- **Solution**: Ensure `subtopics.json` is in the same directory as `index.html`

### Issue: 404 error
- **Check**: GitHub Pages is enabled in settings
- **Solution**: Wait 1-2 minutes after enabling (deployment takes time)

### Issue: Old content showing
- **Solution**: Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
- **Or**: Clear browser cache

### Issue: Mobile menu not working
- **Check**: JavaScript is enabled in browser
- **Solution**: Test in different browser

## Maintenance

### Updating Content
1. Modify `index_old.html` (original source)
2. Run parser: `python3 parse_subtopics.py`
3. Replace `subtopics.json` in repository
4. Commit and push changes
5. GitHub Pages will auto-update (1-2 minutes)

### Adding New Features
1. Modify `index.html`
2. Test locally
3. Push to GitHub
4. Changes reflect automatically

## Support
For issues or questions about the notes content, contact:
- **Email**: muzammil24ma@cds.ac.in
- **LinkedIn**: [S.M. Muzammil Afroz](https://www.linkedin.com/in/muzammil-/)

For technical issues with the website, check:
- Browser console for errors
- GitHub Pages status
- Network tab for failed requests

---

**Note**: All content rights belong to Dr. Ritika Jain. This is for educational purposes only.
