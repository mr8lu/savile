---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: ["docs/prd.md", "docs/architecture.md", "docs/project-analysis.md", "_bmad-output/planning_artifacts/research/market-sovereign-logic-infrastructure-research-2026-03-31.md"]
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-03-31'
project_name: 'phantom-celestial'
user_name: 'Danipan'
date: '2026-03-31'
---

# Architecture Decision Document (v1.5.0)

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
- Implement 'savile add' for remote module installation.
- Implement 'savile.lock' for deterministic logic versioning across teams.
- Enhance Schema Validation to enforce the new metadata standards strictly.

**Non-Functional Requirements:**
- Must remain 100% local-first and execute without cloud latency (except for explicit LLM evaluations in The Crucible).
- Must resolve dependencies deterministically using 'uv'.
- Must prevent path traversal and arbitrary file writes during module installation.

**Scale & Complexity:**
- Primary domain: Python Daemon / MCP Protocol
- Complexity level: Medium/High
- Estimated architectural components: 3 (Registry Parser, Lockfile Generator, Remote Sync Engine)

### Technical Constraints & Dependencies

- Must use 'GitPython' for state management.
- Must use the official 'mcp' Python SDK.
- Relies on 'typer' for CLI routing.

### Cross-Cutting Concerns Identified

- **Security Boundaries:** Ensuring 'savile add' cannot pull malicious code or overwrite core system files.
- **State Consistency:** Ensuring the 'savile.lock' file accurately reflects the Git state without desyncing during merge conflicts.


## Starter Template Evaluation (v1.5.0 Infrastructure)

### Primary Technology Domain
CLI Tool / MCP Daemon based on existing SAVILE Python 3.11+ architecture.

### Starter Options Considered
- **Standard Git-Native Sync**: Leveraging 'GitPython' for all remote logic fetching.
- **HTTP/Registry Sync**: Implementing a custom 'httpx' client for a centralized logic registry.

### Selected Pattern: Git-Native Distribution
**Rationale for Selection:**
Aligns with the 'Sovereign Logic' and 'Local-First' philosophy. Git provides versioning, integrity, and transport for free.

**Initialization Command (Internal):**
```bash
uv add httpx gitpython
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
Python 3.11+ with 'asyncio' to maintain high-performance MCP streaming.

**Dependency Management:**
'uv' with 'pyproject.toml' and 'uv.lock'.

**Lockfile Strategy:**
Implement 'savile.lock' in **TOML** format to maintain parity with the Python ecosystem and provide human-readable diffs.

**Testing Setup:**
Continue utilizing 'pytest' for unit/integration tests and 'The Crucible' for prompt logic validation.


## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- **Remote Module Installation Strategy:** Strict 3-Way Merge (Git-Native)
- **Schema Validation Engine:** Manual PyYAML Parsing

**Important Decisions (Shape Architecture):**
- **Lockfile Format:** TOML (Savile.lock)
- **Sync Transport:** Git over SSH/HTTPS (GitPython)

**Deferred Decisions (Post-MVP):**
- **Namespaced Module Isolation:** Deferred for a future release to keep the initial 'savile add' workflow simple and directly integrated with the root '/personas' and '/frameworks' directories.

### Data Architecture (The Logic Vault)

- **Storage Medium:** Local File System (Markdown + YAML Frontmatter)
- **State Management:** Git Repository (Bidirectional Sync)
- **Validation:** Strict Manual PyYAML parsing to enforce the v1.5.0 Schema (name, version, category, dependencies) upon file read and 'savile add'.

### Authentication & Security

- **Remote Sync Auth:** Delegates entirely to the host's local SSH agent or Git credential helper. SAVILE will not manage or store credentials.
- **MCP Security:** Stdio transport relies on local user execution context. Path traversal protections must be strictly enforced during 'savile add' to prevent malicious repositories from escaping the vault directory.

### API & Communication Patterns

- **IDE Integration:** Official Model Context Protocol (MCP) using the Python SDK.
- **Transport Layers:** Stdio (default for Cursor/Claude) and SSE (Server-Sent Events via Starlette/Uvicorn for Warp AI).
- **Module Discovery:** The MCP Server will parse the vault on startup and broadcast available personas as Prompts, and installation commands as Tools.

### Infrastructure & Deployment

- **Distribution:** Published to PyPI, installable globally via 'uv tool install .'.
- **CI/CD:** GitHub Actions for testing the CLI and Crucible evaluations before release.
- **The Crucible (Hooks):** Native Git pre-push hook integration that invokes a local subprocess to run assertions against the 'gemini-2.0-pro-exp' model (or user-configured equivalent).

### Decision Impact Analysis

**Implementation Sequence:**
1. Implement the TOML lockfile parser and generator ('savile.lock').
2. Build the 'savile add' command leveraging GitPython for a Strict 3-Way Merge of remote repositories into the local working tree.
3. Integrate the Manual PyYAML schema validation step into the 'savile add' pipeline to reject invalid modules before they are merged.
4. Update the MCP Server to read dependencies from the validated frontmatter.

**Cross-Component Dependencies:**
- The 'savile add' command is tightly coupled to the Schema Validation Engine; a repository cannot be merged if its modules fail the strict PyYAML checks.


## Implementation Patterns & Consistency Rules

### Core Development Rules (Strict Enforcement)

**1. File Path Resolution:**
- **MUST** use 'pathlib.Path' exclusively.
- **FORBIDDEN:** 'os.path.join', hardcoded absolute strings.
- **Pattern:** 'vault_root = Path.cwd() / "personas"'

**2. Synchronous vs Asynchronous Boundaries:**
- CLI Entrypoints ('src/savile/cli.py'): **MUST** be synchronous 'def'.
- MCP Handlers ('src/savile/mcp_server.py'): **MUST** be asynchronous 'async def'.
- Boundary bridging: Use 'asyncio.run(main_async_function())' only at the topmost CLI command level.

**3. State Modification & Git Operations:**
- **MUST** use 'GitPython' ('import git') for repository cloning, fetching, and merging during 'savile add'.
- **FORBIDDEN:** 'subprocess.run(["git", ...])' for state management (subprocess is reserved strictly for evaluation hooks).

**4. Error Handling & User Output:**
- **MUST** use 'typer.echo' or 'typer.secho(..., fg=typer.colors.RED, err=True)' for output.
- **FORBIDDEN:** 'print()'.
- **Pattern:** Catch expected operational errors (e.g., Git merge conflicts, invalid YAML) and raise 'raise typer.Exit(code=1)' instead of allowing raw tracebacks to hit the user.

**5. Schema Validation ('pyyaml'):**
- **Pattern:** When reading modules, always use 'yaml.safe_load_all()'. The first document is the frontmatter; the remaining string is the body. 
- **Validation:** Missing required keys ('name', 'version', 'category') must throw a custom 'SchemaValidationError'.


## Project Structure & Boundaries (v1.5.0)

### Complete Project Directory Structure
[As defined in the Python structure above]

### The Refined Vault Schema (v1.5.0)
To support scale and universal adoption, the flat v1.0.0 vault structure is evolving into a Hierarchical & Namespaced Vault Schema.

```text
my-logic-vault/
├── .savile/              # NEW: Vault-level configuration
│   └── vault.toml        # Metadata about the vault itself
├── personas/             # Core local personas
│   └── [category]/       # OPTIONAL: e.g., personas/engineering/dev.md
├── frameworks/           # Core local frameworks
│   └── [category]/       # OPTIONAL: e.g., frameworks/agile/scrum.md
├── modules/              # NEW: Namespaced external logic (from 'savile add')
│   └── [org]/            # e.g., modules/bmad-method/
│       ├── personas/
│       └── frameworks/
├── shared/               # NEW: Reusable fragments & templates
│   └── snippets/         # Common logic to be included in multiple personas
└── evals/                # The Crucible matrices
    └── [category]/
```

### Architectural Boundaries

**Sync & Remote Boundaries:**
- All remote fetching happens in 'src/savile/sync/'.
- 'GitPython' is the exclusive transport for 'savile add' and 'savile sync'.

**Validation & Schema Boundaries:**
- 'src/savile/core/schema.py' is the gatekeeper.
- No module is accepted into the registry if it fails the strict PyYAML validation (name, version, category).

**Lockfile & Resolution Boundaries:**
- 'savile.lock' (TOML) is managed by 'src/savile/core/resolver.py'.
- This ensures team-wide deterministic logic syncing.

### Requirements to Structure Mapping

**Feature: Remote Module Installation ('savile add')**
- CLI Logic: 'src/savile/cli.py'
- Sync Execution: 'src/savile/sync/manager.py'
- Validation: 'src/savile/core/schema.py'

**Feature: Deterministic Versioning ('savile.lock')**
- Parser/Generator: 'src/savile/core/resolver.py'
- Verification: 'src/savile/cli.py' (integrated into 'sync' and 'add' commands).

**Feature: v1.0.0 to v1.5.0 Vault Migration Strategy**
- The 'savile init' and 'savile sync' commands will detect the presence of '.savile/vault.toml'. 
- If absent, a transparent, non-destructive migration script ('savile migrate') will scaffold the new directories ('modules/', 'shared/', '.savile/') without altering the existing flat '/personas' or '/frameworks' files.


## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
The use of TOML for 'savile.lock' and YAML for module frontmatter is syntactically coherent. 'GitPython' seamlessly supports the Strict 3-Way merge strategy defined for remote module installation.

**Pattern Consistency:**
The strict separation of 'async' MCP handlers and synchronous Typer CLI commands ensures the event loop remains unblocked during heavy file I/O or network operations.

**Structure Alignment:**
The introduction of the 'modules/' namespace in the Vault Schema prevents external code collisions and supports the core "Protocol Hegemony" strategic initiative.

### Requirements Coverage Validation ✅

**Feature Coverage:**
The 'savile.lock' file provides the requested deterministic logic versioning, and the 'modules/' directory satisfies the need for an organized, scaleable vault.

**Non-Functional Requirements Coverage:**
The choice of Manual PyYAML parsing ensures the daemon remains lightweight, fulfilling the "zero cloud latency" and "high performance" NFRs.

### Gap Analysis Results
- **Minor:** Git credential management. SAVILE relies on the host OS. The implementation must include user-friendly error boundaries when 'GitPython' encounters authentication failures during 'savile add'.

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION
**Confidence Level:** High

**Key Strengths:**
- Zero cloud lock-in.
- Highly organized, namespaced vault schema.
- Strict consistency rules for AI agent implementation.

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all 'pathlib' and synchronous/asynchronous boundary rules strictly.
- Use 'typer.Exit' for expected errors; no raw tracebacks.
- Refer to the v1.5.0 Vault Schema when modifying the 'Registry' parser.

**First Implementation Priority:**
Develop the v1.0.0 to v1.5.0 Vault Migration Script ('savile migrate') to scaffold '.savile/vault.toml' and the 'modules/' directory before building the 'savile add' command.

