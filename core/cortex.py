#!/usr/bin/env python3
"""
AuraMemory Core Engine: core/cortex.py
A dual-system native agentic memory architecture with schema-driven configurable guardrails.

Now upgraded with Milestone A: 8-Dimensional Local Semantic Vector Embeddings
- Performs semantic text tokenization, stopword cleaning, and plural/gerund stemming.
- Blends tags (70%) and content (30%) into a continuous 8D concept vector.
- Automates memory links and search recall using cosine similarity.
- Maintains 100% dependency-free, pure-python local execution.
"""

import re
import json
import uuid
import time
import math
from typing import Dict, List, Set, Tuple, Optional

# --- GUARDRAIL DEFINITIONS ---

class GuardrailConfig:
    def __init__(self, scrub_pii: bool = True, blocked_topics: List[str] = None, max_retrieval_depth: int = 10):
        self.scrub_pii = scrub_pii
        self.blocked_topics = [t.lower() for t in (blocked_topics or [])]
        self.max_retrieval_depth = max_retrieval_depth
        
        # Regex patterns for common PII
        self.pii_patterns = {
            "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "API_KEY": r"(?:key|token|auth|password|secret)[a-zA-Z0-9_\-\:\=\+\/]{8,64}",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "PHONE_NUMBER": r"\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b"
        }

class GuardrailResult:
    def __init__(self, original: str, processed: str, passed: bool, violations: List[str]):
        self.original = original
        self.processed = processed
        self.passed = passed
        self.violations = violations

    def to_dict(self):
        return {
            "original": self.original,
            "processed": self.processed,
            "passed": self.passed,
            "violations": self.violations
        }


class GuardrailEngine:
    def __init__(self, config: GuardrailConfig):
        self.config = config

    def process_content(self, content: str) -> GuardrailResult:
        violations = []
        processed = content
        passed = True

        # 1. PII Scrubbing
        if self.config.scrub_pii:
            for pii_type, pattern in self.config.pii_patterns.items():
                matches = re.findall(pattern, processed, re.IGNORECASE)
                if matches:
                    violations.append(f"PII Detected: {pii_type}")
                    processed = re.sub(pattern, f"<{pii_type}_SCRUBBED>", processed, flags=re.IGNORECASE)

        # 2. Blocked Topics (Semantic & Exact Checks)
        content_lower = content.lower()
        for topic in self.config.blocked_topics:
            if topic in content_lower:
                violations.append(f"Blocked Topic Detected: '{topic}'")
                passed = False  # Blocked topics completely fail guardrails

        return GuardrailResult(original=content, processed=processed, passed=passed, violations=violations)


# --- NATIVE SEMANTIC EMBEDDINGS ENGINE ---

SEMANTIC_VOCAB = {
    "ai": [1.0, 0.2, 0.0, 0.0, 0.0, 0.1, 0.3, 0.0],
    "agent": [0.9, 0.3, 0.0, 0.0, 0.0, 0.2, 0.4, 0.0],
    "agentic": [0.9, 0.3, 0.0, 0.0, 0.0, 0.2, 0.4, 0.0],
    "cognitive": [0.8, 0.4, 0.0, 0.0, 0.0, 0.1, 0.2, 0.2],
    "memory": [0.8, 0.5, 0.0, 0.0, 0.0, 0.1, 0.3, 0.1],
    "brain": [0.8, 0.3, 0.0, 0.0, 0.0, 0.1, 0.2, 0.2],
    "learning": [0.7, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0],
    "model": [0.7, 0.4, 0.0, 0.0, 0.0, 0.1, 0.3, 0.0],
    "llm": [0.9, 0.3, 0.0, 0.0, 0.0, 0.1, 0.4, 0.0],
    "neural": [0.8, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0],
    
    "architecture": [0.1, 1.0, 0.0, 0.0, 0.0, 0.1, 0.4, 0.3],
    "core": [0.0, 0.9, 0.1, 0.0, 0.0, 0.0, 0.3, 0.0],
    "engine": [0.1, 0.9, 0.0, 0.0, 0.0, 0.0, 0.3, 0.1],
    "code": [0.0, 0.8, 0.1, 0.0, 0.0, 0.0, 0.8, 0.0],
    "database": [0.0, 0.8, 0.1, 0.0, 0.0, 0.1, 0.4, 0.0],
    "backend": [0.0, 0.8, 0.1, 0.0, 0.0, 0.0, 0.6, 0.0],
    "middleware": [0.0, 0.8, 0.1, 0.0, 0.0, 0.0, 0.5, 0.0],
    "python": [0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0],
    "dual-system": [0.4, 0.8, 0.0, 0.0, 0.0, 0.1, 0.3, 0.1],
    
    "security": [0.0, 0.2, 1.0, 0.1, 0.0, 0.0, 0.3, 0.0],
    "safety": [0.1, 0.2, 0.9, 0.0, 0.0, 0.0, 0.2, 0.0],
    "guardrail": [0.2, 0.4, 0.9, 0.1, 0.0, 0.0, 0.4, 0.1],
    "scrub": [0.0, 0.3, 0.8, 0.0, 0.0, 0.0, 0.4, 0.0],
    "encrypt": [0.0, 0.4, 0.9, 0.0, 0.0, 0.0, 0.5, 0.0],
    "private": [0.0, 0.1, 0.8, 0.0, 0.0, 0.0, 0.2, 0.0],
    "auth": [0.0, 0.4, 0.8, 0.0, 0.0, 0.0, 0.5, 0.0],
    "token": [0.0, 0.4, 0.7, 0.0, 0.0, 0.0, 0.5, 0.0],
    "key": [0.0, 0.3, 0.7, 0.0, 0.0, 0.0, 0.4, 0.0],
    "secret": [0.0, 0.1, 0.8, 0.1, 0.0, 0.0, 0.2, 0.0],
    
    "malware": [0.0, 0.2, 0.1, 1.0, 0.0, 0.0, 0.2, 0.0],
    "hacking": [0.1, 0.3, 0.1, 1.0, 0.0, 0.0, 0.3, 0.0],
    "malicious": [0.0, 0.1, 0.1, 1.0, 0.0, 0.0, 0.1, 0.0],
    "exploit": [0.0, 0.3, 0.2, 0.9, 0.0, 0.0, 0.4, 0.0],
    "virus": [0.0, 0.2, 0.1, 0.9, 0.0, 0.0, 0.2, 0.0],
    "insider-trading": [0.0, 0.0, 0.4, 0.8, 0.0, 0.3, 0.0, 0.0],
    "block": [0.0, 0.2, 0.6, 0.4, 0.0, 0.0, 0.2, 0.0],
    
    "marketing": [0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.1, 0.2],
    "instagram": [0.0, 0.0, 0.0, 0.0, 1.0, 0.4, 0.1, 0.3],
    "viral": [0.0, 0.0, 0.0, 0.0, 0.9, 0.5, 0.0, 0.4],
    "social": [0.0, 0.0, 0.0, 0.0, 0.9, 0.3, 0.0, 0.2],
    "audience": [0.1, 0.0, 0.0, 0.0, 0.8, 0.4, 0.0, 0.1],
    "reach": [0.0, 0.0, 0.0, 0.0, 0.8, 0.4, 0.0, 0.1],
    "reels": [0.0, 0.0, 0.0, 0.0, 0.9, 0.3, 0.0, 0.4],
    "creator": [0.0, 0.1, 0.0, 0.0, 0.8, 0.4, 0.1, 0.5],
    "media": [0.0, 0.1, 0.0, 0.0, 0.8, 0.3, 0.1, 0.2],
    
    "startup": [0.1, 0.2, 0.0, 0.0, 0.4, 1.0, 0.3, 0.1],
    "monetization": [0.0, 0.1, 0.0, 0.0, 0.5, 1.0, 0.1, 0.1],
    "pitch": [0.0, 0.0, 0.0, 0.0, 0.6, 0.9, 0.1, 0.3],
    "investment": [0.0, 0.1, 0.1, 0.0, 0.2, 1.0, 0.1, 0.0],
    "business": [0.0, 0.2, 0.1, 0.0, 0.4, 0.9, 0.1, 0.0],
    "vc": [0.1, 0.1, 0.0, 0.0, 0.3, 1.0, 0.2, 0.0],
    "network": [0.2, 0.2, 0.0, 0.0, 0.4, 0.9, 0.2, 0.1],
    "monetize": [0.0, 0.1, 0.0, 0.0, 0.5, 1.0, 0.1, 0.1],
    
    "engineering": [0.2, 0.7, 0.1, 0.0, 0.1, 0.2, 1.0, 0.1],
    "developer": [0.2, 0.5, 0.1, 0.0, 0.2, 0.3, 1.0, 0.1],
    "open-source": [0.1, 0.5, 0.2, 0.0, 0.2, 0.3, 0.9, 0.1],
    "git": [0.0, 0.6, 0.1, 0.0, 0.0, 0.1, 0.9, 0.0],
    "github": [0.0, 0.6, 0.1, 0.0, 0.1, 0.2, 0.9, 0.1],
    "tech": [0.4, 0.5, 0.1, 0.0, 0.2, 0.4, 0.8, 0.1],
    "program": [0.1, 0.7, 0.1, 0.0, 0.0, 0.1, 0.9, 0.0],
    
    "design": [0.1, 0.3, 0.0, 0.0, 0.3, 0.2, 0.2, 1.0],
    "canvas": [0.0, 0.4, 0.0, 0.0, 0.2, 0.1, 0.3, 0.9],
    "visualizer": [0.2, 0.5, 0.0, 0.0, 0.3, 0.2, 0.4, 0.9],
    "physics": [0.1, 0.6, 0.0, 0.0, 0.0, 0.0, 0.3, 0.8],
    "custom": [0.0, 0.4, 0.1, 0.0, 0.1, 0.1, 0.3, 0.7],
    "premium": [0.0, 0.2, 0.1, 0.0, 0.4, 0.5, 0.1, 0.8],
    "glassmorphism": [0.0, 0.3, 0.0, 0.0, 0.2, 0.2, 0.3, 1.0]
}

STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "for", "with", "is", "are", "am", "was",
    "were", "be", "been", "being", "to", "and", "or", "of", "how", "do", "i", "we",
    "my", "our", "you", "your", "he", "she", "they", "it", "this", "that", "these",
    "those", "have", "has", "had", "by", "but", "not", "from", "as", "about"
}

def tokenize_text(text: str) -> List[str]:
    """Tokenize input text: clean, lowercase, split CamelCase, filter stopwords."""
    if not text:
        return []
    # Split camelCase if present, e.g. "AgenticMemory" -> "Agentic Memory"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Remove punctuation except hyphens
    text = re.sub(r'[^\w\s\-]', ' ', text)
    words = text.lower().split()
    return [w for w in words if w not in STOPWORDS]

def stem_word(word: str) -> str:
    """Basic stemmer: strip common suffixes for matching against vocab keys."""
    word = word.strip().lower()
    if len(word) <= 3:
        return word
    if word.endswith("ing"):
        return word[:-3]
    if word.endswith("ed"):
        return word[:-2]
    if word.endswith("es"):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    if word.endswith("tic"):
        return word[:-3]
    return word

def embed_word(word: str) -> List[float]:
    """Retrieve 8D vector for a single word, applying stem and substring fallback."""
    word = word.lower()
    if word in SEMANTIC_VOCAB:
        return SEMANTIC_VOCAB[word]
    
    stemmed = stem_word(word)
    if stemmed in SEMANTIC_VOCAB:
        return SEMANTIC_VOCAB[stemmed]
        
    # Check substring fallbacks
    for vocab_word in SEMANTIC_VOCAB:
        if len(vocab_word) > 3 and (vocab_word in stemmed or stemmed in vocab_word):
            return SEMANTIC_VOCAB[vocab_word]
            
    return [0.0] * 8

def embed_words(words: List[str]) -> List[float]:
    """Embed list of words, returning normalized average vector."""
    if not words:
        return [0.0] * 8
    
    vector = [0.0] * 8
    count = 0
    for w in words:
        v = embed_word(w)
        if any(x != 0.0 for x in v):
            for i in range(8):
                vector[i] += v[i]
            count += 1
            
    if count == 0:
        return [0.0] * 8
        
    for i in range(8):
        vector[i] /= count
        
    return normalize_vector(vector)

def normalize_vector(vec: List[float]) -> List[float]:
    """Normalize vector to unit length."""
    mag = math.sqrt(sum(x * x for x in vec))
    if mag == 0.0:
        return [0.0] * 8
    return [x / mag for x in vec]

def cosine_similarity(vecA: List[float], vecB: List[float]) -> float:
    """Compute cosine similarity between two 8D lists."""
    dot = sum(a * b for a, b in zip(vecA, vecB))
    magA = math.sqrt(sum(a * a for a in vecA))
    magB = math.sqrt(sum(b * b for b in vecB))
    if magA == 0.0 or magB == 0.0:
        return 0.0
    return dot / (magA * magB)

def embed_node(tags: List[str], content: str) -> List[float]:
    """Compute the 8D semantic vector for a node: 70% tags, 30% content."""
    tag_words = []
    for t in tags:
        tag_words.extend(tokenize_text(t))
    content_words = tokenize_text(content)
    
    tag_vec = embed_words(tag_words)
    content_vec = embed_words(content_words)
    
    has_tags = any(x != 0.0 for x in tag_vec)
    has_content = any(x != 0.0 for x in content_vec)
    
    if not has_tags and not has_content:
        return [0.1] * 8
    elif not has_tags:
        return content_vec
    elif not has_content:
        return tag_vec
        
    blended = []
    for i in range(8):
        blended.append(0.7 * tag_vec[i] + 0.3 * content_vec[i])
        
    return normalize_vector(blended)


# --- COGNITIVE MEMORY STRUCTURES ---

class MemoryNode:
    def __init__(self, content: str, system: str = "working", tags: List[str] = None, importance: float = 0.5):
        self.id = str(uuid.uuid4())
        self.content = content
        self.system = system  # "working" (System 1) or "long_term" (System 2)
        self.tags = list(set(tags or []))
        self.importance = importance  # [0.0, 1.0]
        self.timestamp = time.time()
        self.access_count = 1
        self.decay_factor = 0.1  # Rate of decay for System 1
        self.strength = 1.0  # Current memory strength [0.0, 1.0]
        self.associations: Dict[str, float] = {}  # TargetNodeID -> Association Strength [0.0, 1.0]
        
        # Calculate Milestone A Semantic Embedding Vector
        self.vector = embed_node(self.tags, self.content)

    def decay(self, rate_modifier: float = 1.0):
        if self.system == "working":
            self.strength = max(0.0, self.strength - (self.decay_factor * rate_modifier))

    def refresh(self):
        self.access_count += 1
        self.strength = min(1.0, self.strength + 0.2)
        self.timestamp = time.time()

    def add_association(self, target_id: str, strength: float):
        if target_id != self.id:
            self.associations[target_id] = max(0.0, min(1.0, strength))

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "system": self.system,
            "tags": self.tags,
            "importance": self.importance,
            "timestamp": self.timestamp,
            "access_count": self.access_count,
            "strength": self.strength,
            "associations": self.associations,
            "vector": self.vector
        }


# --- THE BRAIN CORE: CORTEX MEMORY ---

class CortexMemory:
    def __init__(self, guardrail_config: GuardrailConfig = None):
        self.config = guardrail_config or GuardrailConfig()
        self.guardrail = GuardrailEngine(self.config)
        self.nodes: Dict[str, MemoryNode] = {}
        self.consolidation_threshold = 0.6  # Score needed to migrate to System 2

    def add_memory(self, content: str, tags: List[str] = None, importance: float = 0.5) -> Tuple[Optional[str], GuardrailResult]:
        """
        Adds a new memory to System 1 (Working Memory) after passing through Guardrails.
        """
        # Run through Guardrails
        result = self.guardrail.process_content(content)
        
        if not result.passed:
            # Blocked topic triggers failure
            return None, result

        # Create new node in System 1 (Working Memory)
        node = MemoryNode(content=result.processed, system="working", tags=tags, importance=importance)
        self.nodes[node.id] = node

        # Form automatic links using 8D Semantic Vector Embeddings Cosine Similarity
        self._link_related_nodes(node)

        return node.id, result

    def _link_related_nodes(self, new_node: MemoryNode):
        """Link nodes automatically if their 8D semantic similarity meets or exceeds 0.20."""
        for node_id, node in self.nodes.items():
            if node_id == new_node.id:
                continue
            
            # Compute cosine similarity between their blended vectors
            sim = cosine_similarity(new_node.vector, node.vector)
            
            if sim >= 0.20:
                # Map similarity [0.20, 1.0] -> strength [0.20, 0.90]
                strength = 0.2 + (0.875 * (sim - 0.20))
                strength = min(0.9, strength)
                
                # Bi-directional link
                new_node.add_association(node_id, strength)
                node.add_association(new_node.id, strength)

    def consolidate(self, decay_rate: float = 1.0) -> List[str]:
        """
        Consolidates working memory:
        1. Decays System 1 nodes.
        2. Promotes highly important or frequently accessed nodes to System 2 (Long-term).
        3. Prunes expired System 1 nodes (strength == 0).
        Returns a list of promoted node contents.
        """
        promoted_contents = []
        to_delete = []

        for node_id, node in list(self.nodes.items()):
            if node.system == "working":
                # Compute cognitive score: importance + access frequency weight
                cognitive_score = (node.importance * 0.5) + (min(node.access_count / 5.0, 1.0) * 0.5)
                
                if cognitive_score >= self.consolidation_threshold:
                    # Promote to System 2
                    node.system = "long_term"
                    node.strength = 1.0  # Long-term memory is persistent
                    promoted_contents.append(node.content)
                else:
                    # Apply cognitive decay
                    node.decay(decay_rate)
                    if node.strength <= 0.0:
                        to_delete.append(node_id)

        # Delete pruned nodes and cleanup their association references
        for d_id in to_delete:
            if d_id in self.nodes:
                del self.nodes[d_id]
                for node in self.nodes.values():
                    if d_id in node.associations:
                        del node.associations[d_id]

        return promoted_contents

    def recall(self, query_tags: List[str] = None, query_text: str = "") -> List[MemoryNode]:
        """
        Retrieve relevant memories sorted by semantic cosine similarity relevance.
        """
        query_words = []
        if query_tags:
            for t in query_tags:
                query_words.extend(tokenize_text(t))
        if query_text:
            query_words.extend(tokenize_text(query_text))

        results = []
        if not query_words:
            # If query is completely empty, rank based purely on importance + memory type
            for node in self.nodes.values():
                base_score = (node.importance * 0.2) + (0.1 if node.system == "long_term" else 0.0)
                results.append((node, base_score * node.strength))
        else:
            # Generate vector for the query
            query_vector = embed_words(query_words)
            
            for node in self.nodes.values():
                # Compute continuous similarity
                sim = cosine_similarity(query_vector, node.vector)
                
                # Combine similarity (80% weight), node importance (20% weight), and system boost
                relevance = sim * 0.8
                
                # Filter out extremely unrelated nodes (similarity < 0.05)
                if relevance > 0.04 or not (query_tags or query_text):
                    base_score = relevance + (node.importance * 0.2) + (0.1 if node.system == "long_term" else 0.0)
                    results.append((node, base_score * node.strength))

        # Sort by final score descending
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Trim to max retrieval depth
        trimmed_results = [item[0] for item in results[:self.config.max_retrieval_depth]]
        
        # Refresh access counts for recalled items
        for node in trimmed_results:
            node.refresh()

        return trimmed_results

    def get_state_json(self) -> str:
        """
        Export state specifically for the web graph visualizer dashboard.
        """
        state = {
            "nodes": [],
            "links": []
        }
        
        # Collect nodes
        for node in self.nodes.values():
            state["nodes"].append({
                "id": node.id,
                "content": node.content,
                "system": node.system,
                "tags": node.tags,
                "importance": node.importance,
                "strength": node.strength,
                "access_count": node.access_count,
                "vector": node.vector
            })
            
            # Collect links
            for target_id, strength in node.associations.items():
                if node.id < target_id:
                    state["links"].append({
                        "source": node.id,
                        "target": target_id,
                        "strength": strength
                    })
                    
        return json.dumps(state, indent=2)


# --- SELF TEST / CLI RUNNER ---

if __name__ == "__main__":
    print("🧠 Starting AuraMemory Upgraded Engine Self-Test...")
    
    # Initialize Engine with standard guardrails
    config = GuardrailConfig(
        scrub_pii=True,
        blocked_topics=["hacking", "malware", "insider-trading"]
    )
    brain = CortexMemory(config)

    print("\n[Test 1] Writing valid memories...")
    brain.add_memory("I am learning how to build agentic memory modules natively.", tags=["AI", "AgenticMemory"], importance=0.8)
    brain.add_memory("AuraMemory uses a dual-system cognitive architecture.", tags=["AI", "Architecture"], importance=0.9)
    brain.add_memory("Instagram content should have high hooks to attract followers.", tags=["Marketing", "Instagram"], importance=0.4)

    # Inspect Graph State
    print(f"Memory count: {len(brain.nodes)}")

    print("\n[Test 2] Testing PII Scrubbing guardrail...")
    _, result_pii = brain.add_memory("My developer secret is key_A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q and email is dev@auramem.ai", tags=["Security"])
    print(f"PII Guardrail Triggered? {'Yes' if result_pii.violations else 'No'}")
    print(f"PII Result Violations: {result_pii.violations}")
    print(f"Scrubbed Output: {result_pii.processed}")

    print("\n[Test 3] Testing Blocked Topic guardrail...")
    node_id, result_block = brain.add_memory("How do I write a malware program to perform insider-trading?", tags=["Malicious"])
    print(f"Blocked Topic Allowed? {'Yes' if node_id else 'No (Blocked)'}")
    print(f"Violations: {result_block.violations}")

    print("\n[Test 4] Testing Cognitive Consolidation & Decay...")
    print("Initial Working (System 1) memory nodes:")
    for nid, n in brain.nodes.items():
        print(f" - [{n.system}] Node: '{n.content[:40]}...', Strength: {n.strength:.2f}")

    print("\n--- Running Consolidation Round 1 ---")
    promoted = brain.consolidate(decay_rate=1.5)
    print(f"Promoted to System 2: {promoted}")
    
    print("\nState after Consolidation & Decay:")
    for nid, n in brain.nodes.items():
        print(f" - [{n.system}] Node: '{n.content[:40]}...', Strength: {n.strength:.2f}")

    print("\n[Test 5] Exact Memory Recall Query...")
    matches = brain.recall(query_tags=["AI"])
    print(f"Found {len(matches)} matches for tag ['AI']:")
    for m in matches:
        print(f" - [{m.system}] Match: '{m.content}', Strength: {m.strength:.2f}")

    print("\n[Test 6] Semantic Vector Embedding Recall Query (Crucial Test!)...")
    # A query for "machine learning" should successfully match "AI" tags and nodes!
    semantic_matches = brain.recall(query_text="neural learning network")
    print(f"Found {len(semantic_matches)} matches for query 'neural learning network' (no exact tag intersection):")
    for m in semantic_matches:
        print(f" - [{m.system}] Match: '{m.content[:50]}...', Strength: {m.strength:.2f}")
        
    print("\n🧠 AuraMemory Self-Test Completed Successfully!")
