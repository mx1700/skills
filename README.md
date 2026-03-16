# Skills

Agent Skills 集合。

## Index

| Skill                                       | Description |
| ------------------------------------------- | ----------- |
| [pollinations-image](#pollinations-image)   | 文生图      |
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
