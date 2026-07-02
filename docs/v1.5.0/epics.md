---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ["docs/prd.md", "_bmad-output/planning_artifacts/architecture-v1.5.0.md"]
---

# phantom-celestial - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for phantom-celestial, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Establish a standard directory schema (/personas, /frameworks, /evals, /modules, /shared).
FR2: Support local/remote repository loading using GitPython via 'savile init' and 'savile sync'.
FR3: Wrap the Python 'mcp' filesystem server in the 'typer' CLI via 'savile serve' (stdio and SSE).
FR4: Integrate mathematical evaluation matrix into 'savile evaluate'.
FR5: Enforce pre-push Git hooks to guarantee logic integrity before syncing to a remote origin.
FR6: Implement 'savile add <repo-url>' for remote module installation using Strict 3-Way Merge.
FR7: Implement 'savile.lock' generation (in TOML) for deterministic logic versioning across teams.
FR8: Enforce Schema Validation (Manual PyYAML parsing) to reject invalid modules during 'savile add'.
FR9: Detect v1.0.0 vaults during 'init/sync' and provide a transparent, non-destructive migration ('savile migrate').

### NonFunctional Requirements

NFR1: 100% local execution and data residency. No cloud dependencies for prompt storage.
NFR2: Zero cloud latency for execution (except for LLM evaluations in The Crucible).
NFR3: Deterministic dependency resolution using 'uv'.
NFR4: Fast execution speeds by keeping the daemon lightweight (Manual PyYAML instead of Pydantic).
NFR5: 'savile add' must prevent path traversal and arbitrary file writes outside the vault directory.
NFR6: Stdio transport relies strictly on local user execution context for security.

### Additional Requirements

- MUST use pathlib.Path exclusively. Absolute paths are forbidden.
- CLI Entrypoints (src/savile/cli.py) MUST be synchronous 'def'.
- MCP Handlers (src/savile/mcp_server.py) MUST be asynchronous 'async def'.
- Boundary bridging uses 'asyncio.run()' only at the topmost CLI command level.
- MUST use GitPython for state management; 'subprocess' is ONLY for The Crucible.
- User output MUST use typer.echo/secho. Raw tracebacks are forbidden; raise 'typer.Exit(code=1)'.
- The schema parser uses 'yaml.safe_load_all()' to isolate frontmatter from body text.
- Must include user-friendly error boundaries when GitPython encounters authentication failures.
- **First Implementation Priority:** Develop the Vault Migration Script ('savile migrate') to scaffold '.savile/vault.toml' and the 'modules/' directory.

### UX Design Requirements

UX-DR1: The CLI output for 'savile add' must clearly log which remote schemas passed or failed PyYAML validation using typer red/green colorization.
UX-DR2: The 'savile sync' command must explicitly warn the user if a Git conflict forces a manual merge resolution.

### FR Coverage Map

FR1: Epic 1
FR6: Epic 2
FR7: Epic 2
FR8: Epic 1
FR9: Epic 1
UX-DR1: Epic 2
UX-DR2: Epic 2

## Epic List

### Epic 1: The Sovereign Vault Migration & Schema Stabilization
**Goal:** Safely upgrade v1.0.0 vaults to v1.5.0 and enforce strict PyYAML validation.
**FRs covered:** FR1, FR8, FR9

### Epic 2: The Package Manager for Intelligence (savile add & savile.lock)
**Goal:** Pull peer-reviewed logic via Strict 3-Way Merge and generate TOML lockfiles.
**FRs covered:** FR2, FR6, FR7

## Epic 1: The Sovereign Vault Migration & Schema Stabilization
**Goal:** Safely upgrade v1.0.0 vaults to v1.5.0 and enforce strict PyYAML validation.

### Story 1.1: Strict PyYAML Schema Validator
As a system daemon,
I want to parse markdown files using 'yaml.safe_load_all' to extract and validate frontmatter,
So that I can reject invalid logic modules (missing name, version, category) before they are executed or shared.

**Acceptance Criteria:**

**Given** a valid markdown file with YAML frontmatter containing 'name', 'version', and 'category'
**When** the schema parser reads the file
**Then** it successfully returns a structured dictionary and the remaining body text
**And** uses 'pathlib.Path' exclusively.

**Given** a markdown file missing the 'version' key
**When** the schema parser reads the file
**Then** it raises a custom 'SchemaValidationError' with a clear message.

### Story 1.2: The 'savile migrate' Command
As a current v1.0.0 user,
I want to run a migration command to upgrade my flat vault to the v1.5.0 Hierarchical Schema,
So that my local personas are protected while I gain the ability to install external modules safely.

**Acceptance Criteria:**

**Given** an existing v1.0.0 vault containing only '/personas' and '/frameworks'
**When** the user executes 'savile migrate'
**Then** the command creates the '/modules', '/shared/snippets', and '/.savile' directories
**And** generates a default '.savile/vault.toml' file without altering the existing personas or frameworks
**And** uses synchronous 'def' CLI handlers and 'typer.secho' for user output.

### Story 1.3: Migration Detection Interceptor
As a system daemon,
I want to detect outdated vaults during 'init' and 'sync',
So that I can block operations and prompt the user to run 'savile migrate' before they break their repository state.

**Acceptance Criteria:**

**Given** a user running 'savile sync' in a vault missing the '.savile/vault.toml' file
**When** the command initializes
**Then** it halts execution
**And** raises a 'typer.Exit(code=1)' error with the message "Legacy vault detected. Please run 'savile migrate' first."


## Epic 2: The Package Manager for Intelligence ('savile add' & 'savile.lock')
**Goal:** Developers can pull peer-reviewed agent logic from remote Git repositories directly into their local vault ('savile add'), and teams are guaranteed to be using the exact same logic versions thanks to the deterministic lockfile ('savile.lock').

### Story 2.1: The TOML Lockfile Generator ('savile.lock')
As a team lead,
I want SAVILE to parse the vault and generate a deterministic TOML lockfile of all local and external modules,
So that my entire team is guaranteed to be running the exact same versions of prompts and frameworks.

**Acceptance Criteria:**

**Given** a valid v1.5.0 vault containing 'personas' and 'modules'
**When** the user runs 'savile lock'
**Then** a 'savile.lock' file is generated in TOML format
**And** it lists every module's 'name', 'version', and 'source_url' (if applicable) extracted from the YAML frontmatter.

### Story 2.2: The 'savile add' GitPython Sync Engine
As a developer,
I want to fetch remote logic modules into a local '.savile/cache' directory using 'GitPython',
So that I can retrieve external personas securely without immediately polluting my active workspace.

**Acceptance Criteria:**

**Given** a valid Git SSH/HTTPS URL
**When** the user runs 'savile add <repo-url>'
**Then** the sync engine clones the repository into '.savile/cache/<org>/<repo>' using 'GitPython'
**And** prevents path traversal exploits by ensuring the clone destination strictly resides within the vault.
**And** provides user-friendly output ('typer.secho') if a Git authentication failure occurs instead of a raw traceback.

### Story 2.3: Module Validation & Strict 3-Way Merge
As a developer,
I want the system to validate the remote modules in the cache and safely merge them into the active 'modules/' directory,
So that I only install safe, valid schemas while preserving my existing logic.

**Acceptance Criteria:**

**Given** a cloned repository in '.savile/cache'
**When** the sync engine prepares the merge
**Then** it runs the PyYAML Schema Validator (from Story 1.1) on every '.md' file
**And** outputs pass/fail status using red/green 'typer' colorization (UX-DR1)
**And** if all validations pass, performs a Strict 3-Way Merge moving the files into the 'modules/<org>/<repo>' directory
**And** if a Git conflict forces a manual merge resolution, explicitly warns the user via 'typer.secho' (UX-DR2).

### Story 2.4: MCP Server Lockfile Resolution
As a connected IDE client,
I want the MCP Bridge to parse the 'savile.lock' file on startup to define its Prompts and Tools,
So that the IDE only sees the deterministic, validated logic versions defined by the team.

**Acceptance Criteria:**

**Given** a valid 'savile.lock' file
**When** the MCP Server ('src/savile/mcp_server.py') starts asynchronously
**Then** it reads the lockfile instead of performing a raw directory crawl
**And** exposes the locked personas as MCP Prompts
**And** uses 'asyncio.run()' only at the topmost CLI boundary.

