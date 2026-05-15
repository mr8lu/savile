import os
import json
import shutil
import uuid
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent, Prompt, GetPromptResult, PromptMessage
import mcp.server.stdio

def get_state_file(vault_path: Path) -> Path:
    state_file = vault_path / ".savile_board.json"
    if not state_file.exists():
        with open(state_file, "w") as f:
            json.dump({"tasks": [], "project_context": "Initialize your project context here."}, f)
    return state_file

def read_state(vault_path: Path) -> dict:
    with open(get_state_file(vault_path), "r") as f:
        return json.load(f)

def write_state(vault_path: Path, state: dict):
    with open(get_state_file(vault_path), "w") as f:
        json.dump(state, f, indent=2)

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

async def list_tools_handler(vault_path: Path) -> list[Tool]:
    tools = [
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

    # Dynamically expose each persona as an agent Tool
    personas_path = vault_path / "personas"
    if personas_path.exists():
        for f in personas_path.iterdir():
            if f.is_file() and not f.name.startswith("."):
                name = f.stem
                description = f"Delegate a task to the {name} persona agent."
                
                # Attempt to extract frontmatter description
                try:
                    with open(f, "r") as file_handle:
                        content = file_handle.read()
                    if content.startswith("---"):
                        import yaml
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            meta = yaml.safe_load(parts[1])
                            if isinstance(meta, dict) and "description" in meta:
                                description = meta["description"]
                except Exception:
                    pass

                tools.append(
                    Tool(
                        name=f"agent_{name}",
                        description=f"{description} Use this tool to summon the {name} agent for a specific task.",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task": {
                                    "type": "string",
                                    "description": f"The specific task or query you want the {name} agent to accomplish."
                                }
                            },
                            "required": ["task"]
                        }
                    )
                )

    # --- Symphony Control Plane Tools ---
    tools.extend([
        Tool(
            name="board_get_tasks",
            description="Control Plane: Retrieve all active tasks from the local SAVILE board. Use this to understand the current project state, who is doing what, and what needs to be picked up.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="board_add_task",
            description="Control Plane: Add a new task to the global board.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Short title of the task"},
                    "description": {"type": "string", "description": "Detailed description, criteria, and context."},
                    "assignee_persona": {"type": "string", "description": "The persona (e.g. 'dev', 'architect') this should be routed to."}
                },
                "required": ["title", "description", "assignee_persona"]
            }
        ),
        Tool(
            name="board_update_task",
            description="Control Plane: Update the status or notes of an existing task. Statuses: 'todo', 'in_progress', 'review', 'done'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "status": {"type": "string", "description": "Must be one of: 'todo', 'in_progress', 'review', 'done'"},
                    "notes": {"type": "string", "description": "Append any findings, commit hashes, or handoff notes."}
                },
                "required": ["task_id", "status"]
            }
        )
    ])

    return tools

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

    elif name.startswith("agent_"):
        persona_name = name[6:] # Strip "agent_"
        task = arguments.get("task", "")
        if not task:
            return [TextContent(type="text", text="Error: You must provide a 'task' argument for this agent.")]

        target = (vault_path / "personas" / f"{persona_name}.md").resolve()
        
        if not target.exists() or not target.is_file():
            return [TextContent(type="text", text=f"Error: Agent persona '{persona_name}' not found.")]
        
        with open(target, "r") as f:
            content = f.read()
            
        formatted_response = (
            f"<activated_agent_persona name=\"{persona_name}\">\n"
            f"{content}\n"
            f"</activated_agent_persona>\n\n"
            f"<agent_task>\n"
            f"{task}\n"
            f"</agent_task>\n\n"
            f"INSTRUCTIONS TO HOST AI: You must now strictly adopt the persona defined above "
            f"and execute the <agent_task> completely. Do not break character."
        )
        return [TextContent(type="text", text=formatted_response)]

    # --- Symphony Control Plane Handlers ---
    elif name == "board_get_tasks":
        state = read_state(vault_path)
        return [TextContent(type="text", text=json.dumps(state, indent=2))]

    elif name == "board_add_task":
        state = read_state(vault_path)
        task_id = str(uuid.uuid4())[:8]
        new_task = {
            "id": task_id,
            "title": arguments.get("title"),
            "description": arguments.get("description"),
            "assignee_persona": arguments.get("assignee_persona"),
            "status": "todo",
            "notes": ""
        }
        state["tasks"].append(new_task)
        write_state(vault_path, state)
        return [TextContent(type="text", text=f"Task added successfully. ID: {task_id}")]

    elif name == "board_update_task":
        state = read_state(vault_path)
        task_id = arguments.get("task_id")
        status = arguments.get("status")
        notes = arguments.get("notes", "")
        
        found = False
        for t in state["tasks"]:
            if t["id"] == task_id:
                t["status"] = status
                if notes:
                    t["notes"] += f"\n- {notes}"
                found = True
                break
                
        if not found:
            return [TextContent(type="text", text=f"Error: Task {task_id} not found.")]
            
        write_state(vault_path, state)
        return [TextContent(type="text", text=f"Task {task_id} updated to {status}.")]
        
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
        return await list_tools_handler(vault_path)

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

async def run_sse_server(vault_path: Path, port: int = 8000):
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route, Mount
    from starlette.responses import Response
    import uvicorn

    server = create_mcp_server(vault_path)
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1], server.create_initialization_options()
            )
        return Response()

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=sse.handle_post_message),
        ],
    )

    uvicorn_config = uvicorn.Config(starlette_app, host="127.0.0.1", port=port, log_level="info")
    uvicorn_server = uvicorn.Server(uvicorn_config)
    await uvicorn_server.serve()
