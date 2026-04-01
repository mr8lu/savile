# SAVILE: Git-Native Prompt Versioning & MCP Server for AI Agents

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/ "Python 3.11+ Version Support")
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/ "Model Context Protocol Standard Compliance")
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/mr8lu/savile/blob/main/LICENSE "MIT License")

**SAVILE** (System for Agentic Versioning, Intelligence, and Logical Evaluation) provides robust **Git-Native Prompt Versioning** and functions as a secure **MCP Server for AI Agents**. It is a high-fidelity, local-first protocol for storing, versioning, syncing, and evaluating your AI agent prompts and skills via the **Model Context Protocol (MCP)**.

Built as a Git-native logic bridge, SAVILE ensures reproducibility and version control for your agentic workflows, connecting your version-controlled logic directly to AI execution environments like **Antigravity**, **Cursor**, and **Claude Code**.

---

## 🧐 Why SAVILE?

Modern AI development is plagued by opaque UI abstractions and "prompt drift." SAVILE treats your agent's "brain"—its **personas**, **frameworks**, and **evaluations**—as first-class code artifacts. By providing a **Git-based prompt management** system, SAVILE enables:

*   **Anti-Performative Software**: No web UI, no cloud lock-in. 100% local residency for logic and execution.
*   **Git-Native State**: Your intelligence isn't tethered to a single machine. Sync your logic vaults across teams using fundamental Git primitives for **collaborative AI development**.
*   **Deterministic Evaluation**: The **Crucible** ensures your logic actually works before you push it. If an assertion fails, the commit is rejected, ensuring **prompt reliability**.

---

## ✨ Key Features

*   **MCP Server (Python)**: Seamlessly broadcast your logic vault as dynamic MCP Prompts and Tools.
*   **Git-Native Logic Storage**: Use Git for versioning and syncing your agent's personas and frameworks.
*   **Local-First Architecture**: Keep your prompts and logic secure on your local machine.
*   **Automated Evaluation (The Crucible)**: Mathematical grading of your logic against predefined thresholds.
*   **Sovereign Development**: Build AI agent infrastructure without vendor lock-in.

---

## 🏗️ System Architecture

> **Deep Dive**: For a comprehensive look at SAVILE's implementation, methodology, and design concepts, read our [Technical Explanation](docs/explanation.md).

SAVILE acts as a deterministic "Logic Router" that brings versioned clarity to the AI infrastructure layer.

---

## 🚀 Quick Start

### 0. Pre-requisites

> **Note:** SAVILE is currently tested and supported only on **macOS** and **Linux** platforms. Windows is not officially supported.

SAVILE's built-in personas and workflows rely on the **BMAD Method** ([bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)) as its underlying multi-agent orchestrated framework.

You can automate this installation and linkage by running:
```bash
./scripts/setup-bmad.sh
```

**OR (Manual Install)**
You will need a local BMad installation to serve as the core intelligence engine:
```bash
# In your main development workspace or a dedicated directory
npx bmad-method install
```

### 1. Installation
```bash
# Clone and install locally
git clone https://github.com/mr8lu/savile.git
cd savile
uv sync
```

> **Tip:** After `uv sync`, you must prefix commands with `uv run` (e.g., `uv run savile --help`). Alternatively, you can activate the environment with `source .venv/bin/activate` or install it globally with `uv tool install .`.

### 2. Initialize a Vault
Scaffold a new local vault or clone an existing one from a remote origin.
```bash
# Initialize a brand new local vault
uv run savile init

# OR Initialize from a remote Git repository
uv run savile init --source git+ssh://github.com/user/my-logic-vault.git
```

### 3. Connect to Your Tools (MCP)
SAVILE is an MCP-compatible server. Use the provided runner script to connect to your preferred AI environment:

```bash
./scripts/run-mcp.sh -h
```

### 4. Pull Remote Modules
Add deterministic logic from external sources.
```bash
uv run savile add git+ssh://github.com/user/remote-logic.git
```

### 5. Enforce Quality
Install the pre-push Git hook to ensure your logic passes **The Crucible** evaluations before syncing.
```bash
uv run savile install-hook
```

---

## 🛠️ Core Components

### The [Registry Core](docs/architecture.md#3-directory-structure)
A standardized directory structure for your intelligence. Every persona and framework is a Markdown file with mandatory **YAML Frontmatter** for metadata tracking.

### The [State Manager](docs/architecture.md#22-the-state-manager-gitpython)
Powered by `GitPython`, handling bidirectional synchronization between your local environment and remote logic origins.

### The [MCP Bridge](docs/architecture.md#23-the-mcp-bridge-mcp-sdk)
Exposes your vault as **MCP Prompts** (for dynamic slash-command integration) and **Tools** (for physical file installation into `.agent/` or `.gemini/` directories).

### The [Crucible](docs/architecture.md#24-the-crucible-pyyaml-subprocess-pytest)
A validation loop that mathematically grades your logic against predefined thresholds in `/evals`.

---

## 🗺️ Roadmap

- **v0.1.0 (Infrastructure)**: ✅ Registry Core, Git sync, and basic MCP bridge.
- **v0.2.0 (The Crucible)**: ✅ Git hook integration, MCP Prompts, and Gemini CLI command generation.
- **v1.0.0 (Stable Protocol)**: ✅ MCP bridge (stdio & SSE), remote module installation (`savile add`), and metadata validation.
- **v1.1.0 (The Ecosystem)**: 🚀 Community registry and automated version pinning.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

*Built with precision for the sovereign developer.*
