---
name: pollinations-image
description: Generate images using Pollinations.ai text-to-image API. Use this skill whenever the user wants to create images from text descriptions, including prompts like "生成一张图片", "create an image", "文生图", "画一幅画", "给我画个X", "帮我生成图片", "text to image", "AI绘图", or any request involving image generation with AI. Supports custom models, sizes, and handles API key configuration.
---

# Pollinations Image Generation

This skill generates images using the Pollinations.ai API. It handles API key configuration, parameter customization, and returns the generated image URL.

## When to Use This Skill

Use this skill when the user:

- Wants to generate an image from a text prompt
- Asks for "文生图", "AI绘图", "生成图片", "画图"
- Uses phrases like "create an image", "text to image", "generate a picture"
- Needs AI-generated images for any purpose
- Asks to create images with specific dimensions, models, or styles

## How It Works

### Step 1: Check API Key Configuration

Before making API calls, the script checks for `.env` file in user's home directory:

- Looks for `~/.env` (home directory only)
- Searches for `POLLINATIONS_API_KEY` in the file

If API key is not found, the script will exit with error `API_KEY_NOT_CONFIGURED`. In this case:

- Ask the user for their API key
- Update `.env` file using the script: `python scripts/generate_image.py --create-env --api-key YOUR_KEY`
- Then retry the image generation

**Prompt user message:**

```
尚未配置 Pollinations API Key。请提供你的 API Key，我会更新 ~/.env 文件。
(如果没有 API Key，可以在 https://pollinations.ai 获取)
```

### Step 2: Parse User Request

Extract the following parameters from the user's request:

| Parameter | Source                                        | Default  |
| --------- | --------------------------------------------- | -------- |
| prompt    | The text description of the image to generate | Required |
| model     | Image generation model                        | `zimage` |
| width     | Image width in pixels                         | `1024`   |
| height    | Image height in pixels                        | `768`    |

**Large/HD Image Detection:**
If the user requests any of the following, use 1600×1200:

- "高清", "HD", "high resolution", "大图", "large size"
- "4K", "ultra", "详细", "细节丰富"
- Width/height requested > 1200

### Step 3: Call the API

Use the `scripts/generate_image.py` script to generate the image:

```bash
python scripts/generate_image.py --prompt "a beautiful sunset" --model zimage --width 1024 --height 768
```

With API key inline:

```bash
python scripts/generate_image.py --prompt "a cat" --api-key YOUR_KEY
```

### Step 4: Return Results

Display the generated image URL to the user:

```
图片已生成! 🎨

📝 提示词: [prompt]
🎨 模型: [model]
📐 尺寸: [width]×[height]

🔗 图片链接: [image_url]

可以直接在浏览器中打开查看。
```

## API Key Setup Flow

1. Run the script: `python scripts/generate_image.py --prompt "test"`
2. If error `API_KEY_NOT_CONFIGURED` appears:
   - Ask user: "请提供你的 Pollinations API Key"
   - After user provides key, update ~/.env:
     ```bash
     python scripts/generate_image.py --create-env --api-key USER_PROVIDED_KEY
     ```
   - Then retry the original request

## Available Models

| Model            | Description                 |
| ---------------- | --------------------------- |
| `zimage`         | Default model (recommended) |
| `flux`           | High-quality flux model     |
| `turbo`          | Fast generation             |
| `gptimage`       | GPT-based image generation  |
| `seedream`       | Seedream model              |
| `nanobanana`     | Creative model              |
| `nanobanana-pro` | Pro version of nanobanana   |

## Script Usage

```bash
# Basic usage
python scripts/generate_image.py --prompt "a cute cat"

# With custom model and size
python scripts/generate_image.py --prompt "landscape" --model flux --width 1600 --height 1200

# With API key inline
python scripts/generate_image.py --prompt "sunset" --api-key YOUR_KEY

# Create .env file
python scripts/generate_image.py --create-env --api-key YOUR_KEY
```

## Error Codes

| Error                    | Meaning          | Action                   |
| ------------------------ | ---------------- | ------------------------ |
| `API_KEY_NOT_CONFIGURED` | No API key found | Prompt user, update ~/.env |
| `AUTH_FAILED`            | Invalid API key  | Ask user for correct key |
| `TIMEOUT`                | Request timeout  | Retry                    |
| `NETWORK_ERROR`          | Network issue    | Check connection, retry  |
| `API_ERROR_XXX`          | Other API errors | Check message            |

## Examples

**Example 1: Basic image generation**

- User: "帮我画一只可爱的猫咪"
- Run: `python scripts/generate_image.py --prompt "一只可爱的猫咪" --model zimage`
- Output: IMAGE_URL: https://...

**Example 2: High-resolution image**

- User: "生成一张高清的城市风景图"
- Run: `python scripts/generate_image.py --prompt "城市风景" --model flux --width 1600 --height 1200`

**Example 3: First time setup**

- Run script → error `API_KEY_NOT_CONFIGURED`
- Ask user for key → user provides "abc123"
- Run: `python scripts/generate_image.py --create-env --api-key abc123`
- Retry original request

## Files

- `scripts/generate_image.py` - Main script for image generation
- `references/models.md` - Available models documentation
