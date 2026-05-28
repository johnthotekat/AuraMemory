# AuraMemory Future Cognitive Roadmap 🔮🧬

AuraMemory is not merely a vector retrieval layer. It represents a continuous local operating substrate for agentic cognition. This document details our active progression timeline, incorporating modern neuro-symbolic and ahead-of-time (AOT) compiler paradigms.

---

## 📊 Evolutionary Phases

### 🟢 Phase 1: Local Foundation (Milestone A) - [COMPLETED]
- **Dual-System Brain Model**: Created ephemeral, high-decay System 1 (Working Memory) and permanent, non-decaying System 2 (Long-Term Memory).
- **Zero-Dependency 8D Vector space**: Implemented pure-Python continuous bag-of-words centroid representations blending tag and text context.
- **Morphological Stemmer Fallbacks**: Built-in regex stemmers for plural, gerund, and substring match calculations with zero external libraries.
- **Real-Time Guardrails**: Schema PII scrubbing (Emails, API Keys, Cards) and restriction block gates intercepting entries before storage.

### 🟡 Phase 2: Enterprise Scaling & Tooling - [COMPLETED]
- **Sub-Linear KD-Tree Index**: Mapped an $O(\log N)$ KD-Tree index, implementing hyperplane distance pruning to bypass linear scan latency for large node sizes.
- **Multi-Domain Vocab Profiles**: Added profiles for Tech/Startup, Medical, and Agriculture domains to enable dynamic semantic matching across diverse fields.
- **Model Context Protocol (MCP) Server**: Zero-dependency gateway (`core/gateway.py`) supporting Claude Desktop Co-work standard stdio transport.
- **Context Optimizer**: Token-Compressed prompt injection capping JSON context payloads up to **75% denser** than raw database chunks.

### 🔵 Phase 3: AOT Knowledge Compiler ("LLM Wiki" Vault) - [ACTIVE IN WORKSPACE]
- **Obsidian Markdown Bridge**: Programmatically serialize consolidated System 2 memory assets into structured Markdown (`.md`) vault folders natively.
- **Continuous-to-Symbolic Bracket Linker**: Automatically write double-bracketed `[[wikilinks]]` between pages if their process 8D cosine similarity $\ge 0.20$, bridging connectionist vector spaces and symbolic web graphs.
- **Factual Contradiction Linter (`auramem_lint`)**: Design background agent daemons executing self-reflection to resolve facts anomalies and merge redundant nodes.

### 🟣 Phase 4: Distilled Local Deep Learning - [FUTURE STRATEGY]
- **Compressed ONNX Embedded Models**: Distill small SentenceTransformer models (~60MB - 80MB) running via ONNX Runtime inside the local process thread.
- **Dynamic Semantic Vector Scaling**: Dynamically expand vocabulary dimensions through ongoing reading loops without requiring dictionary hardcodes.
- **Hardware Acceleration**: Enable metal/webGPU bindings for local vector math optimizations on portable edge devices.
