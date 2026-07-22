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


def test_import_from_system(tmp_path, monkeypatch):
    # Set up mock home directory
    mock_home = tmp_path / "mock_home"
    mock_home.mkdir()

    # Mock Path.home to return our mock home
    monkeypatch.setattr(Path, "home", lambda: mock_home)

    # Create mock system skill
    system_skill_dir = mock_home / ".gemini" / "skills" / "test-skill"
    system_skill_dir.mkdir(parents=True)
    skill_file = system_skill_dir / "SKILL.md"

    skill_content = """---
name: "test-skill"
version: "1.0.0"
category: "persona"
description: "A mock skill for testing"
---

# Test Persona

This is the body of the test persona.

## Methodologies

This is the framework or methodology section.
"""
    skill_file.write_text(skill_content)

    # Run import_from_system
    vault_dir = tmp_path / "vault"
    vault_dir.mkdir()
    registry.scaffold_local_vault(vault_dir)

    p_file, f_file = registry.import_from_system(vault_dir, "test-skill")

    # Assertions
    assert p_file.exists()
    assert f_file.exists()

    p_content = p_file.read_text()
    f_content = f_file.read_text()

    assert "name: test-skill" in p_content
    assert (
        "description: 'A mock skill for testing'" in p_content
        or "description: A mock skill for testing" in p_content
    )
    assert "This is the body of the test persona." in p_content
    assert "This is the framework or methodology section." not in p_content

    assert "name: test-skill" in f_content
    assert "This is the framework or methodology section." in f_content
    assert "This is the body of the test persona." not in f_content


def test_import_from_system_custom_dir(tmp_path):
    custom_dir = tmp_path / "custom_agents"
    custom_dir.mkdir()

    skill_dir = custom_dir / "custom-skill"
    skill_dir.mkdir()

    skill_file = skill_dir / "SKILL.md"
    skill_content = """---
name: "custom-skill"
version: "2.1.0"
category: "persona"
description: "A custom directory skill"
---

# Custom Persona

Body here.

# Framework

Framework here.
"""
    skill_file.write_text(skill_content)

    vault_dir = tmp_path / "vault2"
    vault_dir.mkdir()
    registry.scaffold_local_vault(vault_dir)

    p_file, f_file = registry.import_from_system(
        vault_dir, "custom-skill", source_dir=custom_dir
    )

    assert p_file.exists()
    assert f_file.exists()

    assert (
        "version: '2.1.0'" in p_file.read_text()
        or "version: 2.1.0" in p_file.read_text()
    )
    assert "Custom Persona" in p_file.read_text()
    assert "Framework" in f_file.read_text()
