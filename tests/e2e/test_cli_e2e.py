import pytest
import os
import shutil
from pathlib import Path
from typer.testing import CliRunner
from savile.cli import app
from git import Repo

runner = CliRunner()


def test_cli_help():
    """Test that the CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert (
        "SAVILE: Single Source of Truth Engine for Agent Prompts & Skills"
        in result.stdout
    )


def test_init_local_vault(tmp_path):
    """Test initializing a local vault."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Pass a newline (\n) to the interactive prompt so it skips Method setup
        result = runner.invoke(app, ["bootstrap"], input="\n")
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
        result = runner.invoke(
            app, ["bootstrap", "--source", "invalid-url"], input="\n"
        )
        assert result.exit_code == 1
        assert (
            "error:" in result.stdout
            or "Error:" in result.stdout
            or "error:" in result.stderr
            or "Error:" in result.stderr
        )
    finally:
        os.chdir(original_cwd)


def test_install_hook(tmp_path):
    """Test installing the git hook in an initialized vault."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # First initialize
        runner.invoke(app, ["bootstrap"], input="\n")

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
        assert (
            "error: Current directory is not a Git repository" in result.stdout
            or "Current directory is not a Git repository" in result.stderr
        )
    finally:
        os.chdir(original_cwd)


def test_sync_no_remote(tmp_path):
    """Test syncing a vault with no remote."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")

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


def test_home_view_no_vault(tmp_path):
    """Test running savile with no arguments outside of a vault directory."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "bin: savile" in result.stdout
        assert "vault: 0 logic vaults found in this directory" in result.stdout
    finally:
        os.chdir(original_cwd)


def test_home_view_with_vault(tmp_path):
    """Test running savile with no arguments in an initialized vault."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")
        # Create a mock persona and framework to verify listing
        (tmp_path / "personas" / "custom_persona.md").touch()
        (tmp_path / "frameworks" / "custom_framework.md").touch()

        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "bin: savile" in result.stdout
        assert "personas[1]{name}:" in result.stdout
        assert "  custom_persona" in result.stdout
        assert "frameworks[1]{name}:" in result.stdout
        assert "  custom_framework" in result.stdout
    finally:
        os.chdir(original_cwd)


def test_evaluate_toon_format(tmp_path):
    """Test that the evaluate command outputs in TOON format."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")

        # Copy mock yaml
        mock_yaml_src = Path(__file__).parent.parent / "mock_eval.yaml"
        mock_yaml_dst = tmp_path / "evals" / "mock_eval.yaml"
        shutil.copy(mock_yaml_src, mock_yaml_dst)

        result = runner.invoke(app, ["evaluate"])
        assert result.exit_code == 0
        assert "Evaluating logic changes using The Crucible..." in result.stdout
        assert "evaluations[1]{matrix,target,status}:" in result.stdout
        assert "  Check System Realist,gemini-2.0-pro-exp,PASS" in result.stdout
    finally:
        os.chdir(original_cwd)


def test_create_valid_persona(tmp_path):
    """Test creating a persona with a valid functional name."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")
        result = runner.invoke(app, ["create", "test-engineer"])
        assert result.exit_code == 0
        assert "Created persona:" in result.stdout
        assert (tmp_path / "personas" / "test-engineer.md").exists()
        assert (tmp_path / "frameworks" / "test-engineer.md").exists()
    finally:
        os.chdir(original_cwd)


def test_create_invalid_human_name(tmp_path):
    """Test that creating a persona with a prohibited human name fails."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")
        result = runner.invoke(app, ["create", "david"])
        assert result.exit_code == 1
        assert "error: Invalid agent name 'david'." in result.stdout
        assert "Human-like names are prohibited" in result.stdout
    finally:
        os.chdir(original_cwd)


def test_update_persona(tmp_path):
    """Test updating an existing persona metadata."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")
        runner.invoke(app, ["create", "dev-ops"])

        result = runner.invoke(app, ["update", "dev-ops"])
        assert result.exit_code == 0
        assert "Refreshed metadata for persona: dev-ops" in result.stdout
    finally:
        os.chdir(original_cwd)


def test_export_skills(tmp_path):
    """Test exporting skills to Vercel Labs format."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        runner.invoke(app, ["bootstrap"], input="\n")
        runner.invoke(app, ["create", "researcher"])

        out_dir = tmp_path / "dist" / "skills"
        result = runner.invoke(app, ["export", "-o", str(out_dir)])
        assert result.exit_code == 0
        assert "Successfully exported" in result.stdout

        # Verify output format
        skill_file = out_dir / "researcher" / "SKILL.md"
        assert skill_file.exists()

        content = skill_file.read_text()
        assert content.startswith("---")
        assert "name: researcher" in content
        assert "Methodologies for researcher." in content
    finally:
        os.chdir(original_cwd)
