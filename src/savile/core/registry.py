import os
import yaml
from pathlib import Path

SAVILE_CONFIG_DIR = Path.home() / ".savile"
SAVILE_CONFIG_PATH = SAVILE_CONFIG_DIR / "config.yaml"

def get_config():
    if not SAVILE_CONFIG_PATH.exists():
        return {}
    with open(SAVILE_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f) or {}

def save_config(config_data):
    SAVILE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVILE_CONFIG_PATH, "w") as f:
        yaml.safe_dump(config_data, f)

def scaffold_local_vault(vault_path: Path):
    """Scaffolds the standardized directory structure for a logic vault."""
    (vault_path / "personas").mkdir(parents=True, exist_ok=True)
    (vault_path / "frameworks").mkdir(parents=True, exist_ok=True)
    (vault_path / "evals").mkdir(parents=True, exist_ok=True)
    
    # Create gitkeep or basic instructions
    (vault_path / "personas" / ".gitkeep").touch()
    (vault_path / "frameworks" / ".gitkeep").touch()
    (vault_path / "evals" / ".gitkeep").touch()
