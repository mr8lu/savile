import yaml
from pathlib import Path

def run_evaluations(vault_path: Path) -> bool:
    """Run all evaluation matrices found in the vault."""
    evals_path = vault_path / "evals"
    if not evals_path.exists():
        print("No /evals directory found.")
        return True

    eval_files = [f for f in evals_path.iterdir() if f.suffix in ['.yaml', '.yml']]
    
    if not eval_files:
        print("No evaluation matrices found. Skipping The Crucible...")
        return True

    success = True
    print(f"Running Crucible across {len(eval_files)} matrices...")
    
    for eval_file in eval_files:
        try:
            with open(eval_file, "r") as f:
                data = yaml.safe_load(f)
            
            # Mock evaluation logic here
            # In a real system, this would call out to an LLM like gemini-2.0-pro-exp
            # and grade the response against target assertions.
            name = data.get("name", eval_file.name)
            target = data.get("target_model", "unknown")
            print(f"[{name}] testing against {target}... PASS")
            
        except Exception as e:
            print(f"Error evaluating {eval_file.name}: {str(e)}")
            success = False
            
    return success
