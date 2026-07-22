# SAVILE: Single Source of Truth Engine for Agent Prompts & Skills

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/ "Python 3.11+ Version Support")
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/ "Model Context Protocol Standard Compliance")
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/mr8lu/savile/blob/main/LICENSE "MIT License")

**SAVILE** acts as the definitive "Next.js for Agent Prompts." It provides a powerful local-first environment to write, version, and compile AI logic into universally portable formats.

It operates as a three-tier architecture that orchestrates your agent logic:
1. **The Methodology (Method Framework):** The core psychology and workflow definitions behind how your agents think.
2. **The SSoT Vault (Savile):** A Git-native database where you fork, customize, and version your specific personas, frameworks, and evaluations.
3. **The Universal Export (Vercel Skills & MCP):** Savile seamlessly compiles your custom logic into portable **Vercel Labs SKILL.md formats** for global distribution via `npx skills add`, or serves them dynamically on `localhost` via the **Model Context Protocol (MCP)**.

---

## 🧐 Why SAVILE?

Savile exists to end "prompt drift" and vendor lock-in. Instead of configuring instructions directly inside isolated UIs (like Cursor, Claude Desktop, or V0), you maintain them centrally as pure markdown files.

- **Fork, Modify, Serve:** Treat your agent configurations like open-source software. Fork the baseline logic vault, adapt the QA and Dev personas to your company's standards, and deploy.
- **Universal Portability:** Because Savile exports to the Vercel Labs Skills standard, a customized agent persona can be downloaded into *any* terminal environment instantly.
- **De-anthropomorphized Scale:** Savile enforces strict, functional naming rules (`ux-designer`, `quality-assurance`), ending the chaotic practice of giving AI agents human names and standardizing your robotic workforce.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/mr8lu/savile.git
cd savile
uv sync
```

### 2. The Universal Lifecycle

Savile provides a streamlined lifecycle for managing your agent intelligence.

**`bootstrap`**: Initialize a new SSoT vault or clone an existing one from a remote source. Interactively links your core Method framework.
```bash
uv run savile bootstrap
# Or clone a team vault
uv run savile bootstrap --source git+ssh://github.com/user/my-logic-vault.git
```

**`import`**: Bring logic modules or skills from outside repositories into your local vault.
```bash
uv run savile import git+ssh://github.com/user/remote-logic.git
```

**`import-system`**: Import a custom skill/agent from the system-wide directory (`~/.gemini` or `~/.agents`) or a custom directory into your local vault.
```bash
uv run savile import-system sprint-status
# Or specify a custom source directory
uv run savile import-system custom-skill --dir /path/to/custom_agents
```

**`create`**: Scaffold a new functional agent persona. (Savile strictly enforces non-human, functional naming conventions).
```bash
uv run savile create ux-designer --desc "Analyzes wireframes and user flows"
```

**`update`**: Refresh existing metadata for a persona or framework in your vault.
```bash
uv run savile update ux-designer
```

**`export`**: Compile your raw `personas/` and `frameworks/` down into the universally portable Vercel Labs Skill format (`SKILL.md`), injecting YAML frontmatter automatically.
```bash
# Outputs to dist/skills/
uv run savile export
```

**`serve`**: Boot the local MCP server to dynamically stream your logic vault into IDEs like Cursor, Windsurf, or Claude Desktop.
```bash
uv run savile serve
```

---

## 🛠️ Ecosystem Integrations

### Vercel Labs Skills
By running `savile export`, you generate standard `SKILL.md` artifacts. If you commit these to a public GitHub repository (e.g., your fork of Savile) or deploy them via GitHub Pages, developers anywhere can import your customized agent by running:
```bash
npx skills add <your-username>/savile --skill ux-designer
```

### Model Context Protocol (MCP)
Running `savile serve` exposes your local vault directly to your editor. Changes you make to `personas/ux-designer.md` are instantly available to Claude without requiring a restart.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

*Built with precision for the sovereign developer.*
