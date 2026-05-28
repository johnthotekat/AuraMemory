# Contributing to AuraMemory 🧠🧬

Thank you for choosing to contribute to **AuraMemory**! We are building a visually elite, layerless, native cognitive memory operating layer for AI agents.

---

## ⚡ Core Development Philosophy

AuraMemory is engineered with rigid design boundaries to ensure premium performance and complete local autonomy:
1. **Process-Local Execution**: All memory vector calculations must execute in **< 0.1ms** directly in the process thread. Avoid slow network wrappers, external API calls, or middleware databases.
2. **Zero Dependencies**: Keep the engine 100% lightweight. We do not import heavy deep learning packages (`pytorch`, `transformers`, `numpy`). Stick to pure Python and JavaScript.
3. **Double-System Cognition**: Memory must follow human neuro-symbolic pathways: high-decay short-term Working Memory (System 1) and permanent associative networks (System 2).
4. **Visual Aesthetics**: All visual visualizers must maintain beautiful, glowing cyber-neon colors with interactive force-directed graph canvas animations to wow developers and VCs.

---

## 💻 Quick-Start Local Development

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/roniejosephv-star/AuraMemory.git
   cd AuraMemory
   ```
2. **Bootstrap the Sandbox Environment**:
   Run our zero-overhead update command inside `AuraMemory/` directory. It automatically initializes an isolated Python virtual environment (`.venv`), upgrades `pip`, and installs requirements:
   ```bash
   ./update.sh
   ```
3. **Execute Core Tests**:
   Ensure all local self-test suites compile perfectly:
   ```bash
   python3 core/cortex.py
   ```
4. **Validate MCP JSON-RPC gateways**:
   Test the Model Context Protocol stdio loops natively in milliseconds:
   ```bash
   python3 core/gateway.py --validate
   ```

---

## 🚀 Creating a Pull Request

- Always branch from `main` or create custom developer branches.
- Maintain clean, descriptive semantic commits (e.g. `feat(cortex): stabilized decay`).
- Before pushing, run the self-indexing crawler agent (`python3 agents/pusher.py`) to automatically update changelogs, highlights, and architecture reports.
