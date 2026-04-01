#!/bin/bash

# SAVILE: MCP Server Run Script
# Purpose: Starts the SAVILE MCP server over stdio for AI agents (like Claude Desktop, OpenClaw, Cursor, Warp, Antigravity)

set -e

# Resolve the directory of this script to find the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    cat << EOF
SAVILE MCP Server Runner
========================
Starts the SAVILE MCP server over stdio, seamlessly managing the Python 
virtual environment via uv.

Usage: 
  $(basename "$0") [VAULT_PATH] [--sse] [--port PORT]

Arguments:
  VAULT_PATH    Optional. Path to the SAVILE Logic Vault. Defaults to:
                $PROJECT_ROOT
  --sse         Run the server over HTTP SSE (Required for Warp)
  --port PORT   Port to run the SSE server on (Default: 8000)

--- Configuration Guide for AI Agents ---

To use SAVILE with an MCP-compatible agent or IDE, configure it as a 
'stdio' server using the absolute path to this script.

[ Claude Desktop / Antigravity ]
Add the following to your configuration file:

{
  "mcpServers": {
    "savile": {
      "command": "$SCRIPT_DIR/run-mcp.sh",
      "args": ["$PROJECT_ROOT"]
    }
  }
}

[ Warp ]
In Warp AI, enable MCP and add a new server:
- Name: savile
- Type: SSE (Server-Sent Events)
- Server URL: http://127.0.0.1:8000/sse

* Note: To use Warp, you must start this script with the --sse flag:
  $SCRIPT_DIR/run-mcp.sh "$PROJECT_ROOT" --sse

[ Cursor / Windsurf / OpenClaw ]
Add a new MCP server in the settings:
- Name: savile
- Type: command (or stdio)
- Command: $SCRIPT_DIR/run-mcp.sh "$PROJECT_ROOT"

[ Gemini CLI ]
SAVILE integrates with Gemini CLI via the 'install_logic_module' tool. 
When an agent uses this tool to install a persona, it automatically 
generates a .toml command in your .gemini/commands/ directory.

To use the vault directly in Gemini CLI without installing:
1. Ensure this server is running in another terminal.
2. Use Gemini CLI's 'mcp' integration if configured globally.

EOF
    exit 0
fi

# Log to stderr so it doesn't interfere with the MCP stdio JSON-RPC stream
>&2 echo "Starting SAVILE MCP server..."

# Extract vault path if provided as first arg, otherwise default to PROJECT_ROOT
VAULT_PATH="$PROJECT_ROOT"
if [[ -n "$1" && ! "$1" == -* ]]; then
  VAULT_PATH="$1"
  shift # Remove the path from args so we can pass the rest of the flags
fi

# Execute the MCP server directly using uv run.
# uv automatically manages the .venv detection and environment activation.
exec uv run savile serve --vault "$VAULT_PATH" "$@"
