import os
import shutil
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent, Prompt, GetPromptResult, PromptMessage
import mcp.server.stdio

async def list_prompts_handler(vault_path: Path) -> list[Prompt]:
    prompts = []
    for category in ["personas", "frameworks"]:
        cat_path = vault_path / category
        if cat_path.exists():
            for f in cat_path.iterdir():
                if f.is_file() and not f.name.startswith("."):
                    prompts.append(
                        Prompt(
                            name=f.stem,
                            description=f"{category.capitalize()} module: {f.name}",
                            arguments=[]
                        )
                    )
    return prompts

async def get_prompt_handler(vault_path: Path, name: str, arguments: dict | None) -> GetPromptResult:
    categories = ["personas", "frameworks"]
    
    if isinstance(arguments, dict) and arguments.get("category") in categories:
        categories = [arguments["category"]]

    # Try to find the file in personas then frameworks
    for category in categories:
        cat_path = vault_path / category
        if cat_path.exists():
            for f in cat_path.iterdir():
                if f.is_file() and f.stem == name:
                    with open(f, "r") as file_handle:
                        content = file_handle.read()
                    return GetPromptResult(
                        description=f"Content of {f.name}",
                        messages=[
                            PromptMessage(
                                role="user",
                                content=TextContent(type="text", text=content)
                            )
                        ]
                    )
    raise ValueError(f"Prompt not found: {name}")

async def list_tools_handler() -> list[Tool]:
    return [
        Tool(
            name="list_logic_modules",
            description="List available personas and frameworks in the SAVILE vault.",
            inputSchema={"type": "object", "properties": {}}
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
        ),
        Tool(
            name="install_logic_module",
            description="Installs a persona or framework from the SAVILE vault directly into the current workspace's .agent/workflows/ or .agent/skills/ directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Source category: 'personas' or 'frameworks'"},
                    "name": {"type": "string", "description": "The exact filename of the module (e.g., 'pm.md')"},
                    "target_type": {"type": "string", "description": "Target directory type: 'workflow' or 'skill'"},
                    "project_path": {"type": "string", "description": "Optional explicit path to the project directory. Defaults to the CWD of the server if omitted."},
                },
                "required": ["category", "name", "target_type"]
            }
        )
    ]

async def call_tool_handler(vault_path: Path, name: str, arguments: dict) -> list[TextContent]:
    if arguments is None or not isinstance(arguments, dict):
        # Only list_logic_modules can potentially accept no arguments safely, but MCP schema expects an object
        if name != "list_logic_modules" or arguments is not None:
            return [TextContent(type="text", text="Error: arguments must be a valid dictionary.")]
        arguments = {}
        
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
        
        target = (vault_path / category / module_name).resolve()
        # Path traversal protection
        if not str(target).startswith(str((vault_path / category).resolve())):
            return [TextContent(type="text", text="Error: Invalid path.")]
        
        if not target.exists() or not target.is_file():
            return [TextContent(type="text", text=f"Error: {module_name} not found in {category}.")]
        
        with open(target, "r") as f:
            content = f.read()
        return [TextContent(type="text", text=content)]

    elif name == "install_logic_module":
        category = arguments.get("category", "")
        module_name = arguments.get("name", "")
        target_type = arguments.get("target_type", "")
        project_path_str = arguments.get("project_path")

        if category not in ["personas", "frameworks"]:
            return [TextContent(type="text", text="Error: Category must be 'personas' or 'frameworks'")]
        
        if target_type not in ["workflow", "skill"]:
            return [TextContent(type="text", text="Error: target_type must be 'workflow' or 'skill'")]

        source_file = (vault_path / category / module_name).resolve()
        if not str(source_file).startswith(str((vault_path / category).resolve())):
            return [TextContent(type="text", text="Error: Invalid source path.")]

        if not source_file.exists() or not source_file.is_file():
            return [TextContent(type="text", text=f"Error: Source {module_name} not found.")]

        # Read source to extract description for Gemini CLI
        with open(source_file, "r") as f:
            content = f.read()
        
        description = f"Act as the {module_name.split('.')[0]} agent"
        # Simple frontmatter description extractor
        if content.startswith("---"):
            try:
                import yaml
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    meta = yaml.safe_load(parts[1])
                    if isinstance(meta, dict) and "description" in meta:
                        description = meta["description"]
            except ImportError:
                pass # yaml not installed or parsing error

        base_dir = Path(project_path_str).resolve() if project_path_str else Path.cwd()

        # 1. Install to .agent/
        target_dir = base_dir / ".agent" / f"{target_type}s"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / module_name
        
        if target_file.exists():
            return [TextContent(type="text", text=f"Error: Target {module_name} already exists. Refusing to overwrite.")]
            
        shutil.copy2(source_file, target_file)

        # 2. Generate Gemini CLI TOML command
        gemini_cmd_dir = base_dir / ".gemini" / "commands"
        gemini_cmd_dir.mkdir(parents=True, exist_ok=True)
        stem = Path(module_name).stem
        toml_file = gemini_cmd_dir / f"{stem}.toml"
        
        if not toml_file.exists():
            toml_content = f'description = "{description}"\nprompt = "/{stem} {{{{args}}}}"\n'
            with open(toml_file, "w") as f:
                f.write(toml_content)

        msg = (
            f"Successfully installed {module_name} to {target_file.relative_to(base_dir)}\n"
            f"Created Gemini CLI command at {toml_file.relative_to(base_dir)}"
        )
        return [TextContent(type="text", text=msg)]
        
    raise ValueError(f"Unknown tool: {name}")

def create_mcp_server(vault_path: Path) -> Server:
    server = Server("savile")

    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        return await list_prompts_handler(vault_path)

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        return await get_prompt_handler(vault_path, name, arguments)

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return await list_tools_handler()

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
        return await call_tool_handler(vault_path, name, arguments)

    return server

async def run_stdio_server(vault_path: Path):
    server = create_mcp_server(vault_path)
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
