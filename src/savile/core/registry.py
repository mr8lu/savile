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


def import_from_system(vault_path: Path, name: str, alias: str = None, source_dir: Path = None) -> tuple[Path, Path]:
    """
    Imports a skill or agent from the system-wide ~/.gemini or ~/.agents directory
    (or a specified custom source directory) into the local vault's personas/ and frameworks/ folders.
    """
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError(f"Invalid name '{name}': Path traversal sequences are not allowed.")

    if source_dir:
        source_dir = Path(source_dir).expanduser()
        possible_paths = [
            source_dir / name / "SKILL.md",
            source_dir / f"{name}.md",
            source_dir / "skills" / name / "SKILL.md",
            source_dir / "agents" / f"{name}.md",
        ]
    else:
        home = Path.home()
        possible_paths = [
            home / ".gemini" / "skills" / name / "SKILL.md",
            home / ".agents" / "skills" / name / "SKILL.md",
            home / ".gemini" / "agents" / f"{name}.md",
        ]

    source_file = None
    for path in possible_paths:
        if path.is_file():
            source_file = path
            break

    if not source_file:
        search_locations = (
            str(source_dir) if source_dir else "~/.gemini/skills, ~/.agents/skills, ~/.gemini/agents"
        )
        raise ValueError(
            f"System skill or agent '{name}' not found in search paths ({search_locations})."
        )

    content = source_file.read_text()
    
    # Extract name and description from frontmatter
    from savile.core.protocol import extract_frontmatter
    metadata = extract_frontmatter(content) or {}
    if not isinstance(metadata, dict):
        metadata = {}
    
    import_name = alias or metadata.get("name") or name
    import_name = str(import_name).lower().strip()
    
    # Validate de-anthropomorphized naming
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
    if import_name in prohibited_names or not re.match(r"^[a-z0-9-]+$", import_name):
        raise ValueError(
            f"Invalid target name '{import_name}'. Names must be functional and de-anthropomorphized."
        )

    # Strip existing frontmatter from the main content for splitting
    main_content = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            main_content = parts[2].strip()

    # Split into Persona and Framework sections if a framework header is found
    # Commonly: "# Framework", "# Methodologies", "# Methodology", "# Method"
    framework_patterns = [
        r"(^|\n)#+\s+Framework\b",
        r"(^|\n)#+\s+Methodologies\b",
        r"(^|\n)#+\s+Methodology\b",
        r"(^|\n)#+\s+Method\b"
    ]
    
    persona_content = main_content
    framework_content = ""
    
    for pattern in framework_patterns:
        match = re.search(pattern, main_content, re.IGNORECASE)
        if match:
            split_idx = match.start()
            persona_content = main_content[:split_idx].strip()
            framework_content = main_content[split_idx:].strip()
            break

    personas_dir = vault_path / "personas"
    frameworks_dir = vault_path / "frameworks"
    
    personas_dir.mkdir(parents=True, exist_ok=True)
    frameworks_dir.mkdir(parents=True, exist_ok=True)
    
    p_file = personas_dir / f"{import_name}.md"
    f_file = frameworks_dir / f"{import_name}.md"
    
    # Construct YAML frontmatter for persona
    p_desc = metadata.get("description", f"Imported {import_name} persona")
    p_ver = metadata.get("version", "1.0.0")
    p_cat = "persona"
    
    p_meta = {"name": import_name, "version": p_ver, "category": p_cat, "description": p_desc}
    p_frontmatter = "---\n" + yaml.safe_dump(p_meta, sort_keys=False) + "---\n\n"
    p_file.write_text(p_frontmatter + persona_content + "\n")
    
    # Construct YAML frontmatter for framework
    f_ver = metadata.get("version", "1.0.0")
    f_cat = "framework"
    
    f_meta = {"name": import_name, "version": f_ver, "category": f_cat}
    f_frontmatter = "---\n" + yaml.safe_dump(f_meta, sort_keys=False) + "---\n\n"
    
    if framework_content:
        f_file.write_text(f_frontmatter + framework_content + "\n")
    else:
        # Scaffold an empty framework if none existed
        f_file.write_text(f_frontmatter + f"# Framework\n\nMethodologies for {import_name}.\n")

    return p_file, f_file
