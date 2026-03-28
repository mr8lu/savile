# Adversarial Review Findings & Regression Tests
**Target:** `src/savile/mcp/server.py`
**Reviewer:** Quinn (Adversarial/General)

## Security Vulnerabilities & Implementation Flaws Identified

1. **Path Traversal Bypass (Symlinks) [V1]**: The path traversal protection relied on `resolve()`. Our tests confirm `resolve()` naturally defends against external symlinks on most OS implementations, but the protection strategy should be noted.
2. **Missing Type Validation (Crash Vectors) [V9]**: Unhandled `NoneType` and `list` arguments crash the server immediately because the inputs skip validation before `.get()` is called.
3. **Implicit CWD Pollution [V7]**: `install_logic_module` hardcodes `Path.cwd()`, causing the tool to dump `.agent` and `.gemini` folders into whatever arbitrary directory the MCP server was booted from, rather than the safe `vault_path`.
4. **Silent File Overwrites [V5]**: The installation tool blindly executes `shutil.copy2()`, clobbering existing custom user workflows without warning or requiring a `force` flag.
5. **Namespace Shadowing (Duplicates) [V10]**: If a Persona and Framework share the same filename, the `get_prompt` handler silently ignores the requested category and returns the Persona variant permanently.

## Automated QA Suite Delivered

I have written an aggressive, future-proof test suite encapsulating these exact vulnerabilities into `tests/test_mcp_adversarial.py`.

The test suite currently fails, properly exposing the broken implementations.

**Failing Assertions to Fix:**
- `test_vulnerability_argument_type_validation`
- `test_vulnerability_implicit_cwd_pollution`
- `test_vulnerability_silent_overwrite`
- `test_vulnerability_duplicate_names`

## Next Recommended Action
Hand off to `/dev` or `/architect` to implement the fixes for `src/savile/mcp/server.py` until the newly generated test suite passes.