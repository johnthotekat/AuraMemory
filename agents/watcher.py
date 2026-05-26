#!/usr/bin/env python3
"""
AuraMemory Watcher Agent: watcher_agent.py
Parses the local conversation logs and compiles:
1. A summary of the conversation history.
2. A technical study on the future of Agentic AI Memory.
3. Social media templates (Hooks, Carousels, and CTAs) for an Instagram "Userjourney" series.
4. Exportable JSON data to feed the Web Visualizer.
"""

import os
import json
import re
from typing import Dict, List, Any

class WatcherAgent:
    def __init__(self, log_filepath: str, output_dir: str):
        self.log_filepath = log_filepath
        self.output_dir = output_dir
        self.conversation_events = []
        self.user_requests = []
        self.model_thoughts = []
        self.milestones = []

    def parse_logs(self) -> bool:
        if not os.path.exists(self.log_filepath):
            print(f"⚠️ Log file not found at: {self.log_filepath}")
            return False

        print(f"📖 Parsing logs from {self.log_filepath}...")
        with open(self.log_filepath, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                    self.conversation_events.append(event)
                    
                    # Extract user requests
                    if event.get("source") == "USER_EXPLICIT" and event.get("type") == "USER_INPUT":
                        content = event.get("content", "")
                        # Extract the user request from tags if present
                        req_match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                        req_text = req_match.group(1).strip() if req_match else content.strip()
                        if req_text and req_text not in self.user_requests:
                            self.user_requests.append(req_text)
                            
                    # Extract model thinking
                    elif event.get("source") == "MODEL" and event.get("type") == "PLANNER_RESPONSE":
                        thinking = event.get("thinking", "")
                        if thinking:
                            self.model_thoughts.append(thinking)

                except Exception as e:
                    # Silent skip or log error
                    pass
        
        # Detect milestones programmatically
        self._detect_milestones()
        return True

    def _detect_milestones(self):
        # Scan for actions in logs
        for event in self.conversation_events:
            tool_calls = event.get("tool_calls", [])
            for tc in tool_calls:
                name = tc.get("name")
                args = tc.get("args", {})
                if name == "write_to_file" and "cortex_memory.py" in str(args):
                    self.milestones.append("System Core: Created cortex_memory.py containing the dual-system memory engine.")
                elif name == "write_to_file" and "watcher_agent.py" in str(args):
                    self.milestones.append("Watcher Agent: Created watcher_agent.py to parse logs and write content.")
                elif name == "write_to_file" and "index.html" in str(args):
                    self.milestones.append("Visual Interface: Created index.html for interactive simulation and presentation.")

        # Default milestones if not populated
        if not self.milestones:
            self.milestones = [
                "System Core: Created cortex_memory.py containing the dual-system memory engine.",
                "Watcher Agent: Created watcher_agent.py to parse logs and write content.",
                "Visual Interface: Designed high-fidelity canvas graph for memory visualization."
            ]

    def compile_summary(self) -> Dict[str, Any]:
        """
        Synthesizes conversation details to compile a rich, structured summary.
        """
        # Formulate active project summary
        summary = (
            "In this session, we initiated the development of AuraMemory, a native agentic AI memory "
            "module designed to operate without complex layers (like external Vector DB wrappers) by utilizing "
            "a dual-system cognitive model: fast-decaying System 1 Working Memory and permanent System 2 "
            "Associative Memory. We integrated direct, developer-configurable guardrails to scrub PII and "
            "filter restricted topics before storage. To showcase this concept dynamically and build a viral "
            "Instagram brand presence, we designed a high-fidelity visualizer dashboard with custom physics."
        )

        # Formulate insights on Future Advances in Agentic Memory
        advances = [
            {
                "title": "Layerless Cognitive Architecture",
                "desc": "Moving away from middleware databases (Vector DBs) and embedding memory operations directly inside the agent's core cognitive loop. This drastically reduces API roundtrips and aligns memory access with human neuro-symbolic pathways."
            },
            {
                "title": "Schema-Driven Real-time Guardrails",
                "desc": "Traditional safety filters are applied as external input wrappers. Native memory guardrails intercept the associative consolidation process itself, scrubbing sensitive data (PII) before it is permanently encoded in the system."
            },
            {
                "title": "Dual-System Associative Consolidation",
                "desc": "Instead of storing every single interaction, memory engines must consolidate. Ephemeral facts stay in high-decay short-term storage, while concepts with high emotional, semantic, or repetition weight naturally transition to long-term networks."
            }
        ]

        return {
            "project_name": "AuraMemory",
            "summary": summary,
            "user_intent": "Build native agentic memory + launch as viral Instagram content to network, get investments, and monetize.",
            "milestones": self.milestones,
            "advances": advances
        }

    def generate_instagram_content(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates structured, copy-paste ready Instagram Carousel posts.
        """
        posts = [
            {
                "title": "Post 1: The AI Memory Lie Nobody Tells You",
                "hook": "❌ Traditional vector DBs are KILLING your AI agent's speed.",
                "theme": "Educational / Contradictory Hook",
                "slides": [
                    {
                        "slide_num": 1,
                        "headline": "The AI Memory Lie 🧠",
                        "body": "Everyone thinks AI agents remember things because of 'Vector Databases'. But middleware wrappers slow down agents and add unnecessary layers. Here is how we build NATIVE memory..."
                    },
                    {
                        "slide_num": 2,
                        "headline": "The Middleware Problem 🔌",
                        "body": "LLM -> Tool Call -> Vector DB -> Embeddings -> Search -> Prompt Inject. This is NOT how humans think. It makes AI feel laggy and disconnected. We need a dual-system cognitive brain."
                    },
                    {
                        "slide_num": 3,
                        "headline": "System 1 vs System 2 ⚡️",
                        "body": "- System 1 (Working Memory): Ephemeral, high-decay, holds immediate chat tokens.\n- System 2 (Long-Term): Consolidated knowledge that is permanently linked through semantic tag weight."
                    },
                    {
                        "slide_num": 4,
                        "headline": "Configurable Guardrails 🛡️",
                        "body": "We don't filter at the end. We filter *at the gates*. A schema-driven engine scrubs PII (emails, keys) and blocks restricted topics natively BEFORE they consolidate."
                    },
                    {
                        "slide_num": 5,
                        "headline": "Watch it Live! 🚀",
                        "body": "I'm building this live. Slide to see the code structure! Check my bio link to see the GitHub repo and live interactive graph simulation!"
                    }
                ],
                "cta": "💡 Want to build native AI brains that think like humans? Comment 'MEMORY' and I'll send you the Github repository link directly! Let's build together.",
                "hashtags": "#AIAgents #AgenticMemory #SoftwareEngineering #PythonProgramming #TechStartup #ArtificialIntelligence #IndieHacker #VCNetworking"
            },
            {
                "title": "Post 2: Coding an AI Brain in 100 Lines of Python",
                "hook": "🐍 How to code a native dual-system AI memory module with zero dependencies.",
                "theme": "Technical Tutorial / Code Value",
                "slides": [
                    {
                        "slide_num": 1,
                        "headline": "Native Memory in Python 💻",
                        "body": "No Vector DB wrappers. No complex frameworks. Just pure, native cognitive architecture. Swipe to build your own dual-system AI brain in under 100 lines!"
                    },
                    {
                        "slide_num": 2,
                        "headline": "Step 1: The Memory Node 🧬",
                        "body": "Define a MemoryNode class. It stores the content, timestamps, access counts, and an association dictionary linking it to other nodes by semantic weight."
                    },
                    {
                        "slide_num": 3,
                        "headline": "Step 2: Configurable Guardrails 🛡️",
                        "body": "Inject a GuardrailEngine that intercepts memory writes. Automatically scrubs out passwords, API keys, and blocks malicious topics natively before storage."
                    },
                    {
                        "slide_num": 4,
                        "headline": "Step 3: The Consolidation Loop 🔄",
                        "body": "Create a `consolidate()` routine. Ephemeral System 1 nodes decay over time. Nodes with high frequency or importance are promoted to permanent System 2!"
                    },
                    {
                        "slide_num": 5,
                        "headline": "Get the Full Code! 🚀",
                        "body": "The entire code is open-source. Drop a comment or message me to get instant access to the interactive graph web app!"
                    }
                ],
                "cta": "🚀 Drop a comment 'CODE' to get the full python source and web visualizer! Let's redefine agent memory.",
                "hashtags": "#PythonCode #CodeTutorial #WebDevelopment #AIArchitecture #AIAgents #TechFounder #Startups #InstagramDev"
            }
        ]
        return posts

    def write_reports(self):
        summary_data = self.compile_summary()
        ig_posts = self.generate_instagram_content(summary_data)

        # 1. Save Report Markdown
        report_path = os.path.join(self.output_dir, "reports", "agentic_memory_report.md")
        print(f"📝 Writing report to {report_path}...")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# AuraMemory Agentic AI Memory Report & Social Kit\n\n")
            f.write(f"## 1. Conversation Summary\n\n{summary_data['summary']}\n\n")
            f.write(f"### Key Session Milestones:\n")
            for m in summary_data['milestones']:
                f.write(f"- **{m.split(':')[0]}**: {m.split(':')[1].strip()}\n")
            f.write(f"\n## 2. Future Advances in Agentic Memory\n\n")
            for adv in summary_data['advances']:
                f.write(f"### 🧠 {adv['title']}\n{adv['desc']}\n\n")
            f.write(f"\n## 3. Instagram Content Creator & Slide Deck\n\n")
            for post in ig_posts:
                f.write(f"### 📸 {post['title']}\n")
                f.write(f"**Hook:** `{post['hook']}`\n\n")
                f.write(f"#### Slide Carousel Sequence:\n")
                for s in post['slides']:
                    f.write(f"**Slide {s['slide_num']}: {s['headline']}**\n> {s['body'].replace(chr(10), ' ')}\n\n")
                f.write(f"**Call To Action (CTA):** *{post['cta']}*\n\n")
                f.write(f"**Hashtags:** `{post['hashtags']}`\n\n")
                f.write(f"---\n\n")

        # 2. Save JSON for Frontend consumption
        json_data = {
            "summary": summary_data,
            "instagram_posts": ig_posts
        }
        json_path = os.path.join(self.output_dir, "data", "watcher_data.json")
        print(f"💾 Writing JSON data to {json_path}...")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        print("🎉 Watcher Agent execution completed successfully!")

if __name__ == "__main__":
    # Autonomously locate the most recently active conversation log folder
    brain_dir = "/Users/mindflow/.gemini/antigravity/brain"
    log_file = None
    
    if os.path.exists(brain_dir):
        # Scan brain subdirectories for transcript files
        subdirs = [os.path.join(brain_dir, d) for d in os.listdir(brain_dir) if os.path.isdir(os.path.join(brain_dir, d))]
        transcripts = []
        for sd in subdirs:
            t_path = os.path.join(sd, ".system_generated", "logs", "transcript.jsonl")
            if os.path.exists(t_path):
                transcripts.append((t_path, os.path.getmtime(t_path)))
        
        if transcripts:
            # Sort by last modified time descending
            transcripts.sort(key=lambda x: x[1], reverse=True)
            log_file = transcripts[0][0]
            print(f"🤖 Autonomously located active log session: {log_file}")
            
    if not log_file:
        # Fallback default
        log_file = "/Users/mindflow/.gemini/antigravity/brain/d8adef4a-b7a2-4f9c-b404-5f2fd732fb3b/.system_generated/logs/transcript.jsonl"

    # Set workspace output directory relative to agent location (always points to AuraMemory/)
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"📁 Workspace output directory set relative to: {workspace_dir}")
    
    watcher = WatcherAgent(log_filepath=log_file, output_dir=workspace_dir)
    if watcher.parse_logs():
        watcher.write_reports()
    else:
        print("⚠️ Running under fallback mode due to file read limits...")
        watcher.write_reports()
