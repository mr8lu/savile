# Project Analysis: SAVILE
*System for Agentic Versioning, Intelligence, and Logical Evaluation*

## 1. Executive Overview
SAVILE is a high-fidelity, local-first protocol designed to bridge the gap between version-controlled AI logic (stored in Git) and the real-time execution environments of AI agents (IDEs and CLIs). It treats prompts, personas, and frameworks as first-class code artifacts, complete with metadata, validation, and automated synchronization.

## 2. System Architecture
Think of SAVILE as the "Logic Router" for your AI stack. It ensures that the same "brain" (persona) you use in your IDE is the same one used by your CLI tools, all while keeping a perfect history in Git.

```mermaid
graph TD
    subgraph "Global Logic Vault (Git Repository)"
        V_P[personas/*.md]
        V_F[frameworks/*.md]
        V_E[evals/*.yaml]
    end

    subgraph "SAVILE Daemon (Local Host)"
        CLI[SAVILE CLI]
        SYNC[State Manager: GitPython]
        MCP[MCP Bridge: Prompts & Tools]
        CRU[The Crucible: Evaluation Runner]
    end

    subgraph "Clients (IDE / CLI)"
        AG[Antigravity / Cursor]
        GCLI[Gemini CLI / Claude Code]
        LOC_A[.agent/workflows/]
        LOC_G[.gemini/commands/]
    end

    V_P --> SYNC
    V_F --> SYNC
    SYNC --> MCP
    MCP -- "Prompts (Slash Commands)" --> AG
    MCP -- "install_logic_module" --> LOC_A
    MCP -- "install_logic_module" --> LOC_G
    LOC_G --> GCLI
    CRU -- "pre-push hook" --> V_P
```

## 3. Core Components

### 3.1 The Registry Core (The Brain)
The vault uses a standardized directory structure. Every module is a Markdown file enhanced with **YAML Frontmatter Metadata**.
*   **Location**: `/personas`, `/frameworks`, `/evals`.
*   **Standards**: Winston's Metadata Schema (v1.0.0) ensures every module declares its name, version, and dependencies.

### 3.2 The State Manager (The Heart)
Powered by `GitPython`, this component handles bidirectional synchronization.
*   **Git-Native**: Inherits branching, merging, and history for free.
*   **Safety**: Integrated `pre-push` hooks ensure no "broken" logic (failing evaluations) ever leaves the local machine.

### 3.3 The MCP Bridge (The Voice)
The Model Context Protocol (MCP) implementation that exposes the vault to the world.
*   **Zero-Install (Prompts)**: Dynamic broadcasting of vault modules as slash-commands (e.g., `/architect`).
*   **Physical-Install (Tools)**: The `install_logic_module` tool bootstraps local project directories for tools like Gemini CLI.

### 3.4 The Crucible (The Gatekeeper)
A validation runner that enforces both structural integrity (metadata checks) and logical density (LLM-graded assertions).

## 4. Implementation Status (v1.0.0)
As of April 1, 2026, SAVILE has successfully achieved its v1.0.0 Stable Protocol release:
- [x] Full Git-native sync engine.
- [x] MCP Prompt & Tool implementation.
- [x] Automated Gemini CLI command generation.
- [x] Built-in vault with 9 BMad core agents.
- [x] Pre-push evaluation hooks.
- [x] Automated BMAD pre-requisite linking and initialization scripting.
- [x] Adversarial security hardening for the MCP Server.
- [x] E2E CLI test suite and robust exception handling.
- [x] **Stable Protocol (`savile add`)**: Pulling remote logic modules into local vaults.
- [x] **Metadata Schema**: Winston's v1.0.0 YAML frontmatter validation.
- [x] **Documentation Hub**: MkDocs Material site with automated GitHub Pages deployment.

## 5. Next Horizon: v1.1.0 The Ecosystem
The next phase focuses on expanding the network effect and community tooling:
*   **`savile.lock`**: Deterministic version pinning for team collaboration.
*   **Community Registry**: A centralized or federated index of open-source logic modules.
*   **Advanced Conflict Resolution**: Smarter merging and aliasing when pulling remote modules with overlapping names.
