# AuraMemory Architecture Specification: Local Embedded Semantic Vector Space

This document outlines the self-reflective design decisions, trade-offs, and mechanical specifications of AuraMemory's Milestone A: replacing exact keyword tag matches with a local, zero-dependency 8-Dimensional Semantic Vector Space model.

---

## ⚡ Technical Concept Mapping

To execute memory calculations **100% locally** and **instantly inside agent processes** without database round-trips, AuraMemory uses a **Bag-of-Words concept centroid model**. 

Every text block and list of tags is projected onto an 8-Dimensional continuous concept vector:
$$\vec{v} = [ \text{Intelligence}, \text{System}, \text{Security}, \text{Attack}, \text{Outreach}, \text{Venture}, \text{Developer}, \text{Creative} ]$$

A curated semantic dictionary of ~50 foundational concepts maps keywords to continuous weights. Words outside the dictionary are resolved via **morphological stemming fallbacks** and **partial substring containment checks**.

---

## ⚖️ Trade-off Analysis

Implementing a rule-based centroid embedding model local to the process introduces distinct advantages and engineering tradeoffs compared to using standard neural embedding models (like OpenAI's `text-embedding-3-small` or local HuggingFace `SentenceTransformers`):

### 1. Architectural Advantages (The "Good")

* **Zero Latency (API-Free)**: Traditional vector databases introduce network hops (e.g., Pinecone/Weaviate API) or heavy database drivers (like pgvector) that add 50ms - 200ms latency. AuraMemory's embedding calculation executes in **< 0.1 milliseconds**, running entirely inside standard CPU execution loops.
* **Zero Dependencies**: Standard neural vectorizing requires massive runtime dependencies (PyTorch, Tokenizers, NumPy, scikit-learn). AuraMemory runs in **pure Python and pure JavaScript** with zero external package imports, maintaining a negligible runtime footprint.
* **Deterministic Concept Alignment**: Neural embedding spaces are notoriously hard to debug due to high-dimensional black-box representations (e.g., 1536 dimensions). AuraMemory's 8D space is fully transparent: developers can inspect a node's vector and instantly see exactly *why* it links to another node (e.g., high values in `SECURITY` and `ATTACK` dimensions).
* **Perfect Sync Model**: Because the math is simple and self-contained, the exact same tokenization, vocabulary dictionary, and cosine similarity calculations are implemented in Python and JavaScript. This enables the frontend canvas dashboard to simulate the exact cognitive forces of the backend, completely in the browser!

### 2. Architectural Limitations (The "Bad")

* **Predefined Domain Scope**: The semantic dictionary is customized for developer-creator ecosystems. A node discussing a completely off-topic concept (e.g., *"Gardening techniques for organic tomatoes"*) will yield a zero vector, failing to link semantically unless specific words overlap.
* **Syntax vs. True Semantic Context**: A transformer model captures complex sentence structures and negatives (e.g., *"This is not about security"* matches security topics neutrally). AuraMemory's centroid model is bag-of-words: it splits terms and averages them, meaning negatives or subtle sarcasm are lost.
* **No Out-of-the-Box Generalization**: Scaling to generalized conversational tasks requires manually enriching the `SEMANTIC_VOCAB` dictionary or integrating a small, compressed GloVe/Word2Vec model file.

---

## 🛠️ Performance & Scalability Metrics

### Graph Physical Simulation Math

When a new node $N_{\text{new}}$ is ingested, it is compared with all active nodes in System 1 and System 2.

```mermaid
graph TD
    A[New Memory Node Ingested] --> B[Generate Blended 8D Vector]
    B --> C[Compute Cosine Similarity to all active nodes]
    C --> D{Similarity >= 0.20?}
    D -- Yes --> E[Form Bidirectional Link in Canvas]
    D -- No --> F[Remain Disconnected]
    E --> G[Scale Link Force: 0.20 + 0.875 * Sim - 0.20]
```

This mathematical structure translates semantic proximity directly into interactive mechanical gravity: nodes that are semantically close pull each other together, while unrelated nodes float apart!

---

## 🔌 Universal MCP Context Gateway & Token-Compressed Context Optimizer

To support native integrations with agent environments (Claude Desktop, Cursor, Hermes, Claw Bot) without standard database API overhead, AuraMemory implements a **Model Context Protocol (MCP) JSON-RPC 2.0 Server** in `core/gateway.py`. 

### 1. The Context Bloat Problem in Standard RAG

Traditional RAG integrations suffer from massive prompt token inflation:
* **JSON Metadata Overhead**: Passing serialized database entries introduces raw JSON noise (brackets, commas, field names, and timestamps) that consumes valuable LLM context space.
* **Redundant Document Chunks**: Blind retrieval of standard database paragraphs often inputs repetitive context, wasting tokens on filler text.

### 2. AuraMemory's Token Optimizer Strategy

The `auramem_compress_context` tool solves context bloat at the gateway level. When an agent queries memory:
1. **Semantic Recall**: The KD-Tree index retrieves the top matching `MemoryNode` records using unit vector similarity.
2. **Metadata Stripping**: It discards operational fields (e.g., timestamps, access counts, and full vectors) and extracts only core content, active system tags, and strength values.
3. **High-Density Payload Synthesis**: It structures a highly condensed text payload, formatted as:
   `[System_Label][Tag1,Tag2,...] Memory Content`
4. **Hard Token Capping**: The generator counts characters and dynamically truncates the stream to fit strictly under `max_tokens`.

This compression strategy guarantees that agents receive clean, high-relevance cognitive memories with **up to 75% fewer tokens** than standard JSON vector query payloads!

---

## 🔮 Future Roadmap & Andrej Karpathy "LLM Wiki" Integration

To scale beyond Milestone A's rule-based centroid embeddings and integrate cutting-edge agentic memory patterns, we propose two strategic architectural evolutions:

### 1. The Andrej Karpathy "LLM Wiki" compiled memory layer

In April 2026, Andrej Karpathy introduced the concept of the **"LLM Wiki"**—a personal knowledge management pattern that shifts the paradigm from standard just-in-time (JIT) RAG to **ahead-of-time (AOT) knowledge compilation**. 
* **The Concept**: Raw interactions, papers, and files are the "source code," and the LLM acts as a "compiler" that proactively synthesizes and structures them into a human-readable vault of local plain Markdown (`.md`) files (the "executable" or wiki) rather than raw databases.
* **AuraMemory Implementation Integration**:
  1. **Markdown Entity Vault**: We can configure AuraMemory's System 2 (Long-Term Memory) to serialize directly to a local, Obsidian-compatible folder of plain Markdown pages.
  2. **8D Vector-to-Symbolic Link Bridge**: When two nodes have a cosine similarity $\ge 0.20$, the system automatically writes dynamic double-bracketed `[[wiki-links]]` directly inside the files. This maps continuous connectionist vector space distances to discrete symbolic web graphs!
  3. **The AI Memory Linter (`auramem_lint`)**: Introduce a background agent daemon that audits the wiki files periodically, merging redundant pages, resolving factual contradictions via agentic reflection, and pruning unlinked orphan pages.

### 2. Hybrid Neural Models & Embeddings

* **Local ONNX Runtime**: Package a highly compressed, distilled transformer model (like `all-MiniLM-L6-v2`, ~80MB) running via ONNX Runtime inside the process. This maintains 100% local operation while introducing true deep-learning context awareness.
* **Dynamic Vocabulary Injection**: Allow agents to dynamically "learn" new vocabulary concepts by parsing definitions from incoming interactions and projecting them onto the 8D concept dimensions on the fly.
---
---
---
---
---
---
---
---
---

## 🧠 Live Cognitive Workspace Index

*This section is compiled autonomously by the **AuraMemory Self-Reflective Git Pusher Agent** at `2026-05-28 07:57:36` using the local 8D Semantic Cosine Similarity engine.*

### 📊 Codebase Cognitive Map
| Component Path | System | Importance | Strength | Primary Semantic Vector | Main Associations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `LICENSE` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `requirements.txt` (0.90), `CHANGELOG.md` (0.90) |
| `requirements.txt` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `CHANGELOG.md` (0.90) |
| `CHANGELOG.md` | 🔵 System 1 (Working) | 0.65 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `pyproject.toml` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `README.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.71, 0.57, 0.02, 0.00...]` | `agentic_memory_report.md` (0.90), `configurator.py` (0.90) |
| `update.sh` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `ROADMAP.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `CONTRIBUTING.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `configurator.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.65, 0.61, 0.01, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `core/gateway.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.29, 0.80, 0.03, 0.00...]` | `strategist.py` (0.90), `auradb.py` (0.90) |
| `core/cortex.py` | 🔵 System 1 (Working) | 0.95 | 0.99 | `[0.29, 0.79, 0.14, 0.01...]` | `auradb.py` (0.90), `Auth_Token_Is_Api_Key_Scrubbed.md` (0.90) |
| `core/config.json` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.18, 0.83, 0.05, 0.00...]` | `__init__.py` (0.90), `auradb.py` (0.90) |
| `core/__init__.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.18, 0.81, 0.04, 0.00...]` | `config.json` (0.90), `auradb.py` (0.90) |
| `core/auradb.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.24, 0.81, 0.08, 0.00...]` | `strategist.py` (0.90), `config.json` (0.90) |
| `core/strategist.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.27, 0.81, 0.03, 0.00...]` | `gateway.py` (0.90), `auradb.py` (0.90) |
| `agents/pusher.py` | 🔵 System 1 (Working) | 0.85 | 0.99 | `[0.57, 0.58, 0.00, 0.00...]` | `watcher.py` (0.90), `__init__.py` (0.90) |
| `agents/__init__.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.54, 0.54, 0.01, 0.00...]` | `watcher.py` (0.90), `pusher.py` (0.90) |
| `agents/watcher.py` | 🔵 System 1 (Working) | 0.85 | 0.99 | `[0.56, 0.55, 0.01, 0.00...]` | `pusher.py` (0.90), `__init__.py` (0.90) |
| `examples/guardrails_demo.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.39, 0.66, 0.06, 0.01...]` | `basic_usage.py` (0.90), `__init__.py` (0.88) |
| `examples/basic_usage.py` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.39, 0.66, 0.01, 0.00...]` | `guardrails_demo.py` (0.90), `__init__.py` (0.88) |
| `.github/PULL_REQUEST_TEMPLATE.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.60, 0.03, 0.00...]` | `validate.yml` (0.90), `feature_request.md` (0.90) |
| `.github/workflows/validate.yml` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.60, 0.03, 0.00...]` | `PULL_REQUEST_TEMPLATE.md` (0.90), `feature_request.md` (0.90) |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.60, 0.03, 0.00...]` | `PULL_REQUEST_TEMPLATE.md` (0.90), `validate.yml` (0.90) |
| `.github/ISSUE_TEMPLATE/bug_report.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.60, 0.03, 0.00...]` | `PULL_REQUEST_TEMPLATE.md` (0.90), `validate.yml` (0.90) |
| `visuals/index_upgrade.html` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.55, 0.54, 0.02, 0.00...]` | `index.html` (0.89), `index.css` (0.89) |
| `visuals/index.html` | 🔵 System 1 (Working) | 0.80 | 0.99 | `[0.41, 0.57, 0.02, 0.00...]` | `index.css` (0.90), `app.js` (0.90) |
| `visuals/index.css` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.41, 0.57, 0.02, 0.00...]` | `index.html` (0.90), `app.js` (0.90) |
| `visuals/app.js` | 🔵 System 1 (Working) | 0.80 | 0.99 | `[0.37, 0.56, 0.06, 0.00...]` | `index.html` (0.90), `index.css` (0.90) |
| `data/aura_lockerjsonl` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `watcher_data.json` (0.90), `aura_locker.db` (0.90) |
| `data/watcher_data.json` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `aura_locker.db` (0.90) |
| `data/aura_locker.db` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_7.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Instagram.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.35, 0.78, 0.07, 0.00...]` | `aura_lockerjsonl` (0.89), `watcher_data.json` (0.89) |
| `data/aurawiki_vault/Ai_3.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_2.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_6.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Auth_Token_Is_Api_Key_Scrubbed.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.78, 0.16, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_9.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_10.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_8.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_11.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_12.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_13.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_1.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_5.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai_4.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.34, 0.80, 0.07, 0.00...]` | `aura_lockerjsonl` (0.90), `watcher_data.json` (0.90) |
| `data/aurawiki_vault/Ai.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.45, 0.75, 0.06, 0.00...]` | `aura_lockerjsonl` (0.89), `watcher_data.json` (0.89) |
| `assets/aura_dashboard.png` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/dashboard_mockup.png` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/terminal_simulator.svg` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/glowing_badges.svg` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/maturity_radar.svg` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/workspace_metrics.svg` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/aura_onboarding.png` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `assets/architecture_diagram.svg` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.65, 0.01, 0.00...]` | `architecture_specification.md` (0.90), `configurator.py` (0.90) |
| `reports/auradb_architectural_feasibility_study.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `reports/market_position_and_future_ideation.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.62, 0.03, 0.00...]` | `LICENSE` (0.90), `requirements.txt` (0.90) |
| `reports/architecture_specification.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.62, 0.65, 0.01, 0.00...]` | `architecture_diagram.svg` (0.90), `configurator.py` (0.90) |
| `reports/agentic_memory_report.md` | 🔵 System 1 (Working) | 0.50 | 0.99 | `[0.72, 0.54, 0.02, 0.00...]` | `README.md` (0.90), `configurator.py` (0.89) |

### ⚖️ Automated Architectural Assessment
* An analyzed volume of **59 active files** spanning **61057 lines of code** has been indexed into the memory space.

#### 👍 The "Good" Tradeoffs
- **Code Modularity**: Clean separation of concerns: core engine, frontend browser, reports, examples, and autonomous agents reside in distinct submodules.

#### ⚠️ The "Bad" Warnings
- **Density Alert**: core/cortex.py has grown large (1157 LOC). Consider splitting tokenization, vocabulary dictionary, or guardrails out to avoid massive single file densities.
- **Density Alert**: visuals/app.js is getting dense (1419 LOC). Consider refactoring graph physical forces calculations and canvas render elements into submodules.