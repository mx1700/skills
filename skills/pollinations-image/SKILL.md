---
name: pollinations-image
description: Generate images using Pollinations.ai text-to-image API. Use this skill whenever the user wants to create images from text descriptions, including phrases like "生成图片", "create an image", "文生图", "画一幅画", "给我画个X", "帮我生成图片", "text to image", "AI绘图", or any request involving image generation. ALWAYS use this skill when the user mentions images, pictures, drawings, illustrations, or visual content creation, even if they don't explicitly say "generate image". Make sure to use this skill for any visual content request, including logos, artwork, photos, graphics, or when the user wants to visualize something.
---

# Pollinations Image Generation

Generate images using the Pollinations.ai API.

## 必须严格遵守的规则

- 出现 API_KEY 错误不要尝试绕过! 直接向用户索要 API_KEY!

## When to Use

Use this skill when the user wants to:
- Generate images from text prompts
- Create AI artwork, illustrations, or photos
- Visualize concepts or ideas
- Generate logos, graphics, or designs

## Parameters

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| prompt | Yes | - | Image description |
| model | No | zimage | See references/models.md |
| width | No | 1024 | Use 1600 for HD requests |
| height | No | 768 | Use 1200 for HD requests |

**HD Detection:** Use 1600×1200 when user mentions "高清", "HD", "high resolution", "4K", "detailed", "professional quality".

## Usage

Execute the script directly:

```bash
python scripts/generate_image.py --prompt "a beautiful sunset" --model zimage --width 1024 --height 768
```

## Server Setup

首次运行若返回 `API_KEY_NOT_CONFIGURED` 错误：

1. 询问用户 API key
2. 创建配置：

```bash
python scripts/generate_image.py --create-env --api-key USER_KEY
```

3. 重试原图生成请求

## Error Handling

| 错误                     | 处理                                  |
| ------------------------ | ------------------------------------- |
| `API_KEY_NOT_CONFIGURED` | 询问用户 API_KEY，创建 .env         |
| 其他错误                 | 展示错误信息 |


## Output Format

Display results to user:

```
图片已生成!

📝 提示词: [prompt]
🎨 模型: [model]
📐 尺寸: [width]×[height]
```

## Files

- `scripts/generate_image.py` - Main generation script
- `references/models.md` - Model selection guide
