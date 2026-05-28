#!/usr/bin/env python3
"""
AuraMemory Universal Gateway: core/gateway.py
A zero-dependency Model Context Protocol (MCP) and JSON-RPC 2.0 Server.

Now upgraded with:
- Persistent AuraDB integration supporting multi-agent workspaces.
- CLI switches: `--storage` (jsonl/sqlite/partitioned) and `--db-path`.
- Expanded tool schemas exposing optional "agent_id" namespaces.
- Dynamic Token-Compressed Context Optimizer.
- Built-in HTTP SimpleHTTPRequestHandler AuraMemoryWebHandler to serve Commander visuals.
"""

import sys
import json
import os
import math
import threading
from typing import Dict, List, Any, Optional
from http.server import SimpleHTTPRequestHandler, HTTPServer

try:
    from core.cortex import CortexMemory, GuardrailConfig, tokenize_text, AgentRegistry
except ImportError:
    from cortex import CortexMemory, GuardrailConfig, tokenize_text, AgentRegistry

# Standard MCP JSON-RPC Protocol Spec
class MCPServer:
    def __init__(self, storage_mode: str = "jsonl", db_path: str = None):
        # Resolve configurations
        self.storage_mode = storage_mode
        self.db_path = db_path
        
        # Initialize default AuraMemory brain
        config = GuardrailConfig(scrub_pii=True, blocked_topics=["malicious", "hacking"])
        self.brain = CortexMemory(guardrail_config=config, profile="tech", storage_mode=self.storage_mode, db_path=self.db_path)
        
        # Output debug logging to stderr to prevent corrupting stdout JSON-RPC transport
        self.log(f"🤖 AuraMemory Universal MCP Server Initialized (Storage: {self.storage_mode.upper()}).")

    def log(self, message: str):
        """Log debugging messages to stderr (stdout is reserved for pure JSON-RPC)."""
        print(f"[* LOG *] {message}", file=sys.stderr, flush=True)

    def compress_context(self, query: str, agent_id: str = "default", max_tokens: int = 500) -> str:
        """
        The Token-Optimizer.
        Retrieves semantic nodes, strips metadata, and builds a compact prompt injection block.
        """
        # Hot-swap active brain namespace before recall
        self.brain.agent_id = agent_id
        nodes = self.brain.recall(query_text=query)
        if not nodes:
            return "No relevant memories found."
            
        self.log(f"Compressing context for recall query: '{query}' in namespace '{agent_id}'...")
        
        # Approximate character-to-token ratio (4 chars per token)
        char_limit = max_tokens * 4
        
        context_blocks = []
        current_chars = 0
        
        for node in nodes:
            # Format block compactly
            sys_label = "LTM" if node.system == "long_term" else f"WM:{node.strength:.2f}"
            tags_label = ",".join(node.tags)
            block = f"[{sys_label}][{tags_label}] {node.content}"
            
            if current_chars + len(block) + 2 > char_limit:
                break
                
            context_blocks.append(block)
            current_chars += len(block) + 2
            
        compressed = "\n".join(context_blocks)
        self.log(f"Compressed context generated successfully ({len(compressed) // 4} tokens).")
        return compressed

    def handle_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        """Parses and routes incoming standard JSON-RPC requests."""
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        response = {
            "jsonrpc": "2.0",
            "id": req_id
        }

        try:
            if method == "initialize":
                response["result"] = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "auramemory-mcp",
                        "version": "1.1.4"
                    }
                }
                
            elif method == "tools/list":
                response["result"] = {
                    "tools": [
                        {
                            "name": "auramem_commit",
                            "description": "Commit a new memory to the Working Memory layer, running PII safety scrubbing and blocked topic guardrails.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "content": {
                                        "type": "string",
                                        "description": "The text content of the memory or interaction to commit."
                                    },
                                    "tags": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "A list of relevant keyword tags."
                                    },
                                    "importance": {
                                        "type": "number",
                                        "minimum": 0.0,
                                        "maximum": 1.0,
                                        "description": "The cognitive importance score [0.0 - 1.0]."
                                    },
                                    "agent_id": {
                                        "type": "string",
                                        "description": "Optional agent workspace partition namespace (defaults to 'default')."
                                    }
                                },
                                "required": ["content"]
                            }
                        },
                        {
                            "name": "auramem_recall",
                            "description": "Query the 8D KD-Tree semantic index, retrieving continuous vector similarity memory matches.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The semantic search query words or tags."
                                    },
                                    "agent_id": {
                                        "type": "string",
                                        "description": "Optional agent workspace partition namespace (defaults to 'default')."
                                    }
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "auramem_consolidate",
                            "description": "Run the cognitive consolidator, decaying working memory strength and promoting high-frequency concepts to long-term storage.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "decay_rate": {
                                        "type": "number",
                                        "description": "Cognitive decay modifier speed."
                                    },
                                    "agent_id": {
                                        "type": "string",
                                        "description": "Optional agent workspace partition namespace (defaults to 'default')."
                                    }
                                }
                            }
                        },
                        {
                            "name": "auramem_compress_context",
                            "description": "The Token Optimizer. Retrieves semantically relevant memory blocks and builds a highly compressed, token-capped prompt injection block.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The active conversation topic query to match."
                                    },
                                    "max_tokens": {
                                        "type": "integer",
                                        "description": "Strict maximum token limit to compress context within."
                                    },
                                    "agent_id": {
                                        "type": "string",
                                        "description": "Optional agent workspace partition namespace (defaults to 'default')."
                                    }
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "auramem_repo_strategist",
                            "description": "The Cognitive Repository Strategist. Setup perfect GitHub configurations, analyze repository modularity/friction, draft launch copy, or write conventional commits natively.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {
                                        "type": "string",
                                        "enum": ["analyze", "setup", "social", "commit"],
                                        "description": "The repository strategy action to execute: 'analyze' (crawl health/modularity), 'setup' (bootstrap perfect templates & CONTRIBUTING/ROADMAP docs), 'social' (generate launch copy showcase), 'commit' (generate conventional semantic commits)."
                                    }
                                },
                                "required": ["action"]
                            }
                        }
                    ]
                }
                
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                agent_id = args.get("agent_id", "default")
                
                # Dynamic Hot-Swap Active Brain Namespace
                self.brain.agent_id = agent_id
                
                if tool_name == "auramem_commit":
                    content = args.get("content")
                    tags = args.get("tags", [])
                    importance = args.get("importance", 0.6)
                    
                    node_id, g_result = self.brain.add_memory(content, tags, importance)
                    
                    if node_id:
                        result_text = f"✅ Memory successfully committed to namespace '{agent_id}'. Node ID: {node_id}."
                        if g_result.violations:
                            result_text += f"\n⚠️ Scrubbed PII patterns: {', '.join(g_result.violations)}"
                    else:
                        result_text = f"❌ Ingestion rejected by safety guardrails. Violations: {', '.join(g_result.violations)}"
                        
                    response["result"] = {
                        "content": [{"type": "text", "text": result_text}]
                    }
                    
                elif tool_name == "auramem_recall":
                    query = args.get("query")
                    nodes = self.brain.recall(query_text=query)
                    
                    matches = []
                    for n in nodes:
                        sys_label = "LTM" if n.system == "long_term" else f"WM:{n.strength:.2f}"
                        matches.append(f"- [{sys_label}] ID {n.id[:6]} (Tags: {','.join(n.tags)}): '{n.content}'")
                        
                    result_text = "\n".join(matches) if matches else "No semantically relevant memories located."
                    response["result"] = {
                        "content": [{"type": "text", "text": result_text}]
                    }
                    
                elif tool_name == "auramem_consolidate":
                    decay_rate = args.get("decay_rate", 1.0)
                    promoted = self.brain.consolidate(decay_rate=decay_rate)
                    
                    result_text = f"⚙️ Consolidation worker executed for namespace '{agent_id}'. Promoted to System 2: {len(promoted)} nodes."
                    if promoted:
                        result_text += f"\nPromoted items: {', '.join(promoted)}"
                        
                    response["result"] = {
                        "content": [{"type": "text", "text": result_text}]
                    }
                    
                elif tool_name == "auramem_compress_context":
                    query = args.get("query")
                    max_tokens = args.get("max_tokens", 400)
                    compressed = self.compress_context(query, agent_id, max_tokens)
                    
                    response["result"] = {
                        "content": [{"type": "text", "text": compressed}]
                    }
                    
                elif tool_name == "auramem_repo_strategist":
                    action = args.get("action", "analyze")
                    
                    try:
                        from core.strategist import RepoStrategist
                    except ImportError:
                        try:
                            from strategist import RepoStrategist
                        except ImportError:
                            RepoStrategist = None
                            
                    if RepoStrategist is None:
                        result_text = "❌ Strategy module not loaded. Place core/strategist.py inside repository paths."
                    else:
                        strategist = RepoStrategist()
                        if action == "analyze":
                            health = strategist.crawl_modularity_friction()
                            result_text = (
                                f"📋 AuraMemory Modularity & Friction Audit:\n"
                                f" - Modularity Score: {health.get('modularity_score', 0.0)}/10.0\n"
                                f" - Total Friction Hotspots: {len(health.get('friction_hotspots', []))}\n"
                                f" - Suggestions: {', '.join(health.get('suggestions', []))}"
                            )
                        elif action == "setup":
                            success = strategist.bootstrap_release_templates()
                            result_text = "✅ Setup templates initialized successfully!" if success else "❌ Template setup failed."
                        elif action == "social":
                            result_text = strategist.generate_social_showcase()
                        elif action == "commit":
                            result_text = strategist.generate_conventional_commit()
                        else:
                            result_text = f"❌ Action '{action}' not recognized."
                            
                    response["result"] = {
                        "content": [{"type": "text", "text": result_text}]
                    }
                else:
                    response["error"] = {
                        "code": -32601,
                        "message": f"Method not found: tool '{tool_name}' is not registered."
                    }
            else:
                # Fallback standard JSON-RPC methods
                response["error"] = {
                    "code": -32601,
                    "message": f"Method not found: '{method}'"
                }
        except Exception as e:
            self.log(f"💥 Server execution error: {e}")
            response["error"] = {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }

        return response

    def run_stdio_loop(self):
        """Standard input/output main loop complying with Model Context Protocol."""
        self.log("🔌 Stdio transport loop active. Awaiting JSON-RPC requests...")
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                req = json.loads(line.strip())
                res = self.handle_request(req)
                
                # Output pure JSON line to stdout, immediately flushing buffer
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                err_res = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error: Invalid JSON."}
                }
                sys.stdout.write(json.dumps(err_res) + "\n")
                sys.stdout.flush()
            except Exception as e:
                self.log(f"Loop Exception: {e}")
                break

# --- VALIDATION RUNNER / CLI ---

def run_self_validation(storage_mode: str, db_path: str):
    print(f"🤖 Launching AuraMemory Universal Gateway ({storage_mode.upper()}) Self-Validation...\n")
    server = MCPServer(storage_mode=storage_mode, db_path=db_path)

    print("\n[Step 1] Simulating MCP Client Handshake (initialize)...")
    init_frame = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    res_init = server.handle_request(init_frame)
    print(f"Response: {json.dumps(res_init, indent=2)}")
    assert res_init.get("result", {}).get("serverInfo", {}).get("name") == "auramemory-mcp"
    print("✅ Initialize Handshake Validated!")

    print("\n[Step 2] Simulating Tool Discovery (tools/list)...")
    list_frame = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    res_list = server.handle_request(list_frame)
    tools = res_list.get("result", {}).get("tools", [])
    print(f"Discovered {len(tools)} tools: {[t['name'] for t in tools]}")
    assert len(tools) == 5
    print("✅ Tool Discovery Validated!")

    print("\n[Step 3] Simulating Ingestion Call (tools/call: auramem_commit)...")
    commit_frame = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "auramem_commit",
            "arguments": {
                "content": "Claude Desktop Co-work agent uses standard MCP protocol to query memory.",
                "tags": ["AI", "Integration"],
                "importance": 0.8,
                "agent_id": "agent_alpha"
            }
        }
    }
    res_commit = server.handle_request(commit_frame)
    print(f"Response Text: {res_commit['result']['content'][0]['text']}")
    assert "successfully committed" in res_commit['result']['content'][0]['text']
    print("✅ Ingestion Tool Call Validated!")

    print("\n[Step 4] Simulating Recall Call (tools/call: auramem_recall)...")
    recall_frame = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "auramem_recall",
            "arguments": {
                "query": "integration",
                "agent_id": "agent_alpha"
            }
        }
    }
    res_recall = server.handle_request(recall_frame)
    print(f"Response Text:\n{res_recall['result']['content'][0]['text']}")
    assert "Claude Desktop" in res_recall['result']['content'][0]['text']
    print("✅ Recall Tool Call Validated!")

    print("\n[Step 5] Simulating Token-Compressed Context (tools/call: auramem_compress_context)...")
    compress_frame = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "auramem_compress_context",
            "arguments": {
                "query": "standard mcp",
                "max_tokens": 100,
                "agent_id": "agent_alpha"
            }
        }
    }
    res_compress = server.handle_request(compress_frame)
    print(f"Compressed Output Injection Payload:\n{res_compress['result']['content'][0]['text']}")
    assert "Integration" in res_compress['result']['content'][0]['text']
    print("✅ Context Compression Validated!")

    print(f"\n🎉 AuraMemory Universal Gateway ({storage_mode.upper()}) Self-Validation Passed Successfully!")


# --- WEB RUNNER AND STATIC API CONFIG HANDLER ---

class AuraMemoryWebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set target visuals and data directories relative to the repository workspace
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.visuals_dir = os.path.join(base_dir, "visuals")
        self.data_dir = os.path.join(base_dir, "data")
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Intercept API calls
        if path.startswith("/api/"):
            return path
            
        if path == "/" or path == "/visuals" or path == "/visuals/":
            return os.path.join(self.visuals_dir, "index.html")
            
        # Serve data/ and visuals/ explicitly
        if "/data/" in path:
            rel_path = path.split("/data/", 1)[1]
            return os.path.join(self.data_dir, rel_path)
            
        if "/visuals/" in path:
            rel_path = path.split("/visuals/", 1)[1]
            return os.path.join(self.visuals_dir, rel_path)
            
        # Default fallback inside visuals directory
        return os.path.join(self.visuals_dir, path.lstrip("/"))

    def do_GET(self):
        if self.path == "/api/config":
            # Read config dynamically
            try:
                from core.cortex import AgentRegistry
            except ImportError:
                from cortex import AgentRegistry
            config = AgentRegistry.load_config()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(config).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/config":
            # Read the POST payload
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode("utf-8"))
                try:
                    from core.cortex import AgentRegistry
                except ImportError:
                    from cortex import AgentRegistry
                # Save to configuration file
                success = AgentRegistry.save_config(payload)
                if success:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "message": "Configuration successfully synced to data/agents_config.json!"}).encode("utf-8"))
                    return
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
                return
        
        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_web_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AuraMemoryWebHandler)
    
    # Premium Cyber-Neon Launch Banner
    print(f"""
\033[95m======================================================================
    🧠🧬 AURAMEMORY: NATIVE AGENT ORCHESTRATION SERVER 🧬🧠
======================================================================\033[0m
\033[92m● Serving visual graph dashboard: \033[1mhttp://localhost:{port}/visuals/\033[0m
\033[96m● Active REST API dynamic endpoints:
   - GET  /api/config (Read data/agents_config.json)
   - POST /api/config (Write data/agents_config.json)\033[0m
\033[93m● Zero external framework dependencies. Running process-locally < 0.1ms.\033[0m
======================================================================
Press Ctrl+C to shutdown...
""")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AuraMemory Web Server safely.")
        sys.exit(0)


if __name__ == "__main__":
    # Resolve dynamic options
    storage_mode = "jsonl"
    db_path = None
    
    if "--storage" in sys.argv:
        idx = sys.argv.index("--storage")
        if idx + 1 < len(sys.argv):
            storage_mode = sys.argv[idx + 1].lower()
            
    if "--db-path" in sys.argv:
        idx = sys.argv.index("--db-path")
        if idx + 1 < len(sys.argv):
            db_path = sys.argv[idx + 1]
            
    if not db_path:
        db_path = "data/gateway_locker.auradb" if storage_mode == "jsonl" else "data/gateway_locker.db"

    if "--validate" in sys.argv:
        # Clean test runs
        if os.path.exists(db_path):
            try: os.remove(db_path)
            except Exception: pass
            
        run_self_validation(storage_mode, db_path)
        
        # Clean up
        if os.path.exists(db_path):
            try: os.remove(db_path)
            except Exception: pass
    elif "--web" in sys.argv:
        port = 8001
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                try: port = int(sys.argv[idx + 1])
                except ValueError: pass
        run_web_server(port)
    else:
        # Standard launch mode: Runs MCP stdio transport loop
        server = MCPServer(storage_mode=storage_mode, db_path=db_path)
        server.run_stdio_loop()
