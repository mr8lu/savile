# Getting Started with SAVILE

Welcome to **SAVILE**! This guide will help you set up your local logic vault and connect it to your favorite AI tools like Antigravity, Cursor, and Gemini CLI.

---

## 🚦 Phase 0: The Prerequisite (BMAD-METHOD)

> **Note:** SAVILE is currently tested and supported only on **macOS** and **Linux** platforms. Windows is not officially supported.

SAVILE's built-in personas (like the Architect, Product Manager, or Developer) and workflows rely on the **BMAD Method** ([bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)) as their core multi-agent orchestrated framework.

### Option A: Automate (Recommended)
You can automate the installation and linking by running our setup script:
```bash
./scripts/setup-bmad.sh
```

---

### Option B: Manual Install
Before using SAVILE, you need a local BMad installation.

1.  Choose a directory on your machine for your primary BMad project workspace.
2.  Install the framework in that directory:
    ```bash
    npx bmad-method install
    ```
3.  This creates a `.bmad-core/` directory containing the base agent identities and tasks. SAVILE will link to this directory during setup.

---

## 🏗️ Step 1: Installation

SAVILE is a local Python daemon. First, let's get it installed on your machine.

```bash
# Clone the repository
git clone git@github.com:mr8lu/savile.git
cd savile

# Sync the virtual environment and install the CLI using uv
uv sync
```

Verify the installation by running:
```bash
uv run savile --help
```

---

## 🗄️ Step 2: Initialize Your Logic Vault

A **Logic Vault** is just a directory (backed by Git) that stores your personas, frameworks, and evaluation matrices. You can start fresh or sync from an existing repository.

### Option A: Start Fresh
Initialize a brand new local vault with the required folder structure:
```bash
savile init
```

### Option B: Sync from Remote
Already have your prompts in a Git repository? Clone them instantly:
```bash
savile init --source git+ssh://github.com/user/my-logic-vault.git
```

---

## 🔌 Step 3: Connect to Your Tools (MCP)

SAVILE uses the **Model Context Protocol (MCP)** to communicate with your tools. Use the provided runner script to get the exact configuration for your environment:

```bash
./scripts/run-mcp.sh -h
```

### In Your Tool (e.g., Warp, Antigravity, or Cursor):
1.  **Enable MCP**: Turn on MCP support in your tool's settings.
2.  **Add Server**: Use the absolute path to `scripts/run-mcp.sh` as the command.
3.  **Use Slash-Commands**: Once connected, you can type `/` in your chat interface to see your vault personas (like `/architect` or `/pm`) instantly appear!

---

## 🧠 Step 4: Your First Persona (Gemini CLI Support)

When you are in **Gemini CLI** (this terminal), SAVILE can automatically generate local commands for you:

1. Use the **`install_logic_module`** tool from the SAVILE MCP server.
2. It will physically copy the persona and generate a `.toml` file in `.gemini/commands/`.
3. You can then use the persona as a regular command, like `savile /architect "my message"`.

Let's create a custom "Persona" for your vault first:
...
Let's create a custom "Persona" for your vault. A persona is a Markdown file with mandatory **YAML Frontmatter** metadata.

1. Create a file at `personas/realist.md`:
```yaml
---
name: "realist"
version: "1.0.0"
category: "persona"
description: "A pragmatic and skeptical persona."
---

# Realist Persona
You are a pragmatic, skeptical senior architect. You cut through the fluff and look for technical debt and hidden risks in every architecture.
```

2. Once saved, it will **instantly** be available in your IDE via the `/realist` slash-command.

---

## ⚖️ Step 5: Safety with The Crucible

Before you share your logic with your team, you should ensure it actually works. The **Crucible** is SAVILE's automated evaluation gate.

1.  **Install the Git Hook**: This ensures your logic passes evaluations before you are allowed to `git push`.
    ```bash
    savile install-hook
    ```
2.  **Run Evaluation**:
    ```bash
    savile evaluate
    ```

---

## 🚀 Next Steps

Now that you're set up, you can:
*   **Sync**: Run `savile sync` to push your local changes and pull from your remote vault.
*   **Install**: Use the **`install_logic_module`** MCP tool to physically copy logic into a project's `.agent/workflows/` folder.
*   **Contribute**: Help us build the next phase of the protocol in **v0.3.0**!

*Happy building, sovereign developer!*
