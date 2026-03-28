#!/bin/bash

# SAVILE: BMAD-METHOD Automation Script
# Purpose: Automatically install and link the BMAD framework.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "--- SAVILE: BMAD-METHOD Automation Setup ---"

# 1. Check for Node.js and npx
if ! command -v npx &> /dev/null; then
    echo -e "${RED}Error: 'npx' (Node.js) is not installed.${NC}"
    echo "Please install Node.js (version 18+) from https://nodejs.org/"
    exit 1
fi

# 2. Ask for installation directory
DEFAULT_BMAD_PATH="$HOME/bmad"
echo -e "Where should BMAD-METHOD be installed?"
read -p "Path (default: $DEFAULT_BMAD_PATH): " BMAD_PATH
BMAD_PATH=${BMAD_PATH:-$DEFAULT_BMAD_PATH}

# 3. Create directory if it doesn't exist
mkdir -p "$BMAD_PATH"
cd "$BMAD_PATH"

# 4. Install BMAD-METHOD
echo -e "${GREEN}Installing BMAD-METHOD framework in $BMAD_PATH...${NC}"
# Use --yes to skip prompts if any
npx bmad-method install --yes

# 5. Link to SAVILE vault
VAULT_PATH=$(pwd -P) # Ensure we have the absolute path
SAVILE_ROOT=$(cd - > /dev/null && pwd)

echo -e "${GREEN}Linking .bmad-core to SAVILE vault at $SAVILE_ROOT...${NC}"
cd "$SAVILE_ROOT"

# Check if .bmad-core link already exists
if [ -L ".bmad-core" ] || [ -d ".bmad-core" ]; then
    echo "A .bmad-core already exists in this vault. Skipping link step."
else
    ln -s "$BMAD_PATH/.bmad-core" .bmad-core
    echo -e "${GREEN}✅ Successfully linked .bmad-core to $BMAD_PATH/.bmad-core${NC}"
fi

echo -e "\n${GREEN}--- Setup Complete! ---${NC}"
echo "You can now run 'savile serve' or 'savile evaluate'."
