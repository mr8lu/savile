# Changelog

All notable changes to the SAVILE project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
