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

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies and the CLI
pip install -e .
```

Verify the installation by running:
```bash
savile --help
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

## 🔌 Step 3: Connect to Your IDE

SAVILE uses the **Model Context Protocol (MCP)** to communicate with your tools. When you run the `serve` command, it starts an MCP server.

```bash
savile serve
```

### In Your IDE (e.g., Antigravity or Cursor):
1.  **Configure MCP**: Point your IDE's MCP configuration to the SAVILE `stdio` endpoint.
2.  **Use Slash-Commands**: Because SAVILE broadcasts your vault as **MCP Prompts**, you can simply type `/` in your IDE chat to see your personas (like `/architect` or `/pm`) instantly appear!

---

## 🧠 Step 4: Your First Persona

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
