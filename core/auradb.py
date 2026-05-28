#!/usr/bin/env python3
"""
AuraMemory Database Layer: core/auradb.py
Contains Path C WAL-Optimized partitioned SQLite sharding managers and
AuraWiki Obsidian Markdown double-linked symbolic compilers.
"""

import os
import json
import sqlite3
import threading
import math
from typing import Dict, List, Any, Optional, Tuple

class ThreadSafeWALPartitionManager:
    def __init__(self, base_directory: str = "data/vaults"):
        self.base_dir = os.path.abspath(base_directory)
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Reentrant locks per partition path to prevent multi-thread write collisions
        self._locks: Dict[str, threading.RLock] = {}
        self._global_lock = threading.Lock()
        
    def _get_partition_lock(self, db_path: str) -> threading.RLock:
        """Resolve a dedicated reentrant lock for a specific partition path."""
        with self._global_lock:
            if db_path not in self._locks:
                self._locks[db_path] = threading.RLock()
            return self._locks[db_path]

    def get_partition_path(self, agent_id: str, domain: str = "tech") -> str:
        """Dynamically routes memory to a partitioned SQLite database file."""
        sanitized_agent = "".join(c for c in agent_id if c.isalnum() or c in ("-", "_")).lower()
        sanitized_domain = "".join(c for c in domain if c.isalnum() or c in ("-", "_")).lower()
        filename = f"auramem_{sanitized_domain}_{sanitized_agent}.db"
        return os.path.join(self.base_dir, filename)

    def get_connection(self, db_path: str) -> sqlite3.Connection:
        """
        Creates and configures a WAL-optimized SQLite connection with optimal PRAGMAs.
        """
        conn = sqlite3.connect(db_path, timeout=5.0)
        
        # Concurrency and Performance Tuning
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA busy_timeout = 5000;")
        cursor.execute("PRAGMA temp_store = MEMORY;")
        cursor.execute("PRAGMA cache_size = -4000;")  # 4MB Cache Buffer
        conn.commit()
        
        return conn

    def initialize_partition(self, db_path: str):
        """Initializes the database schema with critical indexes for O(log N) retrievals."""
        lock = self._get_partition_lock(db_path)
        with lock:
            conn = self.get_connection(db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memories (
                        id TEXT PRIMARY KEY,
                        agent_id TEXT,
                        content TEXT,
                        system TEXT,
                        tags TEXT,
                        importance REAL,
                        timestamp REAL,
                        access_count INTEGER,
                        strength REAL,
                        associations TEXT,
                        vector TEXT
                    )
                """)
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_system ON memories(system);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_strength ON memories(strength);")
                conn.commit()
            finally:
                conn.close()

    def write_memory(self, agent_id: str, domain: str, memory_dict: Dict[str, Any]) -> bool:
        """Writes a memory node atomically under thread locks."""
        db_path = self.get_partition_path(agent_id, domain)
        self.initialize_partition(db_path)
        
        lock = self._get_partition_lock(db_path)
        with lock:
            conn = self.get_connection(db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO memories (
                        id, agent_id, content, system, tags, importance, 
                        timestamp, access_count, strength, associations, vector
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    memory_dict["id"],
                    memory_dict.get("agent_id", agent_id),
                    memory_dict["content"],
                    memory_dict["system"],
                    json.dumps(memory_dict["tags"]),
                    memory_dict["importance"],
                    memory_dict["timestamp"],
                    memory_dict["access_count"],
                    memory_dict["strength"],
                    json.dumps(memory_dict["associations"]),
                    json.dumps(memory_dict["vector"])
                ))
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] Failed partition write: {e}")
                return False
            finally:
                conn.close()

    def batch_write_memories(self, agent_id: str, domain: str, memories: List[Dict[str, Any]]) -> int:
        """Executes a transaction-safe batch write to a specific partition database."""
        if not memories:
            return 0
            
        db_path = self.get_partition_path(agent_id, domain)
        self.initialize_partition(db_path)
        
        lock = self._get_partition_lock(db_path)
        written = 0
        with lock:
            conn = self.get_connection(db_path)
            try:
                cursor = conn.cursor()
                cursor.execute("BEGIN TRANSACTION;")
                for mem in memories:
                    cursor.execute("""
                        INSERT OR REPLACE INTO memories (
                            id, agent_id, content, system, tags, importance, 
                            timestamp, access_count, strength, associations, vector
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        mem["id"],
                        mem.get("agent_id", agent_id),
                        mem["content"],
                        mem["system"],
                        json.dumps(mem["tags"]),
                        mem["importance"],
                        mem["timestamp"],
                        mem["access_count"],
                        mem["strength"],
                        json.dumps(mem["associations"]),
                        json.dumps(mem["vector"])
                    ))
                    written += 1
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] Transaction rolled back: {e}")
                written = 0
            finally:
                conn.close()
        return written

    def read_memories(self, agent_id: str, domain: str, system: Optional[str] = None) -> List[Dict[str, Any]]:
        """Reads memory entries from a specific partition using binary indexes."""
        db_path = self.get_partition_path(agent_id, domain)
        if not os.path.exists(db_path):
            return []
            
        lock = self._get_partition_lock(db_path)
        with lock:
            conn = self.get_connection(db_path)
            try:
                cursor = conn.cursor()
                if system:
                    cursor.execute("""
                        SELECT id, agent_id, content, system, tags, importance, 
                               timestamp, access_count, strength, associations, vector 
                        FROM memories WHERE agent_id = ? AND system = ?
                    """, (agent_id, system))
                else:
                    cursor.execute("""
                        SELECT id, agent_id, content, system, tags, importance, 
                               timestamp, access_count, strength, associations, vector 
                        FROM memories WHERE agent_id = ?
                    """, (agent_id,))
                
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    results.append({
                        "id": r[0],
                        "agent_id": r[1],
                        "content": r[2],
                        "system": r[3],
                        "tags": json.loads(r[4]),
                        "importance": r[5],
                        "timestamp": r[6],
                        "access_count": r[7],
                        "strength": r[8],
                        "associations": json.loads(r[9]),
                        "vector": json.loads(r[10])
                    })
                return results
            finally:
                conn.close()


class AuraWikiObsidianCompiler:
    def __init__(self, vault_directory: str = "data/aurawiki_vault"):
        self.vault_dir = os.path.abspath(vault_directory)
        os.makedirs(self.vault_dir, exist_ok=True)

    def _sanitize_filename(self, text: str) -> str:
        """Converts raw prompt strings or tags into short, readable note names."""
        import re
        clean = re.sub(r'[^\w\s\-]', '', text)
        words = clean.strip().split()
        if not words:
            return "unnamed_concept"
        return "_".join(words[:4]).title()

    def _cosine_similarity(self, vecA: List[float], vecB: List[float]) -> float:
        """Returns the cosine similarity unit vector product."""
        dot = sum(a * b for a, b in zip(vecA, vecB))
        magA = math.sqrt(sum(a * a for a in vecA))
        magB = math.sqrt(sum(b * b for b in vecB))
        if magA == 0.0 or magB == 0.0:
            return 0.0
        return dot / (magA * magB)

    def compile_nodes_to_vault(self, memories: List[Dict[str, Any]]) -> int:
        """
        Compiles continuous 8D vector memory arrays into structured Obsidian double-bracketed pages.
        """
        node_mappings: Dict[str, Dict[str, Any]] = {}
        for m in memories:
            title = self._sanitize_filename(m.get("tags", ["concept"])[0] if m.get("tags") else m["content"])
            suffix = 1
            original_title = title
            while any(x.get("title") == title for x in node_mappings.values()):
                title = f"{original_title}_{suffix}"
                suffix += 1
                
            node_mappings[m["id"]] = {
                "id": m["id"],
                "content": m["content"],
                "tags": m.get("tags", []),
                "system": m.get("system", "working"),
                "importance": m.get("importance", 0.5),
                "strength": m.get("strength", 1.0),
                "timestamp": m.get("timestamp", 0.0),
                "vector": m.get("vector", [0.0]*8),
                "title": title,
                "file_path": os.path.join(self.vault_dir, f"{title}.md")
            }

        compiled_count = 0
        for node_id, data in node_mappings.items():
            title = data["title"]
            content = data["content"]
            vector = data["vector"]
            
            markdown_content = []
            markdown_content.append("---")
            markdown_content.append(f"id: \"{data['id']}\"")
            markdown_content.append(f"system: \"{data['system']}\"")
            markdown_content.append(f"importance: {data['importance']}")
            markdown_content.append(f"strength: {data['strength']}")
            markdown_content.append(f"timestamp: {data['timestamp']}")
            markdown_content.append(f"tags: [{', '.join(data['tags'])}]")
            markdown_content.append("---")
            markdown_content.append("")
            
            markdown_content.append(f"# {title.replace('_', ' ')}")
            markdown_content.append("")
            markdown_content.append(f"> **Consolidated Insight**: {content}")
            markdown_content.append("")
            
            # Map cosine associations >= 0.20
            semantic_links = []
            for other_id, other_data in node_mappings.items():
                if other_id == node_id:
                    continue
                similarity = self._cosine_similarity(vector, other_data["vector"])
                if similarity >= 0.20:
                    semantic_links.append((similarity, other_data["title"]))

            semantic_links.sort(key=lambda x: x[0], reverse=True)
            
            markdown_content.append("## 🧬 Semantically Associated Knowledge Connections")
            if semantic_links:
                markdown_content.append("The continuous semantic cognitive engine has traced associations to these concepts:")
                markdown_content.append("")
                for sim, linked_title in semantic_links:
                    display_name = linked_title.replace('_', ' ')
                    markdown_content.append(f"- [[{linked_title}|{display_name}]] (Vector Match Strength: `{sim:.4f}`)")
            else:
                markdown_content.append("No active connections trace to this node currently.")
                
            markdown_content.append("")
            markdown_content.append("---")
            markdown_content.append("*Generated process-locally by AuraWiki double-linked compiler.*")

            with open(data["file_path"], "w", encoding="utf-8") as f:
                f.write("\n".join(markdown_content))
            compiled_count += 1
            
        return compiled_count
