# Changelog: AuraMemory Chronicles of Breaks & Achievements

All notable changes to the AuraMemory cognitive memory module will be documented in this file.

---
## [1.1.1] - 2026-05-27: Release v1.1.1

### 🚀 Achievements & Added Features
* **Feature**: Added interactive basic and guardrail usage examples

### 💥 Breaks & Bug Fixes
* **Fixed**: Resolved remote origin authentication boilerplate rejections

### ⚙️ Refactors & Updates
* **Update**: Updated README.md quick-start blocks and integrated automated release management inside pusher agent

---
## [1.1.0] - 2026-05-27: Milestone A (Local Semantic Vector Embeddings)

This release represents a massive cognitive leap: transitioning the memory association and recall systems from rigid, exact tag containment matching to a native, zero-dependency **8-Dimensional Semantic Vector Space model** executing 100% locally.

### 🚀 Achievements & Added Features
* **8D Semantic Embedding space**: Defined a custom continuous bag-of-words centroid vector model.
* **Morphological Stemming Fallbacks**: Native subword and plural/gerund stemming support (no NLP dependencies required).
* **Cosine Similarity Integration**: Standard dot-product cosine similarity formula mapped directly to node links and visual spring attraction.
* **Tag & Content Blending**: Memory nodes calculate vectors by blending tag words (70% weight) and content words (30% weight) to incorporate deeper textual context.
* **Process-Local Execution**: Runs entirely in process memory. Vector computation takes **< 0.1ms**, removing vector DB latency (50-200ms).
* **Multi-Module Workspace Restructure**: Reorganized repository files into a standard package architecture:
  * `core/cortex.py` (Core Python cognitive engine)
  * `agents/watcher.py` (Autonomous conversation analytics agent)
  * `agents/pusher.py` (Self-reflective Git pusher CLI tool)
  * `visuals/` (Canvas forces visualizer interface)
  * `reports/` (Study analysis documentation)
  * `data/` (JSON channels)

### 💥 Breaks & Path Corrections
* **Path Alignment**: Corrected `visuals/app.js` and `agents/watcher.py` relative paths to fetch and write to `data/watcher_data.json` and `reports/agentic_memory_report.md` cleanly across directories.
* **Exact Tag Heuristic Pruned**: Removed the original tag intersection algorithm. The memory layer now successfully associates nodes discussing semantically related topics (e.g., *"neural network"* automatically linking to *"AI Architecture"*) even if they share zero identical keyword tags!

---

## [1.0.0] - 2026-05-26: Initial Release

Initial bootstrap of the AuraMemory concept.

### 🚀 Achievements
* **Dual-System Cognitive Memory**: Implemented fast-decaying System 1 (Working Memory) and permanent System 2 (Long-Term Associative Memory).
* **Layerless Configurable Guardrails**: Embedded active safety scrubbing (PII scrubbing) and sensitive topic blocks intercepting inputs at the cognitive gates.
* **Glassmorphic Canvas Visualizer**: Designed 2D HTML5 canvas with spring-physics simulation rendering node systems, strengths, and decay rates live.
* **Conversation Watcher**: Built autonomous crawler parsing sessions to generate viral marketing captions.
