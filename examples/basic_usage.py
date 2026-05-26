#!/usr/bin/env python3
"""
AuraMemory Basic Usage Example: examples/basic_usage.py
Demonstrates:
1. Initializing the CortexMemory engine.
2. Ingesting memory nodes into System 1 (Working Memory).
3. Querying memories semantically utilizing 8D vector cosine similarities (Milestone A).
4. Running a cognitive consolidation and decay cycle.
"""

import sys
import os

# Add parent path to import core cortex module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from core.cortex import CortexMemory, GuardrailConfig

def main():
    print("🧠 --- WELCOME TO AURAMEMORY: NATIVE COGNITIVE AGENTIC MEMORY --- 🧠\n")

    # 1. Initialize AuraMemory with standard guardrails
    print("🔌 Step 1: Initializing CortexMemory engine...")
    config = GuardrailConfig(
        scrub_pii=True,
        blocked_topics=["hacking", "malware"]
    )
    brain = CortexMemory(config)
    print("✅ Memory engine online.\n")

    # 2. Add memories to System 1 (Working Memory)
    print("📥 Step 2: Committing memories to working memory (System 1)...")
    
    # Ingest diverse memories
    mem1_id, _ = brain.add_memory(
        "AuraMemory implements a layerless dual-system memory engine directly in process memory.",
        tags=["AI", "Architecture", "Engineering"],
        importance=0.9
    )
    
    mem2_id, _ = brain.add_memory(
        "Vibrant, dark-mode glassmorphic visualizers with spring physics are excellent lead magnets.",
        tags=["Marketing", "Instagram", "Creative"],
        importance=0.5
    )
    
    mem3_id, _ = brain.add_memory(
        "Python and JavaScript packages must remain modular and strictly isolated from parent directories.",
        tags=["Engineering", "Git", "Modular"],
        importance=0.85
    )

    print(f"✅ Committed {len(brain.nodes)} active working memory nodes.")
    for nid, n in brain.nodes.items():
        print(f"  ⚡ Node [{n.system}] '{n.content[:50]}...' | Importance: {n.importance}")
    print()

    # 3. Recall semantically using continuous 8D vector cosine similarities (Milestone A)
    print("🔍 Step 3: Querying memory space semantically (No exact keyword matches!)")
    
    # We query for "neural machine learning code"
    # This query does NOT share any exact tags or text words with our first memory node,
    # but they share extremely close continuous concept vectors!
    query = "neural machine learning code"
    print(f"👉 Querying text: '{query}'...")
    
    matches = brain.recall(query_text=query)
    
    print(f"✅ Retrieved {len(matches)} matching memories:")
    for idx, match in enumerate(matches, 1):
        print(f"  [{idx}] Match (System: {match.system}, Access Count: {match.access_count})")
        print(f"      Content: \"{match.content}\"")
        print(f"      Tags: {match.tags}")
    print()

    # 4. Run a cognitive consolidation and decay cycle
    print("⚙️ Step 4: Initiating cognitive consolidation and decay cycle...")
    print("  * Nodes with high importance or access counts will be promoted to System 2 (Long-Term).")
    print("  * Transient working memory nodes will decay and eventually prune.")
    
    # Run consolidation with a standard decay factor
    promoted = brain.consolidate(decay_rate=0.20)
    
    print(f"✅ Consolidation complete. Promoted to System 2: {promoted}")
    print("\n📊 Current Cognitive Memory State:")
    for nid, n in brain.nodes.items():
        sys_type = "🔴 LONG-TERM (System 2)" if n.system == "long_term" else "🔵 WORKING (System 1)"
        print(f"  └─ [{sys_type}] Strength: {n.strength:.2f} | Accesses: {n.access_count} | Node: '{n.content[:50]}...'")

    print("\n🧠 --- AURAMEMORY BASIC DEMO SUCCEEDED --- 🧠")

if __name__ == "__main__":
    main()
