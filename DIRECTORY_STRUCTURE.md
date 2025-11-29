# 📁 StatHub Backend Directory Structure

## Required Directories

Your backend needs these directories for proper operation:

```
StatHub-backend/
├── static/                    # Static files (served at /static)
│   ├── news_images/          # News article images
│   │   └── news_*.jpg
│   └── profile_pics/         # OLD location (deprecated, use uploads/avatars/)
│
├── uploads/                   # User-uploaded files (served at /uploads)
│   └── avatars/              # Profile pictures
│       └── {uuid}.{ext}
│
└── ... (other backend files)
```

## Directory Creation

### Automatic Creation
- ✅ `uploads/avatars/` - Created automatically on first photo upload
- ✅ `static/news_images/` - Created automatically when saving news images

### Manual Creation (Optional)
If you want to create them manually:

```bash
mkdir -p uploads/avatars
mkdir -p static/news_images
```

Or on Windows:
```powershell
mkdir uploads\avatars
mkdir static\news_images
```

## Render Deployment

Render will:
1. ✅ Auto-create directories when code runs
2. ✅ Persist files in these directories across deployments
3. ⚠️ **Important**: Empty directories may not persist - files inside them ensure persistence

### First Deployment
If directories don't exist on first deployment:
1. The code will create them automatically
2. Or create empty `.gitkeep` files to ensure they exist:
   ```bash
   touch uploads/avatars/.gitkeep
   touch static/news_images/.gitkeep
   ```

## Path Mapping

| URL Path | File System | Purpose |
|----------|-------------|---------|
| `/static/news_images/...` | `static/news_images/...` | News article images |
| `/uploads/avatars/...` | `uploads/avatars/...` | User profile pictures |

## Migration Notes

### Old vs New Photo Paths

**OLD** (deprecated):
- Path: `/static/profile_pics/{filename}`
- Files: `static/profile_pics/*`

**NEW** (current):
- Path: `/uploads/avatars/{filename}`
- Files: `uploads/avatars/*`

### Backward Compatibility

If you have existing photos in `static/profile_pics/`:
- They will still be accessible at `/static/profile_pics/...`
- New uploads go to `/uploads/avatars/`
- Consider migrating old photos if needed

## Verification

After deployment, verify directories exist:

```bash
# Check if directories exist
ls -la uploads/avatars/
ls -la static/news_images/

# Test upload
# Upload a photo via API - should create file in uploads/avatars/
```

---

**Directory structure is ready! 🎯**

