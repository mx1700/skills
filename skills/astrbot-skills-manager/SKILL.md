---
name: astrbot-skills-manager
description: Manage AstrBot skills using vercel-labs/skills CLI. Use when user wants to install, list, or manage AI agent skills for AstrBot. Triggers on phrases like "安装 skill", "管理 AstrBot skills", "添加 skill", "npx skills", "安装 agent-skills".
---

# AstrBot Skills Manager

This skill manages AI agent skills for AstrBot using the `npx skills` CLI tool from vercel-labs/skills.

## When to Use This Skill

Use this skill when the user:

- Wants to install skills from a repository (e.g., "安装 vercel-labs/agent-skills")
- Asks to list available skills from a repository
- Wants to manage (add, remove, update) skills for AstrBot
- Uses phrases like "npx skills", "安装 skill", "添加 skill", "管理 AstrBot skills"

## Important Context

- AstrBot has built-in `npx`, no need to install it
- Skills must be installed to **project-level** (not global)
- AstrBot's data folder is the parent of its skills folder
- Use `-a opencode` parameter because OpenCode installs to the `.agents/skills/` folder in the current directory, which aligns with AstrBot's structure

## How It Works

### Step 1: Determine the Target Repository

The user should specify which skill repository to use. Common repositories:

- `vercel-labs/agent-skills` - Vercel's official collection (most popular)
- Other GitHub repositories with skills

If user doesn't specify, ask them.

### Step 2: List Available Skills

Run the following command from AstrBot's data folder (parent of skills folder):

```bash
cd <astrbot-data-folder>
npx skills add <repo> --list
```

Example:

```bash
npx skills add vercel-labs/agent-skills --list
```

This will display all available skills in the repository.

### Step 3: Ask User Which Skills to Install

Present the list to the user and ask which skills they want to install.

**If user wants ALL skills**: Use `--all` flag (or `--skill '*'`) - do NOT use individual `--skill` parameters.

**If user wants SPECIFIC skills**: Use multiple `--skill <name>` parameters.

### Step 4: Install Skills

From AstrBot's data folder (the parent directory of `skills`), run:

**For all skills:**

```bash
cd <astrbot-data-folder>
npx skills add vercel-labs/agent-skills --all -a opencode
```

**For specific skills:**

```bash
cd <astrbot-data-folder>
npx skills add vercel-labs/agent-skills --skill <skill-name-1> --skill <skill-name-2> -a opencode
```

Example:

```bash
npx skills add vercel-labs/agent-skills --skill frontend-design --skill skill-creator -a opencode
```

### Step 5: Verify Installation

After installation, skills should be available in the `.agents/skills/` folder within the data directory.

## Available Skills from vercel-labs/agent-skills

Based on the official repository, these skills are available:

| Skill Name                | Description                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `react-best-practices`    | React and Next.js performance optimization guidelines from Vercel Engineering. 40+ rules across 8 categories. |
| `web-design-guidelines`   | Review UI code for web interface best practices. 100+ rules covering accessibility, performance, and UX.      |
| `react-native-guidelines` | React Native best practices for AI agents. 16 rules across 7 sections covering performance, architecture.     |
| `composition-patterns`    | React composition patterns that scale. Helps avoid boolean prop proliferation through compound components.    |
| `deploy-to-vercel`        | Deploy applications to Vercel instantly. Returns preview URL and claim URL.                                   |

## Source Formats

When installing skills, you can use various source formats:

| Format            | Example                                                                                             |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| GitHub shorthand  | `npx skills add vercel-labs/agent-skills`                                                           |
| Full GitHub URL   | `npx skills add https://github.com/vercel-labs/agent-skills`                                        |
| Direct skill path | `npx skills add https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines` |
| GitLab URL        | `npx skills add https://gitlab.com/org/repo`                                                        |
| Git SSH URL       | `npx skills add git@github.com:vercel-labs/agent-skills.git`                                        |
| Local path        | `npx skills add ./my-local-skills`                                                                  |

## Other Useful Commands

```bash
# List installed skills
npx skills list

# Check for updates
npx skills check

# Update all skills
npx skills update

# Remove a skill
npx skills remove <skill-name>

# Search for skills
npx skills find <keyword>
```

## Examples

**Example 1: List available skills**

- User: "查看 vercel-labs/agent-skills 有哪些 skills"
- Run: `npx skills add vercel-labs/agent-skills --list`
- Present the list to user

**Example 2: Install specific skills**

- User: "安装 react-best-practices 和 web-design-guidelines"
- Run: `npx skills add vercel-labs/agent-skills --skill react-best-practices --skill web-design-guidelines -a opencode`

**Example 3: Install all skills**

- User: "安装所有 vercel-labs/agent-skills"
- Run: `npx skills add vercel-labs/agent-skills --all -a opencode`

**Example 4: Install from a different repository**

- User: "安装 some-other-org/their-skills"
- Run: `npx skills add some-other-org/their-skills --list` (first list)
- Then: `npx skills add some-other-org/their-skills --skill <name> -a opencode`

## Error Handling

If installation fails:

1. Check if npx is available: `npx --version`
2. Verify the repository exists and is accessible
3. Check if the skill name is correct (use `--list` first)
4. Ensure you're in the correct directory (data folder, not skills folder)

## Notes

- AstrBot must have its data folder accessible
- The `-a opencode` parameter ensures skills are installed to `skills` which is compatible with OpenCode and similar agents
- Skills are typically stored in: `<astrbot-data>/skills/`
