# Technical Architecture: SAVILE
*System for Agentic Versioning, Intelligence, and Logical Evaluation*

## 1. Architectural Philosophy
As the System Architect, my focus is on stability, developer productivity, and pragmatic choices. SAVILE must be reliable and act as a thin, highly deterministic layer between the filesystem (Git) and the AI IDE client (via MCP). We will embrace "boring technology" for stability while enabling cutting-edge AI agent workflows.

## 2. System Components

### 2.1 The CLI & Daemon Router (`typer`)
* **Role:** The entry point for all user interactions.
* **Technology:** `typer` (Python).
* **Rationale:** Provides clean, type-hinted, and self-documenting CLI commands (`init`, `sync`, `serve`, `evaluate`).
* **Design Pattern:** The CLI acts purely as an interface routing to backend logic controllers to ensure modularity.

### 2.2 The State Manager (`GitPython`)
* **Role:** Handles distributed state and portability of the Logic Vault.
* **Technology:** `GitPython`.
* **Rationale:** By using Git as the primitive, we inherit diffing, branching, and remote synchronization for free without building custom cloud infrastructure.
* **Implementation Note:** All file paths must be resolved relatively from `~/.savile/config.yaml` or a local `.savile` marker directory. Avoid hardcoding global states in the executing python process.

### 2.3 The MCP Bridge (`mcp` SDK)
* **Role:** The connective tissue between the SAVILE daemon and the LLM/IDE ecosystem.
* **Technology:** The official Python `mcp` SDK utilizing `asyncio`.
* **Rationale:** It standardizes how local tools are exposed to models. Leveraging asynchronous streaming ensures high performance when reading large frameworks or persona files from disk.
* **Endpoints:** Must support standard `stdio` for local IDE invocation (e.g., Antigravity or Cursor).

### 2.4 The Crucible (`pyyaml` + `subprocess` / `pytest`)
* **Role:** Enforces logical consistency before code can be synced.
* **Technology:** `pyyaml` to parse the `/evals` matrices. `subprocess` to natively invoke evaluators (or integrated with `pytest`).
* **Implementation Note:** Eval tests must be strictly scoped. A test evaluates a mock input against an expected outcome utilizing an external LLM call (e.g., via `gemini-2.0-pro-exp` API). If the threshold fails, the command must exit with a non-zero status code, natively integrating with standard Git pre-push hooks.

## 3. Directory Structure

```text
savile/
├── pyproject.toml        # Poetry or uv managed dependencies
├── src/savile/
│   ├── cli.py            # Typer logic
│   ├── sync.py           # GitPython logic
│   ├── mcp_server.py     # MCP endpoints and routing
│   ├── crucible.py       # Evaluation logic
├── docs/                 # PRD, Architecture, Epics
```

**Target Logic Vault Schema (loaded by SAVILE):**
```text
my-logic-vault/
├── personas/             # e.g., systems_realist.md
├── frameworks/           # e.g., code_review_checklist.md
├── evals/                # test_assertions.yaml
```

## 4. Implementation Guidelines (for Devs)

1. **Async by Default:** Start with `asyncio` for the MCP loop, but explicitly isolate synchronous blocking tasks (like heavy Git networking) with `asyncio.to_thread()`.
2. **Error Handling:** Expose clean, structured stderr outputs. If a sync fails due to merge conflicts, the exception should guide the user on how to resolve it via standard Git workflows.
3. **No Database:** Never fall into the trap of using SQLite or local persistent metadata stores outside of raw YAML/Markdown. The filesystem *is* the database.

## 5. Logic Module Metadata Schema (Integrated)

To support remote installation and automated command generation, every module in the vault MUST include YAML frontmatter.

### 5.1 Schema Specification
```yaml
---
name: "module-name"           # Canonical name for CLI commands
version: "1.0.0"              # Semantic versioning for syncing
category: "persona"           # 'persona' or 'framework'
description: "Human readable"  # Used for Gemini CLI .toml metadata
dependencies:                 # Optional: list of other module names
  - "required-persona-name"
---
```

### 5.2 Validation Rules (The Crucible)
1. **Physical/Logical Match**: The `category` field in the metadata must match the file's subdirectory (e.g., category 'persona' must be in `/personas`).
2. **Naming**: The `name` field in the metadata should be used as the filename (minus `.md`) to prevent resolution conflicts.
3. **Dependency Resolution**: During `savile add`, the system must warn if dependencies listed in the metadata are missing from the local vault.

---
*Signed, Winston (System Architect)*
