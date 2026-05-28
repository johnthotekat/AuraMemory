#!/bin/bash
# Aura Memory: update.sh
# Next-generation Agentic Memory setup and update configurator script.

echo -e "\033[1;36m🚀 Bootstrapping upgraded Aura Memory framework...\033[0m"

# Perform core file replacement under interactive terminal permissions
if [ -f "core/cortex_upgrade.py" ]; then
    mv -f "core/cortex_upgrade.py" "core/cortex.py"
    echo -e "\033[1;32m✅ Swapped core/cortex.py with next-generation version.\033[0m"
fi

if [ -f "core/gateway_upgrade.py" ]; then
    mv -f "core/gateway_upgrade.py" "core/gateway.py"
    echo -e "\033[1;32m✅ Swapped core/gateway.py with next-generation version.\033[0m"
fi

# Perform visual GUI dashboard file replacement under interactive permissions
if [ -f "visuals/index_upgrade.html" ]; then
    mv -f "visuals/index_upgrade.html" "visuals/index.html"
    echo -e "\033[1;32m✅ Swapped visuals/index.html with next-generation GUI.\033[0m"
fi

# Ensure executable permissions are correct
chmod +x core/cortex.py core/gateway.py configurator.py 2>/dev/null

# Launch the interactive storage profiler questionnaire
python3 configurator.py

# Overwrite the old update.sh cleanly
if [ -f "update_new.sh" ]; then
    mv -f "update_new.sh" "update.sh"
    chmod +x update.sh 2>/dev/null
fi
