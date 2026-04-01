# Contributing to SAVILE

Thank you for your interest in contributing to the SAVILE framework! We welcome all contributions that help improve our system for agentic versioning and evaluation.

## Getting Started

### Development Environment

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/mr8lu/savile.git
    cd savile
    ```
2.  **Initialize the Environment:**
    We recommend using a virtual environment and `pip` (or `uv` if preferred).
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    ```
3.  **Run the Tests:**
    Ensure everything is working correctly:
    ```bash
    pytest tests/
    ```

## Development Workflow

1.  **Create a New Branch:**
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  **Implement Changes:**
    Follow the architecture patterns described in `docs/architecture.md`.
3.  **Adhere to Coding Standards:**
    - Use `asyncio` for performance and non-blocking I/O.
    - Follow PEP8 and use clear typing.
    - Write comprehensive tests for new features.
4.  **Run the Crucible:**
    If your changes impact logic evaluation, ensure you've updated the `/evals` matrices and run `savile evaluate`.
5.  **Commit and Pull Request:**
    Ensure your commit messages are descriptive. Follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) standard where possible.

## Project Values

*   **Pragmatism:** Favor simple and stable solutions over complex abstractions.
*   **Privacy First:** All core execution and data storage must remain 100% local.
*   **Git-Native:** Respect the version-controlled state as the source of truth.

---

### Questions?
Open an issue or contact the project maintainers.
