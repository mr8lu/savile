import pytest
import os
from pathlib import Path
from typer.testing import CliRunner
from savile.cli import app
from git import Repo

runner = CliRunner()

def test_cli_help():
    """Test that the CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "SAVILE: System for Agentic Versioning, Intelligence, and Logical Evaluation" in result.stdout

def test_init_local_vault(tmp_path):
    """Test initializing a local vault."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Pass a newline (\n) to the interactive prompt so it skips BMAD setup
        result = runner.invoke(app, ["init"], input="\n")
        assert result.exit_code == 0
        assert "Local vault scaffolded and initialized successfully" in result.stdout
        
        # Verify structure
        assert (tmp_path / ".git").exists()
        assert (tmp_path / "personas").exists()
        assert (tmp_path / "frameworks").exists()
        assert (tmp_path / "evals").exists()
    finally:
        os.chdir(original_cwd)

def test_init_remote_vault_invalid_url(tmp_path):
    """Test initializing a vault from an invalid remote URL."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Pass a newline (\n) in case it gets to the setup step (though it shouldn't if it fails)
        result = runner.invoke(app, ["init", "--source", "invalid-url"], input="\n")
        assert result.exit_code == 1
        # typer.echo(err=True) writes to stderr
        assert "Error:" in result.stdout or "Error:" in result.stderr
    finally:
        os.chdir(original_cwd)

def test_install_hook(tmp_path):
    """Test installing the git hook in an initialized vault."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # First initialize
        runner.invoke(app, ["init"], input="\n")
        
        # Then install hook
        result = runner.invoke(app, ["install-hook"])
        assert result.exit_code == 0
        assert "Pre-push hook installed successfully" in result.stdout
        
        # Verify hook exists
        hook_path = tmp_path / ".git" / "hooks" / "pre-push"
        assert hook_path.exists()
        assert os.access(hook_path, os.X_OK)
    finally:
        os.chdir(original_cwd)

def test_install_hook_not_git_repo(tmp_path):
    """Test installing hook fails if not a git repo."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["install-hook"])
        assert result.exit_code == 1
        # typer.echo(err=True) writes to stderr, runner.invoke captures it all into stdout if unseparated or stderr depending on setup
        assert "Current directory is not a Git repository" in result.stdout or "Current directory is not a Git repository" in result.stderr
    finally:
        os.chdir(original_cwd)

def test_sync_no_remote(tmp_path):
    """Test syncing a vault with no remote."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["init"], input="\n")
        
        # Make a change
        (tmp_path / "personas" / "test.md").touch()
        
        result = runner.invoke(app, ["sync"])
        assert result.exit_code == 0
        assert "No remotes configured. Local commit only." in result.stdout
        
        # Verify it was committed
        repo = Repo(str(tmp_path))
        assert not repo.is_dirty()
    finally:
        os.chdir(original_cwd)
