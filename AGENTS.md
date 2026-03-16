# AGENTS.md - Agent Coding Guidelines

This repository contains Agent Skills - a collection of skills that extend AI agent capabilities.

## 必须遵守

在交流,文档,代码注释,git 提交信息中使用中文

## Project Structure

```
skills/
├── .agents/
│   ├── skills/
│   │   ├── pollinations-image/   # Image generation skill
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── generate_image.py
│   │   │   │   └── __init__.py
│   │   │   ├── references/
│   │   │   │   └── models.md
│   │   │   ├── .env
│   │   │   └── assets/
│   │   └── skill-creator/        # Skill creation/optimization skill
│   │       ├── SKILL.md
│   │       ├── scripts/
│   │       ├── agents/
│   │       ├── references/
│   │       └── eval-viewer/
│   └── skills/                   # Project-level skills (in root)
│       └── pollinations-image/
└── skills/                       # Public skills (symlink or copy)
```

### Linting

No formal linter configured. However, the codebase follows Python conventions:

- Run `python -m py_compile <file.py>` to check syntax
- Use `ruff check .` if ruff is installed globally (cache exists: `.ruff_cache/`)

## Code Style Guidelines

### Python Version

- **Python 3.12+** (type annotations like `list[dict]`, not `List[dict]`)

### Imports

- Standard library first, then third-party
- Use explicit imports (no wildcard `*`)
- Sort with `isort` convention: stdlib → third-party → local

```python
# Correct
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import requests
```

### Type Hints

- Use modern Python 3.12+ syntax (no `List`, `Dict`, `Optional` from typing)
- Use `list[dict]` not `List[Dict]`
- Use `X | None` not `Optional[X]`

```python
# Correct
def find_env_file() -> Optional[Path]:
    ...

def check_api_key() -> tuple[bool, Optional[str]]:
    ...

# Avoid (legacy style)
from typing import List, Dict, Optional
def find_env_file() -> Optional[Path]:  # Old style
```

### Naming Conventions

- **Functions/variables**: `snake_case` (e.g., `find_env_file`, `api_key`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES = 3`)
- **Classes**: `PascalCase` (e.g., `ImageGenerator`)

### Docstrings

- Use Google-style or simple docstrings
- Include: description, args, returns for functions
- Module docstring at top of file

```python
"""Module description.

Usage:
    python script.py --arg value
"""

def generate_image(prompt: str, ...) -> dict:
    """Generate an image using Pollinations.ai API.

    Args:
        prompt: Description of the image to generate.
        model: Model to use (default: zimage).
        ...

    Returns:
        dict: Result with 'success' key and either image_url or error info.
    """
```

### Error Handling

- **Return error dictionaries** instead of raising exceptions in CLI scripts
- Use specific exception types (e.g., `requests.exceptions.Timeout`)
- Never use bare `except:`

```python
# Correct pattern (return dict for errors)
try:
    response = requests.get(url, timeout=60)
except requests.exceptions.Timeout:
    return {"success": False, "error": "TIMEOUT", "message": "请求超时"}
except requests.exceptions.RequestException as e:
    return {"success": False, "error": "NETWORK_ERROR", "message": str(e)[:100]}

# Avoid
try:
    ...
except:
    pass  # Never!
```

### CLI Patterns

- Use `argparse` with `RawDescriptionHelpFormatter` for multi-line help
- Exit with `sys.exit(0)` for success, `sys.exit(1)` for errors
- Print errors to `sys.stderr`

```python
parser = argparse.ArgumentParser(
    description="Description",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("--prompt", "-p", help="Description")
parser.add_argument("--flag", action="store_true", help="Flag description")

args = parser.parse_args()

if not args.prompt:
    print("ERROR: --prompt is required", file=sys.stderr)
    sys.exit(1)
```

### Shebang

- Scripts should have `#!/usr/bin/env python3` at the top
- Make executable: `chmod +x script.py`

### Result Patterns

- Functions that can fail should return a dict with consistent structure:

```python
{
    "success": bool,
    "error": str | None,      # Error code if failed
    "message": str | None,    # Human-readable message
    # ... other result fields
}
```

### File Paths

- Use `pathlib.Path` instead of string concatenation
- Use `parents=True, exist_ok=True` for `mkdir()`

```python
from pathlib import Path

save_path = Path("output") / "file.txt"
save_path.parent.mkdir(parents=True, exist_ok=True)
```

## SKILL.md Structure

Skills follow this structure:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code
    ├── references/ - Docs loaded as needed
    └── assets/     - Static files
```

### Frontmatter Format

```yaml
---
name: skill-name
description: When to trigger, what it does. Primary triggering mechanism.
---
```

## Skill Creator Workflow

When creating new skills:

1. Draft SKILL.md with name, description, instructions
2. Create test cases in `evals/evals.json`
3. Run evaluation loops
4. Iterate based on feedback
5. Package with `scripts/package_skill.py`

See `.agents/skills/skill-creator/SKILL.md` for detailed workflow.

## Environment Configuration

- Use `.env` files for API keys
- Check `.env` in cwd first, then `~/.env`
- Never commit `.env` files (already in `.gitignore`)

```python
def find_env_file() -> Optional[Path]:
    env_path = Path(".env")
    if env_path.exists():
        return env_path
    home_env = Path.home() / ".env"
    if home_env.exists():
        return home_env
    return None
```
