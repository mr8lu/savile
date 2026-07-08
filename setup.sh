#!/bin/bash

# SAVILE: Environment Standardization & Onboarding Setup Script
# Purpose: Guide the user to standardise their environment, install tools, and verify the installation.

set -e

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${BLUE}${BOLD}     SAVILE Environment Standardization & Onboarding${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}\n"

# 1. Dependency Checks
echo -e "${BOLD}[1/4] Checking System Prerequisites...${NC}"

# Check Git
if command -v git &> /dev/null; then
    echo -e "  - Git: ${GREEN}Detected (${NC}$(git --version)${GREEN})${NC}"
else
    echo -e "  - Git: ${RED}Not Found!${NC} Please install Git."
    exit 1
fi

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 11 ]; }; then
        echo -e "  - Python3: ${RED}Detected version $PYTHON_VERSION but SAVILE requires Python >= 3.11${NC}"
        exit 1
    else
         echo -e "  - Python3: ${GREEN}Detected version $PYTHON_VERSION (Compatible)${NC}"
    fi
else
    echo -e "  - Python3: ${RED}Not Found!${NC} Please install Python >= 3.11."
    exit 1
fi

# Check UV (recommended workspace manager)
if command -v uv &> /dev/null; then
    echo -e "  - uv: ${GREEN}Detected (${NC}$(uv --version)${GREEN})${NC}"
else
    echo -e "  - uv: ${YELLOW}Not Found! (Highly Recommended)${NC}"
    echo -e "    Installing 'uv' package manager speeds up dependency resolution by 10-100x."
    echo -e "    Would you like to install 'uv' now via curl?"
    read -p "    Install uv? (y/N): " INSTALL_UV
    if [[ "$INSTALL_UV" =~ ^[Yy]$ ]]; then
        echo -e "    ${BLUE}Installing uv...${NC}"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        # Source cargo env if applicable
        if [ -f "$HOME/.local/bin/env" ]; then
            source "$HOME/.local/bin/env"
        fi
        # Add to PATH for the rest of the script
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo -e "    ${RED}Proceeding without uv. You must have pip/venv set up manually.${NC}"
        exit 1
    fi
fi

# 2. Virtual Environment & Dependencies Setup
echo -e "\n${BOLD}[2/4] Setting Up Python Virtual Environment...${NC}"
if [ ! -d ".venv" ]; then
    echo -e "  - Creating virtual environment using uv..."
    uv venv
else
    echo -e "  - Virtual environment (.venv) already exists."
fi

echo -e "  - Syncing project dependencies (including development and optional groups)..."
uv sync --all-extras --all-groups
echo -e "  - ${GREEN}Environment synchronized successfully!${NC}"

# 3. Test Verification
echo -e "\n${BOLD}[3/4] Verifying System Correctness...${NC}"
echo -e "  - Running the unit/E2E test suite via pytest..."
if uv run pytest; then
    echo -e "  - Test Suite: ${GREEN}PASSED! (All logical assertions verified)${NC}"
else
    echo -e "  - Test Suite: ${RED}FAILED!${NC} Please check the logs above."
    exit 1
fi

# 4. Interactive BMAD Framework Link
echo -e "\n${BOLD}[4/4] Linking BMAD-METHOD framework...${NC}"
if [ -L ".bmad-core" ] || [ -d ".bmad-core" ]; then
    echo -e "  - .bmad-core framework configuration link already detected. ${GREEN}(Standardised)${NC}"
else
    echo -e "  - BMAD-METHOD framework was not detected inside the vault."
    read -p "    Would you like to install and link the BMAD-METHOD framework now? (y/N): " LINK_BMAD
    if [[ "$LINK_BMAD" =~ ^[Yy]$ ]]; then
        bash ./scripts/setup-bmad.sh
    else
        echo -e "    ${YELLOW}Skipped linking. You can run './scripts/setup-bmad.sh' at any time to link later.${NC}"
    fi
fi

# Summary / Next Steps
echo -e "\n${BLUE}${BOLD}====================================================${NC}"
echo -e "${GREEN}${BOLD}     🎉 SAVILE IS FULLY STANDARDISED & READY!${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}\n"
echo -e "You can now run SAVILE commands via '${BOLD}uv run savile${NC}':"
echo -e "  - ${BOLD}uv run savile --help${NC}                   View CLI usage and available commands"
echo -e "  - ${BOLD}uv run savile serve --sse --port 8000${NC}   Start SSE Server (e.g. for Warp AI)"
echo -e "  - ${BOLD}./scripts/run-mcp.sh -h${NC}                Show MCP config blocks for Claude, Cursor, Warp, etc."
echo -e "\nAll agentic tool instruction rules (.cursorrules, .clinerules, .windsurfrules, .copilotinstructions)"
echo -e "have been pre-configured to keep your workspace aligned with root ${BOLD}GEMINI.md${NC} requirements."
