# Changelog

All notable changes to the SAVILE project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-03-28

### Added
- **BMAD Automation:** Added `scripts/setup-bmad.sh` to automatically install the BMAD-METHOD framework and link it to the vault.
- **Interactive Setup:** Introduced `savile setup` command and integrated it into `savile init` to interactively prompt users to link their local `.bmad-core` installation.
- **CLI E2E Tests:** Added comprehensive End-to-End test suite (`tests/e2e/test_cli_e2e.py`) to validate all Typer command workflows.
- **Adversarial Regression Tests:** Added `tests/test_mcp_adversarial.py` to enforce and capture expected secure behaviors in the MCP server.

### Fixed
- **MCP Security Patches:** Addressed path traversal bypass vulnerabilities via strict symlink checking.
- **MCP Memory Safety:** Fixed missing type validation on arguments passed to tool handlers to prevent `NoneType` and `list` crashes.
- **MCP State Pollution:** Resolved Implicit CWD Dependency in `install_logic_module` by introducing the `project_path` argument, stopping the pollution of arbitrary directories.
- **MCP Data Loss:** Fixed silent file overwriting by enforcing strict `.exists()` bounds checks on target files.
- **MCP Namespace Shadowing:** Updated `get_prompt_handler` to properly accept and prioritize category contexts when identical filenames exist across `personas/` and `frameworks/`.
- **CLI Exception Handling:** Fixed an issue where `savile install-hook` was swallowing `typer.Exit` exceptions and returning a `0` exit code incorrectly.

## [0.2.0] - 2026-03-25

### Added
- **The Crucible Integration:** Automated Git `pre-push` hook installation via `savile install-hook`.
- **MCP Prompts:** Support for `list_prompts` and `get_prompt` in the MCP server for dynamic slash-command integration in IDEs.
- **MCP Installation Tool:** New `install_logic_module` tool to physically copy modules from the vault to a project's local `.agent` structure.
- **CLI Enhancements:** Added `--vault` (`-v`) option to `savile serve` for flexible vault positioning.

## [0.1.0] - 2026-03-25

### Added
- **Registry Core:** Standardized directory schema (`/personas`, `/frameworks`, `/evals`).
- **State Manager:** Git-native sync engine for local and remote logical vaults.
- **MCP Bridge:** Python-based MCP server providing logic module read/list capabilities.
- **CLI Router:** Typer-based CLI with `init`, `sync`, `serve`, and `evaluate` commands.
- **Crucible:** Initial implementation of the logic evaluation runner.
- **Technical Documentation:** PRD, Architecture Specs, and Epic Breakdown.
- **Test Suite:** Comprehensive unit tests for registry, sync, and crucible components.

---
*Created with SAVILE v0.1.0 checkpoint.*
