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

使用 vercel-labs/skills CLI 管理 AstrBot 的 agent skills。

### Trigger Phrases

- "安装 skill", "管理 AstrBot skills", "添加 skill"
- "npx skills", "安装 agent-skills"
- "列出可用的 skills", "搜索 skill"

### How It Works

1. 用户提出管理 skills 需求时触发
2. 询问用户要使用的 skill 仓库（任意 GitHub/GitLab 仓库）
3. 使用 `npx skills add <repo> --list` 查看可用的 skills
4. 询问用户要安装哪些 skills
5. 使用 `-a opencode -y` 安装到项目级（不使用 `-g` 全局），`-y` 参数跳过确认
6. 全部安装时使用 `--all` 参数

### Source Formats (安装源格式)

| 格式 | 示例 |
| ---- | ---- |
| GitHub 简写 | `npx skills add owner/repo` |
| 完整 GitHub URL | `npx skills add https://github.com/owner/repo` |
| 直接 skill 路径 | `npx skills add https://github.com/.../tree/main/skills/skill-name` |
| GitLab URL | `npx skills add https://gitlab.com/org/repo` |
| Git SSH URL | `npx skills add git@github.com:owner/repo.git` |
| 本地路径 | `npx skills add ./my-local-skills` |

### Other Commands

```bash
# 搜索 skills
npx skills find <关键词>

# 列出已安装的 skills
npx skills list

# 检查更新
npx skills check

# 更新所有 skills
npx skills update

# 移除 skill
npx skills remove <skill-name>
```

### Examples

**列出可用 skills**
- 用户: "查看 vercel-labs/agent-skills 有哪些 skills"
- 运行: `npx skills add vercel-labs/agent-skills --list`

**安装指定 skills**
- 用户: "安装 vercel-labs/agent-skills 的 react-best-practices"
- 运行: `npx skills add vercel-labs/agent-skills --skill react-best-practices -a opencode -y`

**安装全部 skills**
- 用户: "安装所有 vercel-labs/agent-skills"
- 运行: `npx skills add vercel-labs/agent-skills --all -a opencode -y`

**安装任意仓库**
- 用户: "安装 other-org/some-skills"
- 运行: `npx skills add other-org/some-skills --list` (先查看)
- 然后: `npx skills add other-org/some-skills --skill <name> -a opencode -y`

**搜索 skills**
- 用户: "搜索 react 相关的 skills"
- 运行: `npx skills find react`

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

使用 ComfyUI API 进行文生图。

### Trigger Phrases

- "使用comfyui生成图片", "comfyui文生图", "comfyui画图"
- "comfyui generate image", "comfyui image generation"

### How It Works

1. 用户提出使用 ComfyUI 生成图片时触发
2. 询问用户图片描述（prompt）
3. 检查 `.env` 配置的 ComfyUI 服务器地址
4. 若未配置，提示用户提供服务器地址
5. 调用 ComfyUI API 执行工作流生成图片
6. 下载生成的图片到本地临时目录
7. 返回图片路径给用户

### 首次配置

首次使用需要配置 ComfyUI 服务器地址：

```bash
cd skills/comfyui-image
python scripts/generate_image.py --create-env --host http://127.0.0.1:8188
```

或运行时通过 `--host` 参数指定：

```bash
python scripts/generate_image.py --prompt "a cat" --host http://127.0.0.1:8188
```

### Size Options

- 默认: 1024 × 768
- 高清/大图: 1600 × 1200 (用户说 "高清"、"HD"、"大图" 时自动使用)

### Script Usage

```bash
# 基本用法
python scripts/generate_image.py --prompt "a cute cat"

# 指定尺寸
python scripts/generate_image.py --prompt "landscape" --width 1600 --height 1200

# 指定服务器地址
python scripts/generate_image.py --prompt "sunset" --host http://127.0.0.1:8188

# 指定输出目录
python scripts/generate_image.py --prompt "cat" --output /path/to/save

# 创建 .env 配置
python scripts/generate_image.py --create-env --host http://127.0.0.1:8188
```

### Workflow

默认使用 `references/zimage.json` 工作流（zImageTurbo 模型）。该工作流：
- 使用 zImageTurbo 快速生成模型
- 支持正向提示词和负向提示词
- 自动适配用户指定的图片尺寸

### Error Codes

| Error                       | Meaning                  | Action                     |
| --------------------------- | ------------------------ | -------------------------- |
| `COMFYUI_NOT_CONFIGURED`    | 未配置服务器地址          | 运行 --create-env 配置     |
| `CONNECTION_FAILED`         | 无法连接 ComfyUI 服务器  | 检查服务器是否运行          |
| `WORKFLOW_ERROR`            | 工作流 JSON 格式错误      | 检查工作流文件             |
| `EXECUTION_FAILED`          | 工作流执行失败            | 检查 ComfyUI 控制台输出    |
| `TIMEOUT`                   | 生成超时                  | 增加 --timeout 参数        |

### Examples

**基础用法**

- 用户: "帮我用comfyui画一只猫咪"
- 运行: `python scripts/generate_image.py --prompt "一只可爱的猫咪"`
- 输出: 图片保存到 `/tmp/comfyui/`

**高清图片**

- 用户: "生成一张高清的comfyui城市风景图"
- 运行: `python scripts/generate_image.py --prompt "城市风景" --width 1600 --height 1200`
