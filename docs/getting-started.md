# Getting Started with SAVILE

Welcome to **SAVILE**! This guide will help you set up your local logic vault and connect it to your favorite AI tools like Antigravity, Cursor, and Gemini CLI.

---

## 🚦 Phase 0: The Prerequisite (METHOD-METHOD)

> **Note:** SAVILE is currently tested and supported only on **macOS** and **Linux** platforms. Windows is not officially supported.

SAVILE's built-in personas (like the Architect, Product Manager, or Developer) and workflows rely on the **METHOD Method** ([method-code-org/METHOD-METHOD](https://github.com/method-code-org/METHOD-METHOD)) as their core multi-agent orchestrated framework.

### Option A: Automate (Recommended)
You can automate the installation and linking by running our setup script:
```bash
./scripts/setup-method.sh
```

---

### Option B: Manual Install
Before using SAVILE, you need a local Method installation.

1.  Choose a directory on your machine for your primary Method project workspace.
2.  Install the framework in that directory:
    ```bash
    npx method-method install
    ```
3.  This creates a `.method-core/` directory containing the base agent identities and tasks. *Remember the path to this directory*, as SAVILE will ask for it during initialization (Step 2). SAVILE will link to this directory during setup.

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

During initialization, SAVILE will interactively prompt you for the path to your METHOD installation (from Phase 0). It will create a local symbolic link to connect your vault to the METHOD core logic.

### Option A: Start Fresh
Initialize a brand new local vault with the required folder structure:
```bash
uv run savile init
```

### Option B: Sync from Remote
Already have your prompts in a Git repository? Clone them instantly:
```bash
uv run savile init --source git+ssh://github.com/user/my-logic-vault.git
```

### Need to re-configure later?
If you skipped the prompt or moved your METHOD installation, simply run:
```bash
savile setup
```

---

## 🔌 Step 3: Connect to Your Tools (MCP)

SAVILE uses the **Model Context Protocol (MCP)** to communicate with your tools. You can run the server via standard input/output (stdio) or via Server-Sent Events (SSE) depending on what your agent supports.

You can view the help guide anytime by running:
```bash
./scripts/run-mcp.sh -h
```

### Configuration Guide for AI Agents

To use SAVILE with an MCP-compatible agent or IDE, you need to provide the absolute path to your SAVILE installation. 

**[ Claude Desktop / Antigravity ]**
Add the following to your MCP configuration file (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "savile": {
      "command": "/absolute/path/to/savile/scripts/run-mcp.sh",
      "args": ["/absolute/path/to/savile"]
    }
  }
}
```

**[ Cursor / Windsurf / OpenClaw ]**
Add a new MCP server in the IDE settings:
- **Name**: `savile`
- **Type**: `command` (or `stdio`)
- **Command**: `/absolute/path/to/savile/scripts/run-mcp.sh /absolute/path/to/savile`

**[ Warp AI ]**
Warp requires the server to run over HTTP SSE. 

1. Start the server in your terminal:
   ```bash
   ./scripts/run-mcp.sh /absolute/path/to/savile --sse
   ```
2. In Warp AI settings, enable MCP and add a new server using this JSON config:
   ```json
   {
     "savile": {
       "serverUrl": "http://127.0.0.1:8000/sse"
     }
   }
   ```

### Using Your Vault

Once connected, your personas and frameworks will be available as **MCP Prompts**. 
You can type `/` in your chat interface to see your vault personas (like `/architect` or `/pm`) instantly appear!

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
    uv run savile install-hook
    ```
2.  **Run Evaluation**:
    ```bash
    uv run savile evaluate
    ```

---

## 🚀 Next Steps

Now that you're set up, you can:
*   **Sync**: Run `uv run savile sync` to push your local changes and pull from your remote vault.
*   **Install**: Use the **`install_logic_module`** MCP tool to physically copy logic into a project's `.agent/workflows/` folder.
*   **Contribute**: Help us build the next phase of the protocol, improving remote module installation and version pinning!

*Happy building, sovereign developer!*
