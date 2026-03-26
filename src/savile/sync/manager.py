import os
import time
from pathlib import Path
from git import Repo, exc
from savile.core import registry

def install_pre_push_hook(vault_path: Path):
    """Installs a pre-push Git hook to run savile evaluate."""
    hooks_dir = vault_path / ".git" / "hooks"
    if not hooks_dir.exists():
        hooks_dir.mkdir(parents=True, exist_ok=True)
    
    pre_push_path = hooks_dir / "pre-push"
    # Create a script that tries multiple ways to find and run savile
    hook_script = (
        "#!/bin/bash\n\n"
        "echo 'Running SAVILE Crucible evaluations...'\n"
        "\n"
        "# Find the savile command or its python module equivalent\n"
        "if command -v savile &> /dev/null; then\n"
        "    SAVILE_CMD=\"savile\"\n"
        "elif [ -f \".venv/bin/savile\" ]; then\n"
        "    SAVILE_CMD=\".venv/bin/savile\"\n"
        "elif [ -f \"../.venv/bin/savile\" ]; then\n"
        "    SAVILE_CMD=\"../.venv/bin/savile\"\n"
        "elif command -v python3 &> /dev/null && python3 -m savile.cli --help &> /dev/null; then\n"
        "    SAVILE_CMD=\"python3 -m savile.cli\"\n"
        "else\n"
        "    echo \"Error: 'savile' command not found. Please install it or ensure it is in your PATH.\"\n"
        "    exit 1\n"
        "fi\n"
        "\n"
        "$SAVILE_CMD evaluate\n"
        "if [ $? -ne 0 ]; then\n"
        "    echo 'Crucible evaluations failed. Push rejected.'\n"
        "    exit 1\n"
        "fi\n"
        "exit 0\n"
    )

    with open(pre_push_path, "w") as f:
        f.write(hook_script)
    
    os.chmod(pre_push_path, 0o755)

def init_local(vault_path: Path):
    """Initialize a local logic vault."""
    if (vault_path / ".git").exists():
        raise Exception("Vault is already initialized as a Git repository.")
    try:
        Repo.init(str(vault_path))
        install_pre_push_hook(vault_path)
    except exc.GitCommandError as e:
        raise Exception(f"Failed to initialize repository: {str(e)}")

def init_remote(vault_path: Path, source_uri: str):
    """Clone a logic vault from a remote origin."""
    if (vault_path / ".git").exists():
        raise Exception("Vault is already initialized as a Git repository.")
    try:
        Repo.clone_from(source_uri, str(vault_path))
        install_pre_push_hook(vault_path)
    except exc.GitCommandError as e:
        raise Exception(f"Failed to clone repository: {str(e)}")

def sync_vault(vault_path: Path):
    """Commit local changes and push/pull to keep the vault up to date."""
    try:
        repo = Repo(str(vault_path))
    except exc.InvalidGitRepositoryError:
        raise Exception("Current directory is not a Git repository. Run savile init first.")

    # Add all changes
    repo.git.add(all=True)
    
    # Commit if dirty
    if repo.is_dirty() or repo.untracked_files:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        repo.index.commit(f"savile sync: autocommit at {timestamp}")

    if not repo.remotes:
        return "No remotes configured. Local commit only."

    origin = repo.remotes.origin
    
    try:
        # Pull latest
        origin.pull()
        # Push our commits
        origin.push()
    except exc.GitCommandError as e:
        raise Exception(f"Sync failed during network operation: {str(e)}")
