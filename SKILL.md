# Volcengine API Skill

A comprehensive skill for Volcengine API operations, supporting image generation, video generation, and vision understanding.

## Features

### 1. Image Generation (Seedream 4.0)
- Text-to-Image
- Image Editing
- Image-to-Image
- Multiple sizes and styles supported

### 2. Video Generation (Seedance 1.5)
- Text-to-Video
- Image-to-Video
- Camera motion control
- First/last frame control

### 3. Vision Understanding
- Image content analysis
- Object detection and localization

### 4. Task Management
- View generation progress
- Download results
- Manage history

---

## Quick Start

### Installation

```bash
# Option 1: One-click installation (recommended)
./install.sh

# Option 2: Docker
docker compose up --build

# Option 3: Manual installation
pip install -r volcengine-api/requirements.txt
```

### Configuration

```bash
# Option 1: Environment variable (recommended ✅ most secure)
export ARK_API_KEY="your-api-key"

# Option 2: Interactive configuration
./scripts/configure.sh

# Option 3: Configuration file
mkdir -p ~/.volcengine
echo 'api_key: "your-api-key"' > ~/.volcengine/config.yaml
chmod 600 ~/.volcengine/config.yaml  # Important: set secure permissions
```

### Verification

```bash
./scripts/verify_install.sh
```

---

## 🔒 Security Best Practices

> ⚠️ **Important**: API Keys are sensitive credentials. Please follow these security practices.

### 1. Recommended Key Management Methods

| Method | Security | Recommended Use Case |
|--------|----------|---------------------|
| Environment Variables | ⭐⭐⭐⭐⭐ | **Recommended** - All scenarios |
| Secret Management Service | ⭐⭐⭐⭐⭐ | Production environments |
| Config File (with permissions) | ⭐⭐⭐ | Local development |

### 2. Environment Variable Configuration (Recommended)

```bash
# Temporary (current session)
export ARK_API_KEY="your-api-key"

# Permanent (add to shell config)
echo 'export ARK_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc

# Verify setting
echo $ARK_API_KEY | head -c 4  # Should show first 4 characters
```

### 3. Configuration File Security

If you must use a configuration file to store API Key:

```bash
# Create config directory
mkdir -p ~/.volcengine

# Create config file
cat > ~/.volcengine/config.yaml << 'EOF'
api_key: "your-api-key"
base_url: "https://ark.cn-beijing.volces.com/api/v3"
EOF

# Set secure permissions (critical!)
chmod 700 ~/.volcengine          # Directory: owner access only
chmod 600 ~/.volcengine/config.yaml  # File: owner read/write only
```

### 4. File Permission Verification

```bash
# Check directory permissions (should be drwx------ or 700)
ls -la ~ | grep .volcengine

# Check file permissions (should be -rw------- or 600)
ls -la ~/.volcengine/config.yaml
```

### 5. Prohibited Actions

| Prohibited | Reason |
|------------|--------|
| ❌ Committing API Key to Git | Will be publicly accessible |
| ❌ Printing API Key in logs | May leak |
| ❌ Passing API Key in URL | Will be logged |
| ❌ Hardcoding API Key | Difficult to rotate |
| ❌ Sharing API Key | Cannot track accountability |

### 6. .gitignore Configuration

Ensure `.gitignore` includes:

```gitignore
# Volcengine config (may contain API keys)
.volcengine/
*.volcengine/

# Environment files
.env
.env.local
.env.*.local
```

### 7. Key Rotation Recommendations

```bash
# Rotate API Key regularly (recommended every 90 days)
# 1. Generate new key in Volcengine console
# 2. Update environment variable or config file
# 3. Verify new key works correctly
# 4. Delete old key in console
```

---

## Usage

### Image Generation

```
Generate an image: sunset beach with palm trees and waves
```

```
Generate image, size 1024x768, content: city night view
```

### Video Generation

```
Generate a 5-second video: camera slowly pulls out, revealing mountain scenery
```

```
Generate video from this image: https://example.com/image.jpg
```

### Vision Understanding

```
Analyze this image: https://example.com/image.jpg
```

### Task Management

```
Show my task list
```

```
Check status of task task-123
```

```
Download result of task task-123
```

---

## Parameters

### Image Generation Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| prompt | Yes | Image description | - |
| width | No | Width | 1024 |
| height | No | Height | 1024 |
| negative_prompt | No | Negative prompt | - |
| model | No | Model ID | doubao-seedream-4-0-250828 |

### Video Generation Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| prompt | Yes | Video description | - |
| duration | No | Duration (seconds) | 5 |
| aspect_ratio | No | Aspect ratio | 16:9 |
| model | No | Model ID | doubao-seedance-1-5-pro-251215 |

### Vision Understanding Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| image | Yes | Image URL or local path | - |
| prompt | No | Analysis instruction | - |
| model | No | Model ID | doubao-seed-1-6-vision-250815 |

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ARK_API_KEY` | Volcengine API key | **Yes** |
| `VOLCENGINE_BASE_URL` | API base URL | No |
| `VOLCENGINE_OUTPUT_DIR` | Output directory | No |
| `VOLCENGINE_TIMEOUT` | Request timeout (seconds) | No |
| `VOLCENGINE_MAX_RETRIES` | Max retry attempts | No |

### Configuration Files

**Project Config**: `.volcengine/config.yaml`

**Global Config**: `~/.volcengine/config.yaml`

```yaml
# api_key: "your-api-key"  # Recommended: use environment variable
base_url: "https://ark.cn-beijing.volces.com/api/v3"
timeout: 30
max_retries: 3
output_dir: "./output"
```

### Configuration Priority

1. Environment variable `ARK_API_KEY` (**Recommended**)
2. Project config `.volcengine/config.yaml`
3. Global config `~/.volcengine/config.yaml`
4. Default values

---

## Models

| Feature | Model ID |
|---------|----------|
| Image Generation | doubao-seedream-4-0-250828 |
| Video Generation | doubao-seedance-1-5-pro-251215 |
| Vision Understanding | doubao-seed-1-6-vision-250815 |

---

## Important Notes

1. **API Key Required** - Set environment variable or config file first
2. **Image Dimensions** - Use multiples of 64 for best results
3. **Video Duration** - Limited to 1-10 seconds
4. **Async Tasks** - All generation tasks are async, check progress
5. **Rate Limits** - Monitor API call frequency to avoid limits
6. **Data Persistence** - Task state and history stored in `~/.volcengine/`

---

## Data Persistence

This Skill stores data in the following locations:

| Path | Content | Sensitivity |
|------|---------|-------------|
| `~/.volcengine/config.yaml` | Global config (may contain API Key) | ⚠️ Sensitive |
| `~/.volcengine/tasks/` | Task history | Normal |
| `~/.volcengine/state/` | State files | Normal |
| `./.volcengine/config.yaml` | Project config (may contain API Key) | ⚠️ Sensitive |

**Security Recommendations**:
- Ensure config file permissions are 600
- Do not commit `.volcengine/` directory to version control
- Regularly clean up unnecessary history data

---

## Error Handling

| Error Type | Description | Solution |
|------------|-------------|----------|
| Authentication Error | API Key invalid or not set | Check ARK_API_KEY setting |
| Rate Limit | Too many requests | Wait and retry |
| Network Error | Cannot connect to API | Check network connection |
| Parameter Error | Invalid parameter format | Check parameter format |
| Model Error | Model unavailable | Check model ID or contact support |

---

## Example Workflows

### Complete Image Generation Flow

```
1. Set API Key:
   Set API Key: sk-xxx

2. Generate image:
   Generate an image: beautiful sunset

3. Check task status:
   Check task status

4. Download result:
   Download image to local
```

### Image to Video Flow

```
1. Generate initial image:
   Generate an image: mountain scenery

2. Generate video from image:
   Generate video from the image, camera moves right

3. Check progress:
   Check task status

4. Download video:
   Download video to local
```

---

## Deployment Options

| Method | Time | Use Case |
|--------|------|----------|
| Script Installation | 2-3 min | Local development, quick start |
| Docker | 3-5 min | Containerized environment, team collaboration |
| Manual Installation | 5-10 min | Custom environment |

For detailed deployment instructions, see [INSTALLATION.md](./docs/INSTALLATION.md)

---

## Documentation

- [Quick Start](./docs/QUICKSTART.md) - Get started in 30 seconds
- [Installation Guide](./docs/INSTALLATION.md) - Detailed installation instructions
- [Examples](./docs/examples.md) - More code examples
- [Troubleshooting](./docs/troubleshooting.md) - Common issues and solutions
- [README](./README.md) - Full project documentation

---

## Get Help

```bash
# View help script
./scripts/help.sh

# Verify installation
./scripts/verify_install.sh
```

---

**Welcome to Volcengine API Assistant!**

For help, say "help" or "帮助".
