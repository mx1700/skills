---
name: astrbot-skills-manager
description: Manage AstrBot skills using vercel-labs/skills CLI. Use when user wants to install, list, search, or manage AI agent skills for AstrBot. Triggers on phrases like "安装 skill", "管理 AstrBot skills", "添加 skill", "npx skills", "查找 skill", "搜索 skill", "安装 agent-skills".
---

# AstrBot Skills Manager

This skill manages AI agent skills for AstrBot using the `npx skills` CLI tool from vercel-labs/skills.

## When to Use This Skill

Use this skill when the user:

- Wants to install skills from ANY repository
- Asks to list available skills from a repository
- Wants to search for skills by keyword
- Wants to manage (add, remove, update) skills for AstrBot
- Uses phrases like "npx skills", "安装 skill", "添加 skill", "管理 AstrBot skills", "搜索 skill"

## Important Context

- AstrBot has built-in `npx`, no need to install it
- Skills must be installed to **project-level** (not global)
- Run commands from the directory where you want skills to be installed (AstrBot's data/profiles folder)
- Use `-a openclaw` parameter because OpenClaw installs to the `skills/` folder in the current directory, which aligns with AstrBot's structure
- AstrBot skills are stored in: `<astrbot-data>/skills/`

## How It Works

### Step 1: Determine the Target Repository

Ask the user which skill repository they want to use. Examples:

- `vercel-labs/agent-skills` - Vercel's official collection (most popular)
- Any other GitHub/GitLab repository with skills
- User can provide: owner/repo, full URL, or local path

### Step 2: List Available Skills

Run the following command to view available skills in the repository:

```bash
npx skills add <repo> --list
```

Examples:

```bash
# GitHub shorthand
npx skills add vercel-labs/agent-skills --list

# Full GitHub URL
npx skills add https://github.com/vercel-labs/agent-skills --list

# GitLab
npx skills add https://gitlab.com/org/repo --list
```

This will display all available skills in the repository.

### Step 3: Ask User Which Skills to Install

Present the list to the user and ask which skills they want to install.

**If user wants ALL skills**: Use `--all` flag - do NOT use individual `--skill` parameters.

**If user wants SPECIFIC skills**: Use multiple `--skill <name>` parameters.

### Step 4: Install Skills

Run the install command with `-a openclaw`:

**For all skills:**

```bash
npx skills add <repo> --all -a openclaw
```

**For specific skills:**

```bash
npx skills add <repo> --skill <skill-name-1> --skill <skill-name-2> -a openclaw
```

### Step 5: Verify Installation

After installation, skills should be available in the `skills/` folder in the current directory.

## Source Formats

You can use various source formats to specify the skill repository:

| Format                           | Example                                                                    |
| -------------------------------- | -------------------------------------------------------------------------- |
| GitHub shorthand                 | `npx skills add owner/repo`                                                |
| Full GitHub URL                  | `npx skills add https://github.com/owner/repo`                             |
| Direct skill path (single skill) | `npx skills add https://github.com/owner/repo/tree/main/skills/skill-name` |
| GitLab URL                       | `npx skills add https://gitlab.com/org/repo`                               |
| Git SSH URL                      | `npx skills add git@github.com:owner/repo.git`                             |
| Local path                       | `npx skills add ./my-local-skills`                                         |

## Other Useful Commands

```bash
# List installed skills
npx skills list

# Search for skills by keyword
npx skills find <keyword>

# Check for updates
npx skills check

# Update all skills
npx skills update

# Remove a skill
npx skills remove <skill-name>

# Remove all skills
npx skills remove --all
```

## Examples

**Example 1: List available skills from a repository**

- User: "查看 vercel-labs/agent-skills 有哪些 skills"
- Run: `npx skills add vercel-labs/agent-skills --list`
- Present the list to user

**Example 2: Install specific skills from a repository**

- User: "安装 vercel-labs/agent-skills 的 react-best-practices"
- Run: `npx skills add vercel-labs/agent-skills --skill react-best-practices -a openclaw`

**Example 3: Install all skills from a repository**

- User: "安装所有 vercel-labs/agent-skills"
- Run: `npx skills add vercel-labs/agent-skills --all -a openclaw`

**Example 4: Install from a different repository**

- User: "安装 some-other-org/their-skills"
- Run: `npx skills add some-other-org/their-skills --list` (first list)
- Then: `npx skills add some-other-org/their-skills --skill <name> -a openclaw`

**Example 5: Search for skills**

- User: "搜索 react 相关的 skills"
- Run: `npx skills find react`

**Example 6: Install a single skill from a specific path**

- User: "安装某个仓库里的 web-design-guidelines"
- Run: `npx skills add https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines -a openclaw`

## Popular Skill Repositories

Here are some popular skill repositories users might want to install from:

- `vercel-labs/agent-skills` - Vercel's official collection (React, web design, React Native, Vercel deploy)
- Any GitHub repository with `SKILL.md` files in `skills/` directory

## Error Handling

If installation fails:

1. Check if npx is available: `npx --version`
2. Verify the repository exists and is accessible
3. Check if the skill name is correct (use `--list` first)
4. Ensure you're in the correct directory (AstrBot's profiles/data folder)

## Notes

- This skill supports installing from **ANY** valid skill repository, not just vercel-labs/agent-skills
- The `-a openclaw` parameter ensures skills are installed to `skills/` which is compatible with OpenClaw and AstrBot
- AstrBot stores skills in: `<astrbot-data>/skills/`
