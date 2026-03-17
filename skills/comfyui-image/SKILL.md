---
name: comfyui-image
description: Generate images using ComfyUI API. Use this skill whenever the user requests image generation, drawing, or AI art creation — including phrases like "生成图片", "画一张图", "文生图", "AI绘图", "generate an image", "create a picture", "text to image", or mentions ComfyUI. This skill handles prompt parsing, dimension detection, and workflow execution automatically.
---

# ComfyUI Image Generation

Generate images via ComfyUI's local or remote API.

## Quick Start

Run the script with the user's prompt:

```bash
python /AstrBot/data/skills/comfyui-image/scripts/generate_image.py --prompt "用户描述的内容"
```

## Parameters

| 参数         | 说明             | 默认值       |
| ------------ | ---------------- | ------------ |
| `--prompt`   | 图片描述（必需） | -            |
| `--width`    | 宽度             | 1024         |
| `--height`   | 高度             | 768          |
| `--host`     | ComfyUI 地址     | 从 .env 读取 |
| `--workflow` | 自定义工作流     | zimage.json  |

## Dimension Detection

自动检测并使用高分辨率 (1600×1200) 当用户请求包含：

- "高清"、"HD"、"high resolution"、"大图"、"large"
- "ultra"、"详细"、"细节丰富"

## Server Setup

首次运行若返回 `COMFYUI_NOT_CONFIGURED`：

1. 询问用户 ComfyUI 服务器地址
2. 创建配置：

```bash
python scripts/generate_image.py --create-env --host http://127.0.0.1:8188
```

3. 重试原图生成请求

## Output Format

成功时输出 `SAVED_PATH: /path/to/image.png`

向用户展示结果：

```
图片已生成！
📝 提示词: [prompt]
📐 尺寸: [width]×[height]
💾 保存路径: [path]
```

## Error Handling

| 错误                     | 处理                                  |
| ------------------------ | ------------------------------------- |
| `COMFYUI_NOT_CONFIGURED` | 询问用户服务器地址，创建 .env         |
| `CONNECTION_FAILED`      | 提示检查 ComfyUI 是否运行             |
| 其他错误                 | 展示错误信息，建议检查 ComfyUI 控制台 |
