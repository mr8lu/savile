import os
import re
import shutil
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


def create_persona(vault_path: Path, name: str, description: str) -> tuple[Path, Path]:
    """
    Creates a new persona/function using strict de-anthropomorphized naming conventions.
    Returns a tuple of (persona_file_path, framework_file_path).
    Raises ValueError if validation fails.
    """
    name = name.lower().strip()

    # Enforce naming conventions
    prohibited_names = [
        "david",
        "john",
        "quinn",
        "alice",
        "bob",
        "paige",
        "sally",
        "pete",
        "winston",
    ]
    if name in prohibited_names or not re.match(r"^[a-z0-9-]+$", name):
        raise ValueError(
            f"Invalid agent name '{name}'. Agent names MUST be functional (e.g., 'ux-designer', 'qa'). Human-like names are prohibited by workspace rules."
        )

    personas_dir = vault_path / "personas"
    frameworks_dir = vault_path / "frameworks"

    if not personas_dir.exists():
        raise ValueError("Vault not initialized. Run `savile bootstrap` first.")

    p_file = personas_dir / f"{name}.md"
    f_file = frameworks_dir / f"{name}.md"

    if p_file.exists():
        raise ValueError(f"Persona '{name}' already exists.")

    p_file.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n# Identity\n\nYou are the {name}.\n"
    )
    if frameworks_dir.exists():
        f_file.write_text(
            f"---\nname: {name}\n---\n# Framework\n\nMethodologies for {name}.\n"
        )

    return p_file, f_file


def export_skills(vault_path: Path, out: Path, force: bool) -> list[Path]:
    """
    Compile and export logic into portable Vercel Labs SKILL.md format artifacts.
    Returns a list of exported skill file paths.
    Raises ValueError if vault is not found.
    """
    personas_dir = vault_path / "personas"
    frameworks_dir = vault_path / "frameworks"

    if not personas_dir.exists():
        raise ValueError("No logic vault found. Run `savile bootstrap` first.")

    if out.exists() and force:
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    exported_files = []
    for p_file in personas_dir.iterdir():
        if p_file.suffix == ".md" and p_file.name != ".gitkeep":
            name = p_file.stem
            skill_dir = out / name
            skill_dir.mkdir(exist_ok=True)
            skill_file = skill_dir / "SKILL.md"

            # Read persona content
            content = p_file.read_text()

            # Inject framework if it exists
            f_file = frameworks_dir / f"{name}.md"
            if f_file.exists():
                content += "\n\n" + f_file.read_text()

            # Compile to SKILL.md (Vercel Labs format requires frontmatter)
            if not content.startswith("---"):
                frontmatter = f"---\nname: {name}\ndescription: Functional {name} skill compiled by Savile\n---\n"
                content = frontmatter + content

            skill_file.write_text(content)
            exported_files.append(skill_file)

    return exported_files
