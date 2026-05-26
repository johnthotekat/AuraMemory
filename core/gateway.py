#!/usr/bin/env python3
"""
AuraMemory Universal Gateway: core/gateway.py
A zero-dependency Model Context Protocol (MCP) and JSON-RPC 2.0 Server.

Allows any agent (Claude Co-work, Hermes, Claw Bot) to use AuraMemory natively
over standard stdin/stdout JSON-RPC communications, reducing context tokens.
"""

import sys
import json
import os
import math
from typing import Dict, List, Any, Optional

try:
    from core.cortex import CortexMemory, GuardrailConfig, tokenize_text
except ImportError:
    from cortex import CortexMemory, GuardrailConfig, tokenize_text

# Standard MCP JSON-RPC Protocol Spec
class MCPServer:
    def __init__(self):
        # Initialize default AuraMemory brain
        config = GuardrailConfig(scrub_pii=True, blocked_topics=["malicious", "hacking"])
        self.brain = CortexMemory(guardrail_config=config, profile="tech")
        
        # Output debug logging to stderr to prevent corrupting stdout JSON-RPC transport
        self.log("🤖 AuraMemory Universal MCP Server Initialized.")

    def log(self, message: str):
        """Log debugging messages to stderr (stdout is reserved for pure JSON-RPC)."""
        print(f"[* LOG *] {message}", file=sys.stderr, flush=True)

    def compress_context(self, query: str, max_tokens: int = 500) -> str:
        """
        The Token-Optimizer.
        Retrieves semantic nodes, strips metadata, and builds a compact prompt injection block.
        """
        nodes = self.brain.recall(query_text=query)
        if not nodes:
            return "No relevant memories found."
            
        self.log(f"Compressing context for recall query: '{query}'...")
        
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
                        "version": "1.1.0"
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
                                    }
                                },
                                "required": ["query"]
                            }
                        }
                    ]
                }
                
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                
                if tool_name == "auramem_commit":
                    content = args.get("content")
                    tags = args.get("tags", [])
                    importance = args.get("importance", 0.6)
                    
                    node_id, g_result = self.brain.add_memory(content, tags, importance)
                    
                    if node_id:
                        result_text = f"✅ Memory successfully committed to System 1 Working Memory. Node ID: {node_id}."
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
                    
                    result_text = f"⚙️ Consolidation worker executed. Promoted to System 2: {len(promoted)} nodes."
                    if promoted:
                        result_text += f"\nPromoted items: {', '.join(promoted)}"
                        
                    response["result"] = {
                        "content": [{"type": "text", "text": result_text}]
                    }
                    
                elif tool_name == "auramem_compress_context":
                    query = args.get("query")
                    max_tokens = args.get("max_tokens", 400)
                    compressed = self.compress_context(query, max_tokens)
                    
                    response["result"] = {
                        "content": [{"type": "text", "text": compressed}]
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

def run_self_validation():
    print("🤖 Launching AuraMemory Universal Gateway Self-Validation...\n")
    server = MCPServer()

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
    assert len(tools) == 4
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
                "importance": 0.8
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
                "query": "integration"
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
                "max_tokens": 100
            }
        }
    }
    res_compress = server.handle_request(compress_frame)
    print(f"Compressed Output Injection Payload:\n{res_compress['result']['content'][0]['text']}")
    assert "Integration" in res_compress['result']['content'][0]['text']
    print("✅ Context Compression Validated!")

    print("\n🎉 AuraMemory Universal Gateway Self-Validation Passed Successfully!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        run_self_validation()
    else:
        # Standard launch mode: Runs MCP stdio transport loop
        server = MCPServer()
        server.run_stdio_loop()
