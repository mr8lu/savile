import os
import shutil
import tempfile
import yaml
from pathlib import Path
from git import Repo, exc

def extract_frontmatter(content: str):
    """Extracts YAML frontmatter from a markdown string."""
    if not content.startswith("---"):
        return None
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
        
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

def validate_module(file_path: Path):
    """Validates that a module follows the Winston Metadata Schema v1.0.0."""
    if not file_path.suffix == ".md":
        return False, "Module must be a Markdown file (.md)"
        
    with open(file_path, "r") as f:
        content = f.read()
        
    metadata = extract_frontmatter(content)
    if not metadata:
        return False, "Missing or invalid YAML frontmatter"
        
    required_fields = ["name", "version", "category"]
    for field in required_fields:
        if field not in metadata:
            return False, f"Missing required field: {field}"
            
    # Category validation
    category = metadata.get("category")
    parent_dir = file_path.parent.name
    
    if category == "persona" and parent_dir != "personas":
        return False, f"Persona category module must be in /personas, found in /{parent_dir}"
    if category == "framework" and parent_dir != "frameworks":
        return False, f"Framework category module must be in /frameworks, found in /{parent_dir}"
        
    return True, metadata

def add_remote_module(vault_path: Path, source_uri: str, alias: str = None):
    """Pulls logic from a remote repository and merges it into the local vault."""
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            Repo.clone_from(source_uri, tmpdir)
        except exc.GitCommandError as e:
            raise Exception(f"Failed to clone remote module: {str(e)}")
            
        tmp_path = Path(tmpdir)
        modules_added = []
        
        # Scan for .md files in personas/ and frameworks/
        for category_dir in ["personas", "frameworks"]:
            src_dir = tmp_path / category_dir
            if not src_dir.exists():
                continue
                
            for md_file in src_dir.glob("*.md"):
                is_valid, result = validate_module(md_file)
                if not is_valid:
                    print(f"Skipping invalid module {md_file.name}: {result}")
                    continue
                
                target_name = alias if alias and md_file.stem == alias else md_file.name
                target_path = vault_path / category_dir / target_name
                
                if target_path.exists():
                    # Simple conflict resolution: warn and skip or overwrite?
                    # For v1.0.0, we'll overwrite but warn.
                    print(f"Warning: Overwriting existing module {target_name}")
                
                shutil.copy2(md_file, target_path)
                modules_added.append(result.get("name"))
                
        return modules_added
