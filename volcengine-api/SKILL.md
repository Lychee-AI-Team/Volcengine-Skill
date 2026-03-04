# Volcengine API Skill

Unified skill for Volcengine ARK image generation, video generation, vision understanding, and task querying.

## Scope

- Image generation: Seedream series
- Video generation: Seedance series
- Vision understanding: Seed Vision 1.6
- Task lifecycle: create, query, status polling, result download
- Standardized end-to-end smoke test script

## Current Model IDs

- Image
  - `doubao-seedream-4-0-250828`
  - `doubao-seedream-4-5-251128`
- Video
  - `doubao-seedance-1-5-pro-251215`
  - `doubao-seedance-1-5-250415`
- Vision
  - `doubao-seed-1-6-vision-250815`

## API Endpoints (Current)

- Image generation: `POST /images/generations`
- Video task creation: `POST /contents/generations/tasks`
- Video task query: `GET /contents/generations/tasks/{task_id}`
- Vision understanding: `POST /responses`

Base URL:

- `https://ark.cn-beijing.volces.com/api/v3`

## Installation Options

### Option 1: Script installation (recommended)

```bash
git clone https://github.com/Lychee-AI-Team/Volcengine-Skill.git
cd Volcengine-Skill
./install.sh
export ARK_API_KEY="your-api-key"
python3 examples/quickstart.py
```

### Option 2: Docker

```bash
git clone https://github.com/Lychee-AI-Team/Volcengine-Skill.git
cd Volcengine-Skill
echo "ARK_API_KEY=your-api-key" > .env
docker compose up --build
```

### Option 3: AI chat installation (OpenClaw)

Send this in OpenClaw chat:

```text
Please install this skill from SKILL.md:
https://raw.githubusercontent.com/Lychee-AI-Team/Volcengine-Skill/main/volcengine-api/SKILL.md
```

After OpenClaw installation, verify in local workspace:

```bash
python scripts/smoke_e2e.py --help
```

### Option 4: Manual

```bash
git clone https://github.com/Lychee-AI-Team/Volcengine-Skill.git
cd Volcengine-Skill
python3 -m pip install -r volcengine-api/requirements.txt
export PYTHONPATH="$(pwd)/volcengine-api:${PYTHONPATH}"
export ARK_API_KEY="your-api-key"

# Optional relay/proxy base URL
# export VOLCENGINE_BASE_URL="https://your-relay.example.com/api/v3"
```

## Key Scripts (Latest)

Run from repository root.

- `./install.sh`
  - One-click bootstrap: Python check, dependency install, config template creation
- `./scripts/configure.sh`
  - Interactive API key setup (env / config file / both)
- `./scripts/verify_install.sh`
  - Environment and dependency verification, optional API connectivity check
- `python scripts/smoke_e2e.py`
  - Standardized E2E smoke flow:
    - image generation -> vision understanding -> image-to-video task + polling

Smoke test examples:

```bash
python scripts/smoke_e2e.py
python scripts/smoke_e2e.py --image-prompt "Cyberpunk city at night" --video-prompt "Camera rises as flying cars streak by"
```

## Quick API Usage

```python
from toolkit.api_client import VolcengineAPIClient
from toolkit.config import ConfigManager

config = ConfigManager()
client = VolcengineAPIClient(config)

image = client.post("/images/generations", json={
    "model": "doubao-seedream-4-0-250828",
    "prompt": "Sunset beach with palm trees",
    "size": "1024x1024",
    "response_format": "url",
})

task = client.post("/contents/generations/tasks", json={
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [{"type": "text", "text": "Camera slowly pulls out --duration 5"}],
})

vision = client.post("/responses", json={
    "model": "doubao-seed-1-6-vision-250815",
    "input": [{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Describe this image."},
            {"type": "input_image", "image_url": image["data"][0]["url"]},
        ],
    }],
})

print(image["data"][0]["url"])
print(task["id"])
print(vision)
```

## Configuration Priority

1. `ARK_API_KEY` environment variable
2. `VOLCENGINE_BASE_URL` environment variable
3. Project config: `.volcengine/config.yaml`
4. Global config: `~/.volcengine/config.yaml`
5. Default values

## Security Notes

- Prefer environment variable for API key.
- If storing key in config file, run:

```bash
chmod 700 ~/.volcengine
chmod 600 ~/.volcengine/config.yaml
```

- Never commit API keys into git.

## Troubleshooting

- `AuthenticationError`
  - Check `ARK_API_KEY` value and account permissions.
- `ModuleNotFoundError: toolkit`
  - Ensure `export PYTHONPATH="$(pwd)/volcengine-api:${PYTHONPATH}"`.
- Video task remains running
  - Poll with `GET /contents/generations/tasks/{task_id}` until terminal status.

## References

- Repository README (EN): `../README.md`
- Repository README (CN): `../README_CN.md`
- Quickstart doc: `../docs/QUickstart.md`
- Installation doc: `../docs/INSTALLATION.md`
- Examples doc: `../docs/examples.md`
- Troubleshooting doc: `../docs/troubleshooting.md`
