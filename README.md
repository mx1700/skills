# Skills

Agent Skills 集合。

## Index

| Skill                                       | Description |
| ------------------------------------------- | ----------- |
| [pollinations-image](#pollinations-image)   | 文生图 (Pollinations.ai) |
| [comfyui-image](#comfyui-image)              | 文生图 (ComfyUI)        |
| [astrbot-skills-manager](#astrbot-skills-manager) | 管理 AstrBot skills |

---

## AstrBot Skills Manager

管理 AstrBot 的 agent skills。

### Trigger Phrases

- "安装 skill", "管理 AstrBot skills", "添加 skill"
- "列出可用的 skills", "搜索 skill"

### How It Works

1. 用户提出管理 skills 需求时触发
2. 询问用户要使用的 skill 仓库（任意 GitHub/GitLab 仓库）
3. 查看并选择要安装的 skills
4. 安装到项目中
5. 完成后告知用户

### Examples

**查看 skills**
- 用户: "查看 vercel-labs/agent-skills 有哪些 skills" → 列出可用的 skills

**安装 skills**
- 用户: "安装 vercel-labs/agent-skills 的 react-best-practices" → 安装指定 skill
- 用户: "安装所有 vercel-labs/agent-skills" → 安装全部

**搜索 skills**
- 用户: "搜索 react 相关的 skills" → 列出匹配的 skills

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

---

## ComfyUI Image

使用本地 ComfyUI 服务器进行文生图。

### Trigger Phrases

- "使用comfyui生成图片", "comfyui文生图", "comfyui画图"
- "comfyui generate image", "comfyui image generation"

### How It Works

1. 用户提出使用 ComfyUI 生成图片时触发
2. 询问用户图片描述（prompt）
3. 检查 ComfyUI 服务器是否已配置
4. 若未配置，引导用户配置服务器地址
5. 调用本地 ComfyUI 生成图片
6. 返回图片路径给用户

### 首次配置

需要配置 ComfyUI 服务器地址：

```bash
# 在 skills 目录下运行
python scripts/generate_image.py --create-env --host http://127.0.0.1:8188
```

### Size Options

- 默认: 1024 × 768
- 高清/大图: 1600 × 1200 (用户说 "高清"、"HD"、"大图" 时自动使用)

### Examples

**基础用法**
- 用户: "帮我用comfyui画一只猫咪" → 生成图片

**高清图片**
- 用户: "生成一张高清的comfyui城市风景图" → 生成 1600×1200 图片
