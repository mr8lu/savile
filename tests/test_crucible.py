import pytest
import shutil
from pathlib import Path
from savile.evals import crucible

def test_crucible_evaluations(tmp_path):
    vault_dir = tmp_path / "test-vault"
    vault_dir.mkdir()
    
    evals_dir = vault_dir / "evals"
    evals_dir.mkdir()
    
    # Copy mock yaml
    mock_yaml = Path(__file__).parent / "mock_eval.yaml"
    shutil.copy(mock_yaml, evals_dir / "mock_eval.yaml")
    
    # Run eval
    success = crucible.run_evaluations(vault_dir)
    assert success == True
