import os
from pathlib import Path
import typer
import anyio
from savile.core import registry
from savile.sync import manager
from savile.mcp import server as mcp_server

app = typer.Typer(help="SAVILE: System for Agentic Versioning, Intelligence, and Logical Evaluation")

def run_setup(vault_path: Path):
    """Run the interactive setup for pre-requisites like BMAD."""
    typer.echo("\n--- SAVILE Pre-requisites Setup ---")
    typer.echo("SAVILE's built-in personas rely on the BMAD Method framework.")
    
    bmad_link = vault_path / ".bmad-core"
    if bmad_link.exists() or bmad_link.is_symlink():
        typer.echo("✅ .bmad-core link already exists.")
        return

    typer.echo("BMAD-method not linked. You need a local BMad installation (created via `npx bmad-method install`).")
    bmad_path = typer.prompt("Enter the absolute or relative path to your BMad project directory (or leave blank to skip)", default="")
    
    if not bmad_path:
        typer.echo("Skipping BMAD setup. You can run 'savile setup' later to configure it.")
        return
        
    bmad_dir = Path(bmad_path).expanduser().resolve()
    core_path = bmad_dir / ".bmad-core"
    
    if not core_path.exists():
        typer.echo(f"⚠️  Warning: .bmad-core not found in {bmad_dir}.", err=True)
        typer.echo("Please ensure you run 'npx bmad-method install' in that directory to initialize the framework.", err=True)
    
    try:
        os.symlink(core_path, bmad_link)
        typer.echo(f"✅ Successfully linked .bmad-core to {core_path}")
    except Exception as e:
        typer.echo(f"❌ Failed to create symlink: {e}", err=True)


@app.command()
def setup():
    """Configure pre-requisites (like BMAD-method) for the logic vault."""
    vault_path = Path(os.getcwd())
    run_setup(vault_path)


@app.command()
def init(source: str = typer.Option(None, help="Git URI to logic vault")):
    """Initialize a local logic vault from a remote Git repository."""
    vault_path = Path(os.getcwd())
    if source:
        typer.echo(f"Initializing logic vault from {source}...")
        try:
            manager.init_remote(vault_path, source)
            typer.echo("Remote vault cloned successfully.")
        except Exception as e:
            typer.echo(f"Error: {str(e)}", err=True)
            raise typer.Exit(code=1)
    else:
        typer.echo("Initializing new local logic vault...")
        try:
            registry.scaffold_local_vault(vault_path)
            manager.init_local(vault_path)
            typer.echo("Local vault scaffolded and initialized successfully.")
        except Exception as e:
            typer.echo(f"Error: {str(e)}", err=True)
            raise typer.Exit(code=1)
            
    run_setup(vault_path)

@app.command()
def install_hook():
    """Install the pre-push Git hook to enforce evaluate before push."""
    vault_path = Path(os.getcwd())
    try:
        if not (vault_path / ".git").exists():
            typer.echo("Current directory is not a Git repository. Cannot install hook.", err=True)
            raise typer.Exit(code=1)
            
        manager.install_pre_push_hook(vault_path)
        typer.echo("Pre-push hook installed successfully.")
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)

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
        typer.echo(f"Error: {str(e)}", err=True)

@app.command()
def serve(vault: Path = typer.Option(Path(os.getcwd()), "--vault", "-v", help="Path to the logic vault")):
    """Start the MCP server to expose the logic vault to connected tools."""
    anyio.run(mcp_server.run_stdio_server, vault)

@app.command()
def evaluate():
    """Run the Crucible evaluation loop against logic changes."""
    vault_path = Path(os.getcwd())
    typer.echo("Evaluating logic changes using The Crucible...")
    from savile.evals import crucible as crucible_runner
    
    success = crucible_runner.run_evaluations(vault_path)
    if not success:
        typer.echo("Crucible evaluations failed. Commit rejected.", err=True)
        raise typer.Exit(code=1)
    
    typer.echo("All logical assertions passed.")

if __name__ == "__main__":
    app()