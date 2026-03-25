import os
import anyio
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

def create_mcp_server(vault_path: Path) -> Server:
    server = Server("savile")

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return [
            Tool(
                name="list_logic_modules",
                description="List available personas and frameworks in the SAVILE vault.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                }
            ),
            Tool(
                name="read_logic_module",
                description="Read the contents of a specific persona or framework.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Either 'personas' or 'frameworks'"},
                        "name": {"type": "string", "description": "The exact filename of the module (e.g., 'realist.md')"},
                    },
                    "required": ["category", "name"]
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == "list_logic_modules":
            results = []
            for category in ["personas", "frameworks"]:
                cat_path = vault_path / category
                if cat_path.exists():
                    files = [f.name for f in cat_path.iterdir() if f.is_file() and not f.name.startswith(".")]
                    results.append(f"[{category.upper()}]: " + ", ".join(files))
            return [TextContent(type="text", text="\n".join(results) or "Vault empty.")]
            
        elif name == "read_logic_module":
            category = arguments.get("category", "")
            module_name = arguments.get("name", "")
            
            if category not in ["personas", "frameworks"]:
                return [TextContent(type="text", text="Error: Category must be 'personas' or 'frameworks'")]
            
            target = vault_path / category / module_name
            
            # Simple path traversal protection
            if not target.is_relative_to(vault_path / category):
                return [TextContent(type="text", text="Error: Invalid path.")]
            
            if not target.exists() or not target.is_file():
                return [TextContent(type="text", text=f"Error: {module_name} not found in {category}.")]
            
            with open(target, "r") as f:
                content = f.read()
            return [TextContent(type="text", text=content)]
            
        raise ValueError(f"Unknown tool: {name}")

    return server

async def run_stdio_server(vault_path: Path):
    server = create_mcp_server(vault_path)
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
