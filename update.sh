#!/usr/bin/env bash
# AuraMemory Zero-Overhead Sync & Dependency Update Manager
# Automates Git synchronization, local python venv isolation, and package installer.

# Color escape codes for premium terminal layout
C_BLUE="\033[94m"
C_CYAN="\033[96m"
C_GREEN="\033[92m"
C_YELLOW="\033[93m"
C_RED="\033[91m"
C_PURPLE="\033[95m"
C_BOLD="\033[1m"
C_END="\033[0m"

echo -e "${C_PURPLE}${C_BOLD}======================================================================${C_END}"
echo -e "${C_PURPLE}${C_BOLD}    🧠⚙️ AURAMEMORY: ZERO-OVERHEAD AUTONOMOUS UPDATE MANAGER ⚙️🧠${C_END}"
echo -e "${C_PURPLE}${C_BOLD}======================================================================${C_END}"

# Resolve the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

# 1. Pull latest code from GitHub
if [ -d ".git" ]; then
    echo -e "🚀 ${C_BLUE}Fetching latest updates from GitHub...${C_END}"
    git pull origin main
    if [ $? -eq 0 ]; then
        echo -e "✅ ${C_GREEN}GitHub sync complete!${C_END}"
    else
        echo -e "⚠️ ${C_YELLOW}Git pull failed or branch was already up-to-date. Proceeding...${C_END}"
    fi
else
    echo -e "ℹ️ ${C_BLUE}Running in standalone package mode (Git not active in this subfolder).${C_END}"
fi

# 2. Check Python3 installation
if ! command -v python3 &> /dev/null; then
    echo -e "❌ ${C_RED}Error: Python3 is not installed or not in PATH.${C_END}"
    exit 1
fi

# 3. Handle Python virtual environment (.venv)
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "\n📦 ${C_CYAN}Initializing isolated local Python virtual environment (.venv)...${C_END}"
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo -e "✅ ${C_GREEN}Virtual environment created successfully! (System remains unpolluted)${C_END}"
    else
        echo -e "⚠️ ${C_YELLOW}Could not create venv automatically. Checking system dependencies...${C_END}"
    fi
fi

# 4. Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    echo -e "🔌 ${C_BLUE}Activating isolated local workspace environment...${C_END}"
    source "$VENV_DIR/bin/activate"
else
    echo -e "⚠️ ${C_YELLOW}Running using global system Python (venv not active).${C_END}"
fi

# 5. Upgrade pip and install package requirements autonomously
if [ -f "requirements.txt" ]; then
    echo -e "\n⚡ ${C_CYAN}Autonomously scanning package requirements...${C_END}"
    pip install --upgrade pip -q
    # Perform install silently unless an error occurs
    pip install -r requirements.txt -q
    if [ $? -eq 0 ]; then
        echo -e "✅ ${C_GREEN}Dependencies scanned & updated successfully! (Zero installation overheads)${C_END}"
    else
        echo -e "❌ ${C_RED}Failed to install packages in requirements.txt.${C_END}"
    fi
fi

# 6. Execute local self-validation loops to verify runtime health
echo -e "\n🛡️ ${C_PURPLE}Running cognitive and MCP gateway validation suite...${C_END}"

python3 core/cortex.py &> /dev/null
CORTEX_STATUS=$?

python3 core/gateway.py --validate &> /dev/null
GATEWAY_STATUS=$?

if [ $CORTEX_STATUS -eq 0 ] && [ $GATEWAY_STATUS -eq 0 ]; then
    echo -e "✅ ${C_GREEN}All system self-tests and MCP Gateway handshakes passed flawlessly!${C_END}"
    echo -e "\n${C_GREEN}${C_BOLD}======================================================================${C_END}"
    echo -e "${C_GREEN}${C_BOLD}  🎉 SUCCESS! AURAMEMORY UPDATE & AUTO-INSTALL COMPLETED!${C_END}"
    echo -e "${C_GREEN}${C_BOLD}======================================================================${C_END}"
    echo -e "🤖 Your Universal MCP JSON-RPC Gateway is fully prepared."
    echo -e "📁 Absolute path: ${C_CYAN}$SCRIPT_DIR/core/gateway.py${C_END}"
    echo -e "🔌 Connect to Claude Desktop or Cursor to begin co-working natively!"
else
    echo -e "❌ ${C_RED}System self-validation failed. Please review error logs in core/cortex.py.${C_END}"
    exit 1
fi
