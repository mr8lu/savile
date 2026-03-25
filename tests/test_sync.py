import pytest
import os
from pathlib import Path
from git import Repo
from savile.sync import manager
from savile.core import registry

def test_manager_sync_vault_local(tmp_path):
    vault_dir = tmp_path / "test-vault"
    vault_dir.mkdir()
    
    # Init empty repo
    repo = Repo.init(str(vault_dir))
    
    # Create some files via registry
    registry.scaffold_local_vault(vault_dir)
    
    # Should not throw any errors, commits locally
    res = manager.sync_vault(vault_dir)
    assert res == "No remotes configured. Local commit only."
    
    # Check that it's clean (no untracked files)
    assert not repo.is_dirty()
    assert not repo.untracked_files
