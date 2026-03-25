# Product Requirements Document: SAVILE
*System for Agentic Versioning, Intelligence, and Logical Evaluation*

## 1. Executive Summary

### 1.1 Objective
Establish a high-fidelity, tool-agnostic protocol for storing, versioning, syncing, and evaluating AI agent skills via the Model Context Protocol (MCP), written strictly in Python. 

### 1.2 Product Philosophy
**Anti-performative software.** No web UI. No cloud lock-in. A bare-metal, dependency-minimized architecture designed to outlive transient SaaS abstractions. We rely on fundamental computing primitives: Git for state management, Markdown/YAML for schema, and local Python execution for data privacy and compute efficiency.

### 1.3 The Problem
The current paradigm of agentic prompt management relies heavily on opaque UI abstractions that sever developers from the model's underlying logic. Tools like Antigravity, Cursor, and Claude Code require localized context, but managing them individually results in state drift. A systems-thinker does not tolerate disparate tool-specific configurations.

### 1.4 The Solution
An agnostic, local-first architecture rooted in MCP. By shifting execution to Python—the native runtime of AI infrastructure—we strip away the web-centric bloat and build a deterministic framework for system feedback and logic distribution.

---

## 2. Core Mechanics & Architecture

SAVILE operates as a local Python daemon bridging version-controlled text files and IDE agent runners. It enforces a strict separation of concerns between prompt logic, evaluation, and IDE execution.

### 2.1 The Registry Core (Vault Schema)
A standardized, file-system-level directory structure isolated from the execution environment:
* `/personas`: System-level constraints and operational parameters (e.g., `systems_realist.md`). The baseline operational logic.
* `/frameworks`: Actionable logic chains and PRD structures (e.g., `system_architecture_review.md`).
* `/evals`: YAML-based assertion matrices used by The Crucible. These files define mock inputs, target models (e.g., `gemini-2.0-pro-exp`), and expected logical thresholds to grade the performance of personas or frameworks. If an assertion fails during `savile evaluate`, the system rejects the code change.

### 2.2 The State Manager (Sync Engine)
A Git-native sync engine supporting bidirectional syncing.
* Managed via a global `~/.savile/config.yaml`.
* Fetches the latest state from designated Git repositories (via `savile sync`), ensuring the logic vault is perfectly mirrored across work, home, and cloud environments.
* Supports both local (`file://`) and remote (`git+ssh://` or `git+https://`) URIs.

### 2.3 The MCP Bridge (Daemon)
A lightweight Python CLI (`savile`) leveraging the official MCP server SDK.
* Mounts the synchronized vault.
* Broadcasts capabilities via standard `stdio` or `SSE` endpoints to connected IDE tools.

### 2.4 The Crucible (Evaluation Loop)
Logic without system feedback is just idealism.
* Run via `savile evaluate`.
* Uses a strict matrix test. If a framework modification fails predefined logical density thresholds (e.g., against `gemini-2.0-pro-exp`), the commit is rejected.

---

## 3. Technical Specifications

* **Runtime:** Python 3.11+ (leveraging `asyncio` for MCP streaming).
* **Dependencies:** `mcp` (official SDK), `typer` (CLI routing), `pyyaml` (schema parsing), `GitPython` (repository syncing), `pytest` (or native subprocess evaluator).
* **Data Residency:** 100% local execution. The vault sits on the host machine; the IDE reaches in. Perfect isolation for strict enterprise environments.

---

## 4. Execution Flow
*The user experience adheres to the Unix philosophy—do one thing, do it deterministically.*

1. **Initialize:** User runs `savile init --source git+ssh://github.com/user/logic-vault.git`. The system clones the repository and structures the local cache.
2. **Edit:** User modifies constraints locally (e.g., in `/personas/realist.md`).
3. **Serve:** User runs `savile serve`. The daemon binds to the local MCP port, ensuring IDEs always access the most recently synced state.
4. **Consume:** In the IDE, the user prompts: *"@savile Use the realist persona to critique this architecture."*
5. **Execute:** The agent pulls unadulterated, version-controlled text directly from the MCP server and executes.

---

## 5. Development Milestones

### v0.1.0: The Infrastructure
* Standardize the directory schema (`personas`, `frameworks`, `evals`).
* Integrate `GitPython` for local/remote repository loading.
* Wrap the Python `mcp` filesystem server in the `typer` CLI.

### v0.2.0: The Crucible
* Integrate the evaluation matrix directly into the `savile evaluate` command.
* Enforce pre-push Git hooks to guarantee logic integrity before syncing to a remote origin.

### v0.3.0: The Protocol
* Establish the open-source registry for sharing deterministic logic modules.
* Enable remote module installation (e.g., `savile add https://github.com/org/system-architecture-frameworks.git`).
