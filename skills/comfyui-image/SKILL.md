---
name: comfyui-image
description: Generate images using ComfyUI API. Use this skill when user wants to generate images via ComfyUI workflow, including prompts like "生成一张图片", "create an image", "文生图", "画一幅画", "给我画个X", "帮我生成图片", "text to image", "AI绘图", "使用comfyui生成图片", "comfyui文生图", "comfyui image generation", or requests using local ComfyUI server.
---

# ComfyUI Image Generation

This skill generates images using ComfyUI's API endpoint. It handles server configuration, workflow execution, and returns the generated image path.

## When to Use This Skill

Use this skill when the user:

- Wants to generate images using ComfyUI
- Asks for "comfyui生成图片", "comfyui文生图"
- Needs to use a local or remote ComfyUI server
- Has a ComfyUI workflow JSON file

## How It Works

### Step 1: Check ComfyUI Server Configuration

Before making API calls, the script checks for `.env` file in the skill directory:

- Looks for `comfyui-image/.env` (skill directory)
- Falls back to `~/.env` (home directory)
- Searches for `COMFYUI_HOST` in the file (e.g., `http://127.0.0.1:8188`)

If server is not configured, the script will exit with error `COMFYUI_NOT_CONFIGURED`. In this case:

- Ask the user for their ComfyUI server address
- Update `.env` file using the script: `python scripts/generate_image.py --create-env --host YOUR_HOST`
- Then retry the image generation

**Prompt user message:**

```
尚未配置 ComfyUI 服务器地址。请提供你的 ComfyUI 服务器地址 (例如 http://127.0.0.1:8188)，我会更新 .env 文件。
```

### Step 2: Parse User Request

Extract the following parameters from the user's request:

| Parameter | Source                                        | Default  |
| --------- | --------------------------------------------- | -------- |
| prompt    | The text description of the image to generate | Required |
| width     | Image width in pixels                         | `1024`   |
| height    | Image height in pixels                        | `768`    |

**Large/HD Image Detection:**
If the user requests any of the following, use 1600×1200:

- "高清", "HD", "high resolution", "大图", "large size"
- "4K", "ultra", "详细", "细节丰富"
- Width/height requested > 1200

### Step 3: Call the ComfyUI API

Use the `scripts/generate_image.py` script to generate the image:

```bash
python scripts/generate_image.py --prompt "a beautiful sunset"
```

With host inline:

```bash
python scripts/generate_image.py --prompt "a cat" --host http://127.0.0.1:8188
```

### Step 4: Return Results

Display the generated image path to the user:

```
图片已生成! 🎨

📝 提示词: [prompt]
📐 尺寸: [width]×[height]

💾 保存路径: [saved_path]

可以在浏览器中打开查看。
```

## Server Setup Flow

1. Run the script: `python scripts/generate_image.py --prompt "test"`
2. If error `COMFYUI_NOT_CONFIGURED` appears:
   - Ask user: "请提供你的 ComfyUI 服务器地址"
   - After user provides host, update .env:
     ```bash
     python scripts/generate_image.py --create-env --host http://127.0.0.1:8188
     ```
   - Then retry the original request

## Script Usage

```bash
# Basic usage
python scripts/generate_image.py --prompt "a cute cat"

# With custom size
python scripts/generate_image.py --prompt "landscape" --width 1600 --height 1200

# With host inline
python scripts/generate_image.py --prompt "sunset" --host http://127.0.0.1:8188

# Create .env file
python scripts/generate_image.py --create-env --host http://127.0.0.1:8188

# Use custom workflow
python scripts/generate_image.py --prompt "cat" --workflow custom_workflow.json
```

## Workflow File

The skill uses `references/zimage.json` as the default workflow. This ComfyUI workflow:

- Uses zImageTurbo model for fast, high-quality generation
- Supports positive and negative prompts
- Outputs to PreviewImage node (node 15)

The workflow dimensions can be overridden via command-line arguments.

## Error Codes

| Error                       | Meaning                        | Action                        |
| --------------------------- | ------------------------------ | ----------------------------- |
| `COMFYUI_NOT_CONFIGURED`    | No server host found           | Prompt user, update .env     |
| `CONNECTION_FAILED`         | Cannot connect to ComfyUI      | Check if server is running    |
| `WORKFLOW_ERROR`            | Invalid workflow JSON          | Check workflow file syntax    |
| `EXECUTION_FAILED`          | Workflow execution error       | Check ComfyUI console         |
| `TIMEOUT`                   | Request timeout                | Retry                         |
| `NETWORK_ERROR`             | Network issue                  | Check connection, retry       |

## Examples

**Example 1: Basic image generation**

- User: "帮我用comfyui画一只可爱的猫咪"
- Run: `python scripts/generate_image.py --prompt "一只可爱的猫咪"`
- Output: SAVED_PATH: /tmp/comfyui/...

**Example 2: High-resolution image**

- User: "生成一张高清的comfyui城市风景图"
- Run: `python scripts/generate_image.py --prompt "城市风景" --width 1600 --height 1200

**Example 3: First time setup**

- Run script → error `COMFYUI_NOT_CONFIGURED`
- Ask user for host → user provides "http://192.168.1.100:8188"
- Run: `python scripts/generate_image.py --create-env --host http://192.168.1.100:8188`
- Retry original request

## Files

- `scripts/generate_image.py` - Main script for image generation
- `references/zimage.json` - Default ComfyUI workflow (zImageTurbo)
