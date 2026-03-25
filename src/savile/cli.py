import os
from pathlib import Path
import typer
import anyio
from savile.core import registry
from savile.sync import manager
from savile.mcp import server as mcp_server

app = typer.Typer(help="SAVILE: System for Agentic Versioning, Intelligence, and Logical Evaluation")

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
    else:
        typer.echo("Initializing new local logic vault...")
        registry.scaffold_local_vault(vault_path)
        typer.echo("Local vault scaffolded successfully.")

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
def serve():
    """Start the MCP server to expose the logic vault to connected tools."""
    vault_path = Path(os.getcwd())
    anyio.run(mcp_server.run_stdio_server, vault_path)

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
