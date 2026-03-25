import os
import shutil
from pathlib import Path
from savile.core import registry

def test_scaffold_local_vault(tmp_path):
    vault_dir = tmp_path / "test-vault"
    vault_dir.mkdir()
    registry.scaffold_local_vault(vault_dir)

    assert (vault_dir / "personas").exists()
    assert (vault_dir / "personas" / ".gitkeep").exists()
    assert (vault_dir / "frameworks").exists()
    assert (vault_dir / "evals").exists()
