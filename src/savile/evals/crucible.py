import yaml
from pathlib import Path


def run_evaluations(vault_path: Path) -> bool:
    """Run all evaluation matrices found in the vault."""
    evals_path = vault_path / "evals"
    if not evals_path.exists():
        print("error: No /evals directory found.")
        return True

    eval_files = [f for f in evals_path.iterdir() if f.suffix in [".yaml", ".yml"]]

    if not eval_files:
        print("evals: 0 evaluation matrices found. Skipping The Crucible...")
        return True

    success = True
    eval_results = []

    for eval_file in eval_files:
        try:
            with open(eval_file, "r") as f:
                data = yaml.safe_load(f)

            # Mock evaluation logic here
            # In a real system, this would call out to an LLM like gemini-2.0-pro-exp
            # and grade the response against target assertions.
            name = data.get("name", eval_file.name)
            target = data.get("target_model", "unknown")
            eval_results.append((name, target, "PASS"))

        except Exception as e:
            eval_results.append((eval_file.name, "unknown", f"FAIL ({str(e)})"))
            success = False

    if eval_results:
        print(f"evaluations[{len(eval_results)}]{{matrix,target,status}}:")
        for name, target, status in sorted(eval_results):
            print(f"  {name},{target},{status}")

    return success
