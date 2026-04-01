#!/bin/bash

# SAVILE: MCP Server Run Script
# Purpose: Starts the SAVILE MCP server over stdio for AI agents (like Claude Desktop, OpenClaw, Cursor)

set -e

# Resolve the directory of this script to find the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default to the project root if no vault path is provided
VAULT_PATH="${1:-$PROJECT_ROOT}"

# Execute the MCP server directly using uv run.
# uv automatically manages the .venv detection and environment activation.
exec uv run savile serve --vault "$VAULT_PATH"
