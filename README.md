# SAVILE (System for Agentic Versioning, Intelligence, and Logical Evaluation)

**SAVILE** is an agnostic, local-first framework rooted in the Model Context Protocol (MCP). It establishes a high-fidelity protocol for storing, versioning, syncing, and evaluating AI agent skills, written strictly in Python.

## The Core Philosophy

*   **Anti-performative software:** No web UI, no cloud lock-in. A bare-metal architecture designed to outlive transient SaaS abstractions.
*   **Deterministic Logic Distribution:** Using Python—the native runtime of the AI infrastructure layer—to strip away web-centric bloat and provide a deterministic framework for system feedback.
*   **Git-native State:** Intelligence must not be tethered to a single host machine. Git is the engine for distributed, version-controlled state.

## Core Mechanics

SAVILE operates as a local Python daemon, bridging version-controlled text files and IDE agent runners (such as Antigravity, Cursor, and Claude Code). It enforces a strict separation of concerns between prompt logic, evaluation, and IDE execution.

### The Registry Core
A standardized directory structure that defines the **Logic Vault**:
- `/personas`: System-level constraints and operational parameters.
- `/frameworks`: Actionable logic chains and PRD structures.
- `/evals`: YAML-based assertions for matrix evaluation.

### The State Manager
A Git-native sync engine that allows you to mount logic vaults from local paths (`file://`) or remote repositories (`git+ssh://` or `git+https://`).

### The MCP Bridge
A lightweight Python CLI (`savile`) utilizing the MCP server SDK to expose the loaded vault to any active IDE.

### The Crucible (Eval)
A sub-process evaluation loop. A skill is only exposed to the MCP endpoint if it mathematically passes its predefined logical thresholds in `/evals`.

---

## Technical Specifications

- **Runtime:** Python 3.11+ (leveraging `asyncio` for high-performance streaming).
- **Dependencies:** `mcp`, `typer`, `pyyaml`, `GitPython`, `pytest`.
- **Data Residency:** 100% Local execution. Perfectly suited for strict enterprise environments.

## Getting Started

### Installation

```bash
# In the project directory
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Basic Commands

1. **Initialize a Logic Vault:**
   ```bash
   savile init --source git+ssh://github.com/user/logic-vault.git
   ```
   This clones the repository and structures the local cache.

2. **Run the MCP Bridge:**
   ```bash
   savile serve
   ```
   The daemon binds to the local MCP port, providing your IDE with synchronized, versioned logic.

3. **Evaluate Your Logic:**
   ```bash
   savile evaluate
   ```
   Runs the evaluation matrix against your logic changes.

---

## Development Milestones

- **v0.1.0 (The Infrastructure):** Current state. Core CLI, Git sync engine, and basic MCP bridge implementation.
- **v0.2.0 (The Crucible):** Full integration of the evaluation matrix into the `savile evaluate` command.
- **v0.3.0 (The Protocol):** Open-source registry for sharing deterministic logic modules.

## LICENSE

MIT License. See [LICENSE](LICENSE) for details.
