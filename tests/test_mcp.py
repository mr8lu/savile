import pytest
from pathlib import Path
import os
import shutil
from savile.mcp.server import (
    create_mcp_server, 
    list_prompts_handler, 
    get_prompt_handler, 
    call_tool_handler
)

@pytest.fixture
def mock_vault(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "personas").mkdir()
    (vault / "frameworks").mkdir()
    
    # Create a persona
    persona_file = vault / "personas" / "realist.md"
    persona_file.write_text("You are a realist.")
    
    # Create a framework
    framework_file = vault / "frameworks" / "review.md"
    framework_file.write_text("Code review checklist.")
    
    return vault

@pytest.mark.asyncio
async def test_list_prompts(mock_vault):
    prompts = await list_prompts_handler(mock_vault)
    assert len(prompts) == 2
    names = [p.name for p in prompts]
    assert "realist" in names
    assert "review" in names

@pytest.mark.asyncio
async def test_get_prompt(mock_vault):
    result = await get_prompt_handler(mock_vault, "realist", None)
    assert "You are a realist." in result.messages[0].content.text

@pytest.mark.asyncio
async def test_install_logic_module(mock_vault, tmp_path):
    # Change CWD to simulate project root
    project_root = tmp_path / "project"
    project_root.mkdir()
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Mock vault content with description
        (mock_vault / "personas" / "pm.md").write_text("---\ndescription: Product Manager\n---\nPM Logic")

        results = await call_tool_handler(mock_vault, "install_logic_module", {
            "category": "personas",
            "name": "pm.md",
            "target_type": "workflow"
        })
        
        assert len(results) == 1
        assert "Successfully installed" in results[0].text
        assert "Created Gemini CLI command" in results[0].text
        
        # Check .agent/ file
        target_file = project_root / ".agent" / "workflows" / "pm.md"
        assert target_file.exists()
        
        # Check .gemini/ command file
        toml_file = project_root / ".gemini" / "commands" / "pm.toml"
        assert toml_file.exists()
        toml_content = toml_file.read_text()
        assert 'description = "Product Manager"' in toml_content
        assert 'prompt = "/pm {{args}}"' in toml_content
        
    finally:
        os.chdir(original_cwd)

@pytest.mark.asyncio
async def test_read_logic_module_path_traversal(mock_vault):
    # Try to read something outside the vault
    results = await call_tool_handler(mock_vault, "read_logic_module", {
        "category": "personas",
        "name": "../../../etc/passwd" 
    })
    
    assert "Error" in results[0].text

