# Skills

Agent Skills 集合。

## Index

| Skill                                     | Description |
| ----------------------------------------- | ----------- |
| [pollinations-image](#pollinations-image) | 文生图      |

---

## Pollinations Image

使用 Pollinations.ai 进行文生图。

### Trigger Phrases

- "生成图片", "画图", "文生图", "AI绘图", "给我画个X"
- "create an image", "generate a picture", "text to image"

### How It Works

1. 用户提出图片生成需求时触发
2. 询问用户图片描述（prompt）
3. 自动选择合适的模型和尺寸（高清需求自动使用更大尺寸）
4. 调用 API 生成图片并保存到临时目录
5. 返回图片路径给用户

### Available Models

| Model            | Description          |
| ---------------- | -------------------- |
| `zimage`         | 默认模型，综合效果好 |
| `flux`           | 高质量模型           |
| `turbo`          | 快速生成             |
| `gptimage`       | GPT 图像生成         |
| `nanobanana`     | 创意风格             |
| `nanobanana-pro` | 专业版               |

### Size Options

- 默认: 1024 × 768
- 高清/大图: 1600 × 1200 (用户说 "高清"、"HD"、"大图" 时自动使用)

### Examples

**基础用法**

- 用户: "帮我画一只猫咪" → 生成 1024×768 图片

**指定模型**

- 用户: "用 flux 画一个 sunset" → 使用 flux 模型

**指定尺寸**

- 用户: "生成一张 1600×1200 的城市风景" → 使用高清尺寸

**组合使用**

- 用户: "用 nanobanana 画一幅 1600×1200 的抽象画" → 指定模型和尺寸
