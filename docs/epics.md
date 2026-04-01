---
stepsCompleted: ["v1.0.0-completion"]
inputDocuments: ["docs/prd.md"]
---

# SAVILE - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for SAVILE, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Local-first execution using Python 3.11+ and asyncio.
FR2: Standardized Registry Core with /personas, /frameworks, and /evals directories.
FR3: Git-native State Manager for bidirectional sync (local and remote URIs).
FR4: Lightweight Python CLI (Typer-based) supporting `init`, `sync`, `serve`, and `evaluate`.
FR5: MCP Bridge to expose the vault to IDEs (e.g., Antigravity).
FR6: Evaluation loop (Crucible) for logical threshold verification.

### NonFunctional Requirements

NFR1: Privacy: 100% local residency for logic and execution.
NFR2: Portability: Git-driven distributed state management.
NFR3: High Performance: Asynchronous MCP server logic.
NFR4: Low Dependency: Minimal dependencies (typer, pyyaml, GitPython).

### Additional Requirements

- Registry Core structure: `/personas`, `/frameworks`, `/evals`.
- Global configuration at `~/.savile/config.yaml`.
- Integration with `gemini-2.0-pro-exp` for evaluation.

### UX Design Requirements

N/A (SAVILE is a CLI-first, non-performative tool).

### FR Coverage Map

FR1: Epic 1 - The Registry Core & Local CLI
FR2: Epic 1 - The Registry Core & Local CLI
FR3: Epic 2 - Portable Logic (Git-Native Sync)
FR4: Epic 1 (init, serve), Epic 2 (sync), Epic 4 (evaluate)
FR5: Epic 3 - The MCP Bridge (IDE Integration)
FR6: Epic 4 - The Crucible (Execution Logic & Evals)

## Epic List

### Epic 1: The Registry Core & Local CLI (Status: COMPLETED ✅)
**Goal:** Users can initialize a local vault and manage their personas/frameworks via the Typer CLI utilizing local execution with asyncio.
- **Story 1.1:** Standardize directory schema and scaffolding. [DONE]
- **Story 1.2:** Implement Typer CLI for `init` and vault management. [DONE]
- **Story 1.3:** Setup basic async runner for local execution. [DONE]

### Epic 2: Portable Logic (Git-Native Sync) (Status: COMPLETED ✅)
**Goal:** Users can sync their logic vaults across multiple devices and teams using Git-native operations and the `savile sync` CLI command.
- **Story 2.1:** Integrate GitPython for repository cloning and sync. [DONE]
- **Story 2.2:** Implement bidirectional sync logic in `savile sync`. [DONE]
- **Story 2.3:** Support local and remote Git URIs. [DONE]

### Epic 3: The MCP Bridge (IDE Integration) (Status: COMPLETED ✅)
**Goal:** Users can broadcast their version-controlled logic directly to their IDEs (Antigravity/Cursor) via standard stdio or SSE MCP endpoints.
- **Story 3.1:** Implement basic MCP server with tool support (list/read modules). [DONE]
- **Story 3.2:** Broadcast logic modules as **MCP Prompts** for slash-command integration. [DONE]
- **Story 3.3:** Implement `install_logic_module` tool with **Gemini CLI TOML** generation. [DONE]
- **Story 3.4:** Add `--vault` flag to `serve` command for flexible vault positioning. [DONE]

### Epic 4: The Crucible (Execution Logic & Evals) (Status: COMPLETED ✅)
**Goal:** Users can mathematically validate their logic against thresholds using YAML-based tests in `/evals`.
- **Story 4.1:** Implement `savile evaluate` runner for YAML assertions. [DONE]
- **Story 4.2:** Automated **Git pre-push hook** installation to block invalid commits. [DONE]
- **Story 4.3:** CLI command `install-hook` for manual setup. [DONE]

### Epic 5: The Protocol (Remote Modules) (Status: REFINED 🎯)
**Goal:** Establish the open-source registry for sharing deterministic logic modules.
- **Story 5.1: Logic Module Metadata Schema (Prerequisite)**
  - **Why?** Standardize how modules define their identity (Persona vs. Framework) and metadata.
  - **Acceptance Criteria:**
    - [ ] Define Frontmatter/YAML schema (name, version, category, description).
    - [ ] Support for dependencies (e.g., framework X requires persona Y).
- **Story 5.2: The `savile add` Command**
  - **Why?** Enable users to pull logic from remote repositories or local paths.
  - **Acceptance Criteria:**
    - [ ] Command: `savile add <repo-url> [--alias name]`.
    - [ ] Clone remote, validate schema, and merge into local vault.
    - [ ] Reject modules with invalid paths or missing metadata.
- **Story 5.3: Conflict Resolution & Versioning**
  - **Why?** Manage name collisions and remote updates without breaking local logic.
  - **Acceptance Criteria:**
    - [ ] Implement `savile sync --dry-run` to preview remote changes.
    - [ ] Basic version pinning in a local manifest/lock file.
    - [ ] User prompt/warning if an `add` would overwrite existing local files.
