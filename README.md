# 🧠 AuraMemory: Layerless Native Cognitive AI Memory Module

Welcome to **AuraMemory**, a next-generation cognitive memory engine designed to let AI agents interact with memory *natively* and *securely* without slow database middleware wrappers (like standard Vector DB APIs), backed by a schema-configurable guardrail system and a process-local continuous semantic vector space.

To launch this as a viral, high-reach social media brand, this workspace includes an interactive, gorgeous force-directed graph dashboard, alongside an autonomous **Conversation Watcher Agent** and a self-reflective **Git Pusher CLI Tool**.

---

## ⚡ The Architecture: Dual-System Cognitive Brain

Standard RAG architectures use an external Vector Database. This introduces latency, breaks native LLM context attention loops, and stores junk interactions. AuraMemory mirrors human cognitive neuroscience by separating memory into two systems and encoding them in a lightweight 8D Semantic Vector space:

```
                  ┌───────────────────────────────┐
                  │      Incoming Interaction     │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │   Configurable Guardrails     ├───────► [Blocked Category] 
                  │  (PII Scrubbing & Filtering)  │         (Entry REJECTED!)
                  └──────────────┬────────────────┘
                                 │ (Passed)
                                 ▼
                  ┌───────────────────────────────┐
                  │ System 1: Working Memory      │ ◄─────► [8D Semantic CosSim Links]
                  │ (Ephemeral, High-Decay nodes)  │
                  └──────────────┬────────────────┘
                                 │
                    [Consolidation Cycle Run]
                                 │
                                 ├─── (Cognitive Score < 0.60) ──► [Decayed / Deleted]
                                 │
                                 └─── (Cognitive Score >= 0.60) ──► Promoted
                                 
                                 ▼
                  ┌───────────────────────────────┐
                  │ System 2: Long-Term Memory    │
                  │ (Permanent Associative Nodes) │
                  └───────────────────────────────┘
```

1. **System 1 (Working Memory):** Captures immediate interactions. Nodes possess a `strength` rating that decays over time. If a node is repeatedly accessed or deemed highly important, its score increases.
2. **System 2 (Long-Term Memory):** Persistent, non-decaying knowledge structure. Nodes consolidate and bind via semantic associations using 8D vector cosine similarities.
3. **Layerless Guardrails:** Validates information *at the gates*. A schema scrubs PII patterns (Emails, API Keys, Cards) and rejects blocked categories before the agent encodes them.
4. **8-Dimensional Continuous Semantic Space**: Every node and search query is converted into an 8D concept vector based on a local, zero-dependency vocabulary matrix with stemming and substring fallbacks. Node links are formed automatically if cosine similarity $\ge 0.20$.

---

## 💻 Repository Blueprint

AuraMemory is structured into a clean, multi-module workspace:

```
AuraMemory/ (Git Repository Root)
├── core/
│   ├── __init__.py
│   └── cortex.py                  # Core dual-system memory engine
├── agents/
│   ├── __init__.py
│   ├── watcher.py                 # Crawler log analyzer agent
│   └── pusher.py                  # Self-reflective CLI Git pusher agent
├── visuals/
│   ├── index.html                 # Canvas simulation dashboard
│   ├── index.css                  # Custom styling and glows
│   └── app.js                     # Frontend controller
├── reports/
│   ├── architecture_specification.md # Architectural tradeoffs report
│   └── agentic_memory_report.md   # Social outreach report
├── data/
│   └── watcher_data.json          # Compiled JSON insights
├── README.md                      # Inner documentation
└── CHANGELOG.md                   # Chronicles of breaks & achievements
```

---

## 📸 The 30-Day Instagram "Userjourney" Startup Playbook

You want to monetize this and attract networking and venture capital (VC) investment. Here is your step-by-step funnel strategy:

1. **The Hook (Reel video):** Record a screen capture of the visuals dashboard floating. Type a secret password like `token_987654321` into the console, hit Commit, and show the console scrubbing it into `<API_KEY_SCRUBBED>`. Then search for *"machine learning"* and film the canvas pulsing *"AI Architecture"* nodes because of **semantic vector embeddings similarity**, even with zero exact tag overlaps!
2. **The Education (Caption / Carousel):** Explain that standard Vector DBs are dead because local process embeddings process memory in **< 0.1ms**, reducing API overhead.
3. **The Call-to-action (CTA):** *“Want to build native AI brains that think like humans? Comment 'MEMORY' and I'll send you the full open-source Python code and visualizer directly!”*
4. **The Conversion:** By giving away high-quality engineering value, you build a targeted community of developers, founders, and VCs looking for agentic memory solutions.

---

## 🚀 Running the Project Locally

### 1. Execute Self-Tests & Verify python engine
Run unit test suites on the core cognitive engine, including semantic similarity checks:
```bash
python3 core/cortex.py
```

### 2. Crawl Logs & Refresh Instagram Content
Run the Watcher Agent to parse new conversation logs, updating the dashboard's social panel dynamically:
```bash
python3 agents/watcher.py
```

### 3. Launch the Premium Visualizer Dashboard
Start a lightweight local server to open the glassmorphism visualizer:
```bash
python3 -m http.server 8000 --directory visuals/
```
Then, open your browser and navigate to: **[http://localhost:8000](http://localhost:8000)**.
Drag nodes, simulate inputs, adjust guardrails, and recall memories semantically!

### 4. Push Updates Natively
Run the self-reflective Git Pusher Agent to analyze local repository changes and format structural commits:
```bash
python3 agents/pusher.py
```
