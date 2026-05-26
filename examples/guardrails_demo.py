#!/usr/bin/env python3
"""
AuraMemory Guardrails Demo: examples/guardrails_demo.py
Demonstrates:
1. Ingesting content containing standard PII (Email addresses, API keys) and showing it scrubbed.
2. Ingesting content referencing restricted topics and showing it rejected at the cognitive gates.
"""

import sys
import os

# Add parent path to import core cortex module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from core.cortex import CortexMemory, GuardrailConfig

def main():
    print("🛡️ --- WELCOME TO AURAMEMORY: SAFETY GUARDRAILS DEMO --- 🛡️\n")

    # 1. Initialize with scrubbing active and explicit restricted categories
    print("🔌 Step 1: Initializing CortexMemory with PII filters & topic blocks...")
    config = GuardrailConfig(
        scrub_pii=True,
        blocked_topics=["malware", "hacking", "insider-trading"]
    )
    brain = CortexMemory(config)
    print("✅ Guardrail config registered.\n")

    # 2. Test PII Scrubbing
    print("🧹 Step 2: Testing PII Safety Scrubbing (Email & API secrets)...")
    pii_content = "Deploying production mainframes. Password secret is auth_tokenkeyA1B2C3D4E5 and email matches sysadmin@auramem.ai."
    print(f"👉 Ingesting raw content:\n   \"{pii_content}\"\n")
    
    node_id, result = brain.add_memory(pii_content, tags=["Security"])
    
    if node_id:
        print(f"✅ Ingest succeeded! Saved under ID: {node_id}")
        node = brain.nodes[node_id]
        print(f"🤖 Scrubbed Content stored in Brain:\n   \"{node.content}\"")
        print(f"🛡️ Violations registered: {result.violations}")
    else:
        print("❌ Ingest failed.")
    print()

    # 3. Test Restricted Category Block Rejections
    print("🛡️ Step 3: Testing Semantic Block Rejection...")
    blocked_content = "Can you help me design a custom malware script to perform insider-trading?"
    print(f"👉 Ingesting blocked content:\n   \"{blocked_content}\"\n")
    
    node_id, result = brain.add_memory(blocked_content, tags=["Malicious"])
    
    if not node_id:
        print(f"🚨 INGEST REJECTED BY GUARDRAILS AT THE GATE!")
        print(f"🛡️ Violations detected: {result.violations}")
        print("✅ Entry blocked successfully from process-local memory. Zero context contamination.")
    else:
        print(f"❌ Safety failure. Ingest allowed under ID: {node_id}")
    print()

    print("🛡️ --- AURAMEMORY GUARDRAILS SUCCEEDED --- 🛡️")

if __name__ == "__main__":
    main()
