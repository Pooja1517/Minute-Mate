# Deployment Failure Troubleshooting Guide

## Current Status
- ✅ `minute-mate-backend` - Deployed successfully (23h ago)
- ❌ `minute-mate-whisper` - Failed deploy (5 days ago)

## Quick Fixes to Try

### Option 1: Use Stable Versions (Recommended)
Replace your current `render.yaml` with the stable version:

```bash
# Backup current file
cp render.yaml render-backup.yaml

# Use stable version
cp render-stable.yaml render.yaml
```

### Option 2: Use Minimal Configuration
If Option 1 fails, try the minimal approach:

```bash
# Use minimal configuration
cp render-minimal.yaml render.yaml
```

### Option 3: Use Docker Approach
If both fail, try Docker:

```bash
# Use Docker configuration
cp render-docker-only.yaml render.yaml
```

## Step-by-Step Troubleshooting

### Step 1: Check Build Logs
1. Go to your Render dashboard
2. Click on `minute-mate-whisper` service
3. Check the "Logs" tab for specific error messages
4. Look for:
   - `__version__` KeyError
   - ffmpeg installation errors
   - Memory issues
   - Package conflicts

### Step 2: Try Different Build Approaches

#### Approach A: Stable Build
```yaml
buildCommand: chmod +x build-stable.sh && ./build-stable.sh
```

#### Approach B: Minimal Build
```yaml
buildCommand: chmod +x build-minimal.sh && ./build-minimal.sh
```

#### Approach C: Docker Build
```yaml
env: docker
dockerfilePath: ./Dockerfile
```

### Step 3: Manual Deployment Test

1. **Create a new service** in Render
2. **Use the minimal configuration** first
3. **Test with a simple build** before adding complexity

## Common Error Solutions

### Error: `__version__` KeyError
**Solution**: Use `requirements-stable.txt` or `requirements-minimal.txt`

### Error: ffmpeg not found
**Solution**: Ensure `build.sh` is executable and includes ffmpeg installation

### Error: Memory issues
**Solution**: Use Docker approach or minimal requirements

### Error: Package conflicts
**Solution**: Use `--no-cache-dir` and `--force-reinstall` flags

## Immediate Action Plan

1. **Try the stable version first**:
   ```bash
   cp render-stable.yaml render.yaml
   # Deploy in Render
   ```

2. **If that fails, try minimal**:
   ```bash
   cp render-minimal.yaml render.yaml
   # Deploy in Render
   ```

3. **If both fail, try Docker**:
   ```bash
   cp render-docker-only.yaml render.yaml
   # Deploy in Render
   ```

## Environment Variables to Set

Make sure these are set in your Render service:
- `NOTION_TOKEN` (if using Notion)
- `NOTION_DATABASE_ID` (if using Notion)
- `PYTHONUNBUFFERED=1`
- `FLASK_ENV=production`

## Testing After Deployment

1. **Check health endpoint**: `https://your-whisper-service.onrender.com/health`
2. **Test with small audio file** (< 5MB)
3. **Monitor logs** for any runtime errors

## If All Else Fails

1. **Create a new service** with a different name
2. **Use the Docker approach** as it's most reliable
3. **Start with minimal configuration** and add features gradually

## Contact Support

If none of these solutions work:
1. **Check Render status page** for any platform issues
2. **Contact Render support** with your build logs
3. **Consider upgrading** to a paid plan for more resources 