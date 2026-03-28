import pytest
import os
from pathlib import Path
import shutil
from savile.mcp.server import call_tool_handler, get_prompt_handler

@pytest.fixture
def mock_vault(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "personas").mkdir()
    (vault / "frameworks").mkdir()
    return vault

@pytest.mark.asyncio
async def test_vulnerability_argument_type_validation(mock_vault):
    """V9: Missing Type Validation on Arguments"""
    # Should return an error TextContent, not throw an unhandled exception crashing the server
    try:
        results = await call_tool_handler(mock_vault, "read_logic_module", None)
        assert len(results) == 1
        assert "Error" in results[0].text
    except AttributeError:
        pytest.fail("Server crashed due to unhandled NoneType argument. Missing type validation.")

    try:
        results = await call_tool_handler(mock_vault, "read_logic_module", ["invalid", "list"])
        assert len(results) == 1
        assert "Error" in results[0].text
    except AttributeError:
        pytest.fail("Server crashed due to unhandled List argument. Missing type validation.")

@pytest.mark.asyncio
async def test_vulnerability_symlink_path_traversal(mock_vault, tmp_path):
    """V1: Path Traversal Bypass (Symlinks)"""
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("SUPER_SECRET_TOKEN")
    
    symlink_path = mock_vault / "personas" / "malicious.md"
    os.symlink(secret_file, symlink_path)
    
    results = await call_tool_handler(mock_vault, "read_logic_module", {
        "category": "personas",
        "name": "malicious.md"
    })
    
    # Enforce that it explicitly blocks symlinks pointing outside the vault
    assert len(results) == 1
    assert "SUPER_SECRET_TOKEN" not in results[0].text, "Path traversal vulnerability: Able to read arbitrary files via symlink"
    assert "Error:" in results[0].text

@pytest.mark.asyncio
async def test_vulnerability_implicit_cwd_pollution(mock_vault, tmp_path):
    """V7: Implicit CWD Dependency"""
    persona_file = mock_vault / "personas" / "pollution_test.md"
    persona_file.write_text("---\ndescription: Test\n---\nContent")
    
    random_dir = tmp_path / "random_dir"
    random_dir.mkdir()
    original_cwd = os.getcwd()
    os.chdir(random_dir)
    
    try:
        results = await call_tool_handler(mock_vault, "install_logic_module", {
            "category": "personas",
            "name": "pollution_test.md",
            "target_type": "workflow"
        })
        
        # The tool should install the file relative to the vault root, NOT the current working directory
        # If it uses Path.cwd(), it will pollute random_dir.
        target_file = mock_vault / ".agent" / "workflows" / "pollution_test.md"
        assert target_file.exists(), "Installation target should be relative to the vault_path, not CWD"
        assert not (random_dir / ".agent").exists(), "Vulnerability: Tool pollutes arbitrary current working directories instead of using vault context."
    finally:
        os.chdir(original_cwd)

@pytest.mark.asyncio
async def test_vulnerability_silent_overwrite(mock_vault, tmp_path):
    """V5: Silent File Overwrites"""
    persona_file = mock_vault / "personas" / "overwrite_test.md"
    persona_file.write_text("---\ndescription: Test\n---\nContent")
    
    project_dir = mock_vault
    
    # Pre-create an existing file that the user might have customized
    target_dir = project_dir / ".agent" / "workflows"
    target_dir.mkdir(parents=True)
    existing_file = target_dir / "overwrite_test.md"
    existing_file.write_text("USER_CUSTOM_WORKFLOW_DO_NOT_OVERWRITE")
    
    original_cwd = os.getcwd()
    os.chdir(project_dir)
    
    try:
        results = await call_tool_handler(mock_vault, "install_logic_module", {
            "category": "personas",
            "name": "overwrite_test.md",
            "target_type": "workflow"
        })
        
        # It should either fail with an error or require a force flag.
        # Currently it silently clobbers. We assert it does NOT clobber.
        assert existing_file.read_text() == "USER_CUSTOM_WORKFLOW_DO_NOT_OVERWRITE", "Vulnerability: Tool silently clobbers existing user files without warning or force flag."
    finally:
        os.chdir(original_cwd)

@pytest.mark.asyncio
async def test_vulnerability_bad_frontmatter_parsing(mock_vault, tmp_path):
    """V8: Inadequate Frontmatter Parsing"""
    bad_md = mock_vault / "personas" / "bad.md"
    # No starting frontmatter, just a random horizontal rule in the content
    bad_md.write_text("# Hello\n\nSome text.\n\n---\n\ninvalid_yaml: @@@\n")
    
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Should not crash the server with yaml parsing errors
        results = await call_tool_handler(mock_vault, "install_logic_module", {
            "category": "personas",
            "name": "bad.md",
            "target_type": "workflow"
        })
        assert len(results) == 1
        # If it didn't crash, it passed.
    finally:
        os.chdir(original_cwd)

@pytest.mark.asyncio
async def test_vulnerability_duplicate_names(mock_vault):
    """V10: Duplicate Module Names shadowing"""
    (mock_vault / "personas" / "dup.md").write_text("Persona Dup")
    (mock_vault / "frameworks" / "dup.md").write_text("Framework Dup")
    
    # We should be able to specifically request the framework version via arguments
    result = await get_prompt_handler(mock_vault, "dup", {"category": "frameworks"})
    assert "Framework Dup" in result.messages[0].content.text, "Vulnerability: Cannot access framework if persona shares the same name (Namespace Shadowing)"
