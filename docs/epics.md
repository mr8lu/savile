---
stepsCompleted: []
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

### Epic 1: The Registry Core & Local CLI
**Goal:** Users can initialize a local vault and manage their personas/frameworks via the Typer CLI utilizing local execution with asyncio.
**FRs covered:** FR1, FR2, FR4 (initial)

### Epic 2: Portable Logic (Git-Native Sync)
**Goal:** Users can sync their logic vaults across multiple devices and teams using Git-native operations and the `savile sync` CLI command.
**FRs covered:** FR3, FR4 (sync)

### Epic 3: The MCP Bridge (IDE Integration)
**Goal:** Users can broadcast their version-controlled logic directly to their IDEs (Antigravity/Cursor) via standard stdio or SSE MCP endpoints.
**FRs covered:** FR5, FR4 (serve)

### Epic 4: The Crucible (Execution Logic & Evals)
**Goal:** Users can mathematically validate their logic against thresholds using YAML-based tests in `/evals`. These tests use mock inputs to grade personas/frameworks against models like `gemini-2.0-pro-exp` to block invalid commits.
**FRs covered:** FR6, FR4 (evaluate)
