import os
import sys
import re
import shutil
from pathlib import Path
import typer
import anyio
from savile.core import registry, protocol
from savile.sync import manager
from savile.mcp import server as mcp_server

app = typer.Typer(
    help="SAVILE: Single Source of Truth Engine for Agent Prompts & Skills",
    no_args_is_help=False,
)


def print_error(message: str, help_text: str = None):
    """Prints a structured error message to stdout per AXI Standard 6."""
    typer.echo(f"error: {message}")
    if help_text:
        typer.echo(f"help: {help_text}")


def run_setup(vault_path: Path, method_path: str = None):
    """Run the setup for pre-requisites like the Method core framework."""
    method_link = vault_path / ".method-core"
    if method_link.exists() or method_link.is_symlink():
        typer.echo("✅ Method core link already exists.")
        return

    if method_path is None:
        if sys.stdin.isatty():
            typer.echo("\n--- SAVILE Pre-requisites Setup ---")
            typer.echo("SAVILE's built-in personas rely on the Method framework.")
            typer.echo(
                "Method core not linked. You need a local Method installation (created via framework installation)."
            )
            method_path = typer.prompt(
                "Enter the absolute or relative path to your Method project directory (or leave blank to skip)",
                default="",
            )
        else:
            typer.echo(
                "info: Skipping interactive setup (non-interactive environment)."
            )
            typer.echo(
                "help: To link the Method core, run `savile setup --method-path <path>`"
            )
            return

    if not method_path:
        typer.echo("Skipping setup. You can run 'savile setup' later to configure it.")
        return

    method_dir = Path(method_path).expanduser().resolve()
    core_path = method_dir / ".method-core"

    if not core_path.exists():
        print_error(
            f"Method core not found in {method_dir}",
            "Please ensure you run framework installation in that directory to initialize.",
        )
        return

    try:
        os.symlink(core_path, method_link)
        typer.echo(f"✅ Successfully linked Method core to {core_path}")
    except Exception as e:
        print_error(f"Failed to create symlink: {e}")


@app.command()
def setup(
    method_path: str = typer.Option(
        None,
        "--method-path",
        help="Absolute or relative path to your Method project directory",
    ),
):
    """Configure pre-requisites for the logic vault."""
    vault_path = Path(os.getcwd())
    run_setup(vault_path, method_path=method_path)


@app.command(name="bootstrap")
def bootstrap(
    source: str = typer.Option(None, help="Git URI to logic vault"),
    method_path: str = typer.Option(
        None,
        "--method-path",
        help="Absolute or relative path to your Method project directory",
    ),
):
    """Initialize a new local logic vault or clone from a remote SSoT."""
    vault_path = Path(os.getcwd())
    if source:
        typer.echo(f"Bootstrapping logic vault from {source}...")
        try:
            manager.init_remote(vault_path, source)
            typer.echo("Remote vault cloned successfully.")
        except Exception as e:
            print_error(str(e), "Verify the source Git URL or network connection")
            raise typer.Exit(code=1)
    else:
        typer.echo("Bootstrapping new local logic vault...")
        try:
            registry.scaffold_local_vault(vault_path)
            manager.init_local(vault_path)
            typer.echo("Local vault scaffolded and initialized successfully.")
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(code=1)

    run_setup(vault_path, method_path=method_path)


# Alias init to bootstrap for backwards compatibility
@app.command(name="init", hidden=True)
def init_alias(
    source: str = typer.Option(None, help="Git URI to logic vault"),
    method_path: str = typer.Option(
        None, "--method-path", help="Path to Method project"
    ),
):
    bootstrap(source, method_path)


@app.command(name="import")
def import_cmd(
    source: str = typer.Argument(..., help="Git URI to logic module repository"),
    alias: str = typer.Option(
        None, "--alias", "-a", help="Alias for the logic module filename"
    ),
):
    """Import logic modules/skills from outside sources into the local vault."""
    vault_path = Path(os.getcwd())
    typer.echo(f"Importing logic modules from {source}...")
    try:
        modules = protocol.add_remote_module(vault_path, source, alias)
        if not modules:
            print_error(
                "No valid modules found in the source repository.",
                "Ensure the repository has valid logic modules",
            )
            raise typer.Exit(code=1)

        for m in modules:
            typer.echo(f"✅ Imported module: {m}")
        typer.echo("Successfully imported all logic modules.")
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(code=1)


# Alias add to import
@app.command(name="add", hidden=True)
def add_alias(source: str, alias: str = None):
    import_cmd(source, alias)


@app.command()
def create(
    name: str = typer.Argument(
        ..., help="Functional name of the agent/persona (e.g., ux-designer)"
    ),
    description: str = typer.Option(
        "A new functional persona", "--desc", help="Brief description of the role"
    ),
):
    """Create a new persona/function using strict de-anthropomorphized naming conventions."""
    vault_path = Path(os.getcwd())
    try:
        p_file, f_file = registry.create_persona(vault_path, name, description)
        typer.echo(f"✅ Created persona: {p_file}")
        typer.echo(f"✅ Created framework: {f_file}")
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=1)


@app.command()
def update(
    name: str = typer.Argument(..., help="Name of the existing persona to update"),
):
    """Update an existing persona/function/skill (refreshes metadata)."""
    vault_path = Path(os.getcwd())
    p_file = vault_path / "personas" / f"{name}.md"

    if not p_file.exists():
        print_error(
            f"Persona '{name}' not found.", f"Run `savile create {name}` to create it."
        )
        raise typer.Exit(code=1)

    # Touch the file to update modification time (simulating a refresh/update)
    p_file.touch()
    typer.echo(f"✅ Refreshed metadata for persona: {name}")


@app.command()
def export(
    out: Path = typer.Option(
        Path("dist/skills"), "--out", "-o", help="Output directory for Vercel Skills"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing output directory"
    ),
):
    """Compile and export logic into portable Vercel Labs SKILL.md format artifacts."""
    vault_path = Path(os.getcwd())
    try:
        exported_files = registry.export_skills(vault_path, out, force)
        for skill_file in exported_files:
            typer.echo(f"  Exported skill -> {skill_file}")
        typer.echo(
            f"\n✅ Successfully exported {len(exported_files)} Vercel-compatible skills to {out}/"
        )
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(code=1)


@app.command()
def serve(
    vault: Path = typer.Option(
        Path(os.getcwd()), "--vault", "-v", help="Path to the logic vault"
    ),
    sse: bool = typer.Option(
        False, "--sse", help="Run the server over HTTP SSE instead of stdio"
    ),
    port: int = typer.Option(
        8000, "--port", "-p", help="Port to run the SSE server on (if --sse is used)"
    ),
):
    """Start the local MCP server to dynamically supply skills to IDEs."""
    if sse:
        typer.echo(
            f"Starting MCP server over SSE at http://127.0.0.1:{port}/sse", err=True
        )
        anyio.run(mcp_server.run_sse_server, vault, port)
    else:
        anyio.run(mcp_server.run_stdio_server, vault)


@app.command()
def evaluate():
    """Run the Crucible evaluation loop against logic changes."""
    vault_path = Path(os.getcwd())
    typer.echo("Evaluating logic changes using The Crucible...")
    from savile.evals import crucible as crucible_runner

    success = crucible_runner.run_evaluations(vault_path)
    if not success:
        print_error(
            "Crucible evaluations failed. Commit rejected.",
            "Verify that all evaluations are defined correctly.",
        )
        raise typer.Exit(code=1)

    typer.echo("All logical assertions passed.")


@app.command()
def install_hook():
    """Install the pre-push Git hook to enforce evaluate before push."""
    vault_path = Path(os.getcwd())
    if not (vault_path / ".git").exists():
        print_error(
            "Current directory is not a Git repository. Cannot install hook.",
            "Initialize Git using `git init` or initialize the vault using `savile bootstrap` first.",
        )
        raise typer.Exit(code=1)

    try:
        manager.install_pre_push_hook(vault_path)
        typer.echo("Pre-push hook installed successfully.")
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(code=1)


@app.command()
def sync():
    """Sync the local logic vault with the remote repository."""
    vault_path = Path(os.getcwd())
    typer.echo("Syncing logic vault...")
    try:
        res = manager.sync_vault(vault_path)
        if res:
            typer.echo(res)
        typer.echo("Sync complete.")
    except Exception as e:
        print_error(str(e))


def show_home_view():
    """Renders the Content-First AXI Home View on standard output."""
    vault_path = Path(os.getcwd())

    # Identify the tool
    typer.echo("bin: savile")
    typer.echo("description: Single Source of Truth Engine for Agent Prompts & Skills")
    typer.echo()

    # Check if this is a valid local vault
    is_vault = (
        (vault_path / "personas").exists()
        or (vault_path / "frameworks").exists()
        or (vault_path / "evals").exists()
    )

    if not is_vault:
        typer.echo("vault: 0 logic vaults found in this directory")
        typer.echo()
        typer.echo("help[1]:")
        typer.echo(
            "  Run `savile bootstrap` to initialize a local logic vault or pull from remote"
        )
        return

    # List Personas
    personas_path = vault_path / "personas"
    personas = []
    if personas_path.exists():
        personas = [
            p.stem
            for p in personas_path.iterdir()
            if p.is_file() and p.suffix == ".md" and p.name != ".gitkeep"
        ]

    if personas:
        typer.echo(f"personas[{len(personas)}]{{name}}:")
        for p in sorted(personas):
            typer.echo(f"  {p}")
    else:
        typer.echo("personas: 0 personas found in this repository")
    typer.echo()

    # List Frameworks
    frameworks_path = vault_path / "frameworks"
    frameworks = []
    if frameworks_path.exists():
        frameworks = [
            f.stem
            for f in frameworks_path.iterdir()
            if f.is_file() and f.suffix == ".md" and f.name != ".gitkeep"
        ]

    if frameworks:
        typer.echo(f"frameworks[{len(frameworks)}]{{name}}:")
        for f in sorted(frameworks):
            typer.echo(f"  {f}")
    else:
        typer.echo("frameworks: 0 frameworks found in this repository")
    typer.echo()

    # List Evaluations
    evals_path = vault_path / "evals"
    evals = []
    if evals_path.exists():
        evals = [
            e.stem
            for e in evals_path.iterdir()
            if e.is_file() and e.suffix in [".yaml", ".yml"] and e.name != ".gitkeep"
        ]

    if evals:
        typer.echo(f"evals[{len(evals)}]{{name}}:")
        for e in sorted(evals):
            typer.echo(f"  {e}")
    else:
        typer.echo("evals: 0 evaluations found in this repository")
    typer.echo()

    # Contextual disclosures
    typer.echo("help[4]:")
    typer.echo("  Run `savile create <name>` to scaffold a new persona")
    typer.echo("  Run `savile export` to compile Vercel-compatible SKILL.md files")
    typer.echo("  Run `savile serve` to start the local MCP server")
    typer.echo("  Run `savile evaluate` to run Crucible evaluations")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-V", help="Show version and exit"
    ),
):
    """SAVILE: Single Source of Truth Engine for Agent Prompts & Skills"""
    if version:
        typer.echo("savile 1.5.0")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        show_home_view()


if __name__ == "__main__":
    app()
