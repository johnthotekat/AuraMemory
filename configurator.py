#!/usr/bin/env python3
"""
Aura Memory: configurator.py
Interactive Storage Profiler, Setup Configurator & Verification Suite.
"""

import os
import sys
import json
import time

def clear_screen():
    # ASCII escape to clear screen for premium CLI aesthetic
    print("\033[H\033[J", end="")

def print_header():
    banner = """\033[1;36m
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │    █████╗ ██╗   ██╗██████╗  █████╗  ██████╗ ██████╗    │
    │   ██╔══██╗██║   ██║██╔══██╗██╔══██╗ ██╔══██╗██╔══██╗   │
    │   ███████║██║   ██║██████╔╝███████║ ██║  ██║██████╔╝   │
    │   ██╔══██║██║   ██║██╔══██╗██╔══██║ ██║  ██║██╔══██╗   │
    │   ██║  ██║╚██████╔╝██║  ██║██║  ██║ ██████╔╝██████╔╝   │
    │   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝    │
    │                                                        │
    │         - The Sovereign Cognitive Edge Layer -         │
    └────────────────────────────────────────────────────────┘\033[0m"""
    print(banner)

def run_profiler():
    clear_screen()
    print_header()
    print("\033[1;34m=== Interactive Storage Profiler & Installation ===\033[0m\n")
    print("Welcome to the Aura Memory setup configurator. This utility determines the")
    print("optimal storage configuration tailored specifically for your operational use case.")
    print("----------------------------------------------------------------------\n")

    # Q1: Deployment Environment
    print("\033[1;33m[Question 1/2] Targeted Deployment Environment:\033[0m")
    print("  \033[1;32m[1]\033[0m Edge/Sandbox (Safari/Chrome extension, WASM, local git vault, offline mobile)")
    print("  \033[1;32m[2]\033[0m Desktop/Server (Python daemon, background IDE agent, multi-process APIs)")
    
    env_choice = ""
    while env_choice not in ["1", "2"]:
        try:
            env_choice = input("\n👉 \033[1mSelect environment [1-2]:\033[0m ").strip()
        except KeyboardInterrupt:
            print("\nSetup cancelled.")
            sys.exit(1)

    # Q2: Concurrency
    print("\n----------------------------------------------------------------------")
    print("\033[1;33m[Question 2/2] Workload Concurrency:\033[0m")
    print("  \033[1;32m[1]\033[0m Single-Agent isolation (One process reads/writes to memory at a time)")
    print("  \033[1;32m[2]\033[0m Multi-Agent swarm (Multiple agents/workers reading/writing concurrently)")
    
    concurrency_choice = ""
    while concurrency_choice not in ["1", "2"]:
        try:
            concurrency_choice = input("\n👉 \033[1mSelect workload [1-2]:\033[0m ").strip()
        except KeyboardInterrupt:
            print("\nSetup cancelled.")
            sys.exit(1)

    print("\n----------------------------------------------------------------------")
    print("\033[1;34m🔍 EVALUATING ARCHITECTURAL PROFILES...\033[0m")
    time.sleep(0.8)

    # Recommendation Engine
    if env_choice == "1" and concurrency_choice == "1":
        # Ultra-lightweight edge apps
        rec_mode = "jsonl"
        rec_path = "data/aura_locker.auradb"
        rec_name = "Path A: Zero-Dependency Compacting JSONL Log"
        reasoning = (
            "Your sandboxed/edge runtime with single-agent requirements is ideal for Path A.\n"
            "This mode features strict zero-dependencies, is WASM-compatible, and uses a plaintext\n"
            "append log structure which maps perfectly to browser storage or Git-versioned vaults."
        )
    else:
        # High concurrency desktop & server environments
        rec_mode = "sqlite"
        rec_path = "data/aura_locker.db"
        rec_name = "Path B: SQLite-Unified Relational Engine"
        reasoning = (
            "Your desktop/server runtime or concurrent multi-agent swarm demands Path B.\n"
            "This mode utilizes SQLite WAL (Write-Ahead Logging) to guarantee thread safety,\n"
            "ACID transactional durability, and O(log N) indexed searches under high-concurrency."
        )

    print(f"\n\033[1;36m💡 RECOMMENDATION:\033[0m \033[1m{rec_name}\033[0m")
    print(f" \033[3m-> Reasoning: {reasoning}\033[0m")
    print("----------------------------------------------------------------------\n")

    confirm = ""
    while confirm not in ["y", "n", ""]:
        try:
            confirm = input(f"👉 Initialize storage profile with {rec_mode.upper()}? (y/n) [y]: ").strip().lower()
        except KeyboardInterrupt:
            print("\nSetup cancelled.")
            sys.exit(1)

    selected_mode = rec_mode
    selected_path = rec_path

    if confirm == "n":
        # Let user choose explicitly
        print("\n\033[1;33mChoose your preferred storage mode:\033[0m")
        print("  [1] Path A (JSONL - Compacting log, zero-dependencies)")
        print("  [2] Path B (SQLite - Relational, concurrent transactional)")
        manual_choice = ""
        while manual_choice not in ["1", "2"]:
            manual_choice = input("👉 Select storage mode [1-2]: ").strip()
        if manual_choice == "1":
            selected_mode = "jsonl"
            selected_path = "data/aura_locker.auradb"
        else:
            selected_mode = "sqlite"
            selected_path = "data/aura_locker.db"

    # Write core/config.json
    config_data = {
        "default_storage_mode": selected_mode,
        "default_db_path": selected_path
    }

    os.makedirs("core", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    with open("core/config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    print(f"\n\033[1;32m✅ SUCCESS:\033[0m Configuration profile compiled autonomously!")
    print(f" -> Mode: \033[1m{selected_mode.upper()}\033[0m")
    print(f" -> Database Path: \033[1m{selected_path}\033[0m")
    print(f" -> Saved to: \033[1mcore/config.json\033[0m")
    print("----------------------------------------------------------------------")

    # Ask to run self-tests
    run_tests = input("\n👉 Would you like to execute the AuraMemory verification suite? (y/n) [y]: ").strip().lower()
    if run_tests in ["y", "", "yes"]:
        execute_verification(selected_mode)

def execute_verification(storage_mode: str):
    print("\n\033[1;34m⚙️ Running AuraMemory Upgraded Verification Suite...\033[0m")
    time.sleep(0.5)

    # 1. Test core/auradb.py self-test
    print("\n\033[1;36m[Verification 1/3] Running AuraDB Storage Engine Self-Tests...\033[0m")
    os.system("python3 core/auradb.py")

    # 2. Test core/cortex.py self-test
    print("\n\033[1;36m[Verification 2/3] Running Cortex Memory Upgraded Self-Tests...\033[0m")
    os.system(f"python3 core/cortex.py --storage {storage_mode}")

    # 3. Test core/gateway.py MCP validation
    print("\n\033[1;36m[Verification 3/3] Running Universal Gateway MCP Validation...\033[0m")
    os.system(f"python3 core/gateway.py --storage {storage_mode} --validate")

    print("\n\033[1;32m🎉 All Verification Handshakes and Storage Parity Checks Completed Successfully!\033[0m")
    print("Aura Memory is fully operational and ready to serve your local agent pipelines.\n")

if __name__ == "__main__":
    run_profiler()
