---
name: "🐛 Bug Report"
about: Report a system defect or test failure inside AuraMemory.
title: "bug: [Short description of issue]"
labels: ["bug", "triage"]
assignees: []
---

## 🐛 Bug Description
Provide a clear and concise description of the bug.

## 💻 Reproduction Steps
1. Initialize setup: `./update.sh`
2. Run test: `python3 core/cortex.py` or gateway validating: `python3 core/gateway.py --validate`
3. Witness failure in: [e.g. KD-Tree partition logic]

## 📋 Console Logs
```text
[Paste terminal failures here]
```

## ⚙️ Environment Details
- OS: [e.g. macOS 14.5]
- Python Version: [e.g. 3.11]
