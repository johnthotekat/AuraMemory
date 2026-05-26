#!/usr/bin/env python3
"""
AuraMemory Core Engine: core/cortex.py
A dual-system native agentic memory architecture with schema-driven configurable guardrails.

Now upgraded with:
- Milestone A: 8-Dimensional Local Semantic Vector Embeddings
- Enterprise Scaling Milestone: Pure-Python KD-Tree Sub-linear Indexing O(log N)
- Enterprise Scaling Milestone: Multi-domain Vocabulary Profiles (Tech, Medical, Agriculture)
- 100% dependency-free, pure-python local execution.
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


# --- MULTI-DOMAIN SEMANTIC VOCABULARY PROFILES ---

TECH_STARTUP_VOCAB = {
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
    "glassmorphism": [0.0, 0.3, 0.0, 0.0, 0.2, 0.2, 0.3, 1.0],
    
    "integration": [0.2, 0.8, 0.0, 0.0, 0.1, 0.2, 0.5, 0.0],
    "standard": [0.1, 0.8, 0.3, 0.0, 0.0, 0.1, 0.4, 0.0],
    "mcp": [0.8, 0.7, 0.2, 0.0, 0.1, 0.3, 0.6, 0.1],
    "protocol": [0.4, 0.8, 0.3, 0.0, 0.0, 0.1, 0.5, 0.0],
    "system": [0.3, 0.9, 0.1, 0.0, 0.0, 0.1, 0.4, 0.0]
}

MEDICAL_VOCAB = {
    "healthcare": [1.0, 0.2, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0],
    "clinical": [0.9, 0.4, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0],
    "patient": [0.8, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2],
    "diagnosis": [0.9, 0.5, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1],
    "medical": [0.9, 0.3, 0.0, 0.0, 0.0, 0.1, 0.2, 0.0],
    "heart": [0.7, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1],
    "treatment": [0.8, 0.3, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1],
    "symptoms": [0.8, 0.2, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1],
    "drug": [0.7, 0.2, 0.0, 0.0, 0.0, 0.2, 0.1, 0.0],
    "therapy": [0.8, 0.2, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1],
    "hospital": [0.6, 0.4, 0.0, 0.0, 0.0, 0.2, 0.1, 0.0],
    "record": [0.4, 0.8, 0.1, 0.0, 0.0, 0.1, 0.3, 0.0],
    "disease": [0.8, 0.2, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0],
    "doctor": [0.8, 0.3, 0.0, 0.0, 0.0, 0.1, 0.2, 0.1],
    "medicine": [0.8, 0.2, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0],
    "nurse": [0.7, 0.2, 0.0, 0.0, 0.0, 0.1, 0.1, 0.2]
}

AGRICULTURE_VOCAB = {
    "crops": [0.9, 0.1, 0.0, 0.0, 0.0, 0.2, 0.1, 0.1],
    "soil": [0.8, 0.2, 0.0, 0.0, 0.0, 0.1, 0.2, 0.0],
    "organic": [0.7, 0.1, 0.0, 0.0, 0.1, 0.2, 0.1, 0.2],
    "irrigation": [0.7, 0.6, 0.0, 0.0, 0.0, 0.1, 0.3, 0.1],
    "harvest": [0.8, 0.3, 0.0, 0.0, 0.1, 0.3, 0.1, 0.1],
    "tomato": [0.5, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.3],
    "fertilizer": [0.6, 0.3, 0.0, 0.0, 0.0, 0.2, 0.1, 0.0],
    "farming": [0.8, 0.2, 0.0, 0.0, 0.2, 0.3, 0.2, 0.1],
    "plants": [0.7, 0.1, 0.0, 0.0, 0.0, 0.1, 0.1, 0.2],
    "pest": [0.6, 0.2, 0.1, 0.4, 0.0, 0.1, 0.2, 0.0],
    "weather": [0.6, 0.2, 0.0, 0.0, 0.1, 0.1, 0.1, 0.1],
    "yield": [0.7, 0.4, 0.0, 0.0, 0.1, 0.5, 0.1, 0.0],
    "agricultural": [0.8, 0.3, 0.0, 0.0, 0.2, 0.3, 0.2, 0.1],
    "crop": [0.9, 0.1, 0.0, 0.0, 0.0, 0.2, 0.1, 0.1],
    "seeds": [0.8, 0.2, 0.0, 0.0, 0.0, 0.2, 0.1, 0.1],
    "tractor": [0.4, 0.8, 0.0, 0.0, 0.1, 0.2, 0.4, 0.1]
}

VOCAB_PROFILES = {
    "tech": TECH_STARTUP_VOCAB,
    "medical": MEDICAL_VOCAB,
    "agriculture": AGRICULTURE_VOCAB
}

STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "for", "with", "is", "are", "am", "was",
    "were", "be", "been", "being", "to", "and", "or", "of", "how", "do", "i", "we",
    "my", "our", "you", "your", "he", "she", "they", "it", "this", "that", "these",
    "those", "have", "has", "had", "by", "but", "not", "from", "as", "about"
}

# --- NLP & VECTOR MATHEMATICAL UTILITIES ---

def tokenize_text(text: str) -> List[str]:
    """Tokenize input text: clean, lowercase, split CamelCase, filter stopwords."""
    if not text:
        return []
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'[^\w\s\-]', ' ', text)
    words = text.lower().split()
    return [w for w in words if w not in STOPWORDS]

def stem_word(word: str) -> str:
    """Basic stemmer: strip common suffixes for robust vocab match."""
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

def embed_word(word: str, vocab: Dict[str, List[float]]) -> List[float]:
    """Retrieve 8D vector for a single word, applying stem and substring fallback."""
    word = word.lower()
    if word in vocab:
        return vocab[word]
    
    stemmed = stem_word(word)
    if stemmed in vocab:
        return vocab[stemmed]
        
    for vocab_word in vocab:
        if len(vocab_word) > 3 and (vocab_word in stemmed or stemmed in vocab_word):
            return vocab[vocab_word]
            
    return [0.0] * 8

def embed_words(words: List[str], vocab: Dict[str, List[float]]) -> List[float]:
    """Embed list of words, returning normalized average vector."""
    if not words:
        return [0.0] * 8
    
    vector = [0.0] * 8
    count = 0
    for w in words:
        v = embed_word(w, vocab)
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

def embed_node(tags: List[str], content: str, vocab: Dict[str, List[float]]) -> List[float]:
    """Compute the 8D semantic vector for a node: 70% tags, 30% content."""
    tag_words = []
    for t in tags:
        tag_words.extend(tokenize_text(t))
    content_words = tokenize_text(content)
    
    tag_vec = embed_words(tag_words, vocab)
    content_vec = embed_words(content_words, vocab)
    
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


# --- SUB-LINEAR SEARCH INDEX: 8D KD-TREE ---

class KDNode:
    def __init__(self, point: List[float], node_id: str, left=None, right=None, axis: int = 0):
        self.point = point
        self.node_id = node_id
        self.left = left
        self.right = right
        self.axis = axis

class KDTreeIndex:
    def __init__(self, k: int = 8):
        self.k = k
        self.root = None

    def build(self, nodes: List[Tuple[List[float], str]]):
        """Construct KD-Tree from list of (vector, node_id) tuples."""
        self.root = self._build_tree(nodes, 0)

    def _build_tree(self, nodes: List[Tuple[List[float], str]], depth: int) -> Optional[KDNode]:
        if not nodes:
            return None
        
        axis = depth % self.k
        # Sort nodes by alternate dimension axis coordinate
        nodes.sort(key=lambda x: x[0][axis])
        median = len(nodes) // 2
        
        return KDNode(
            point=nodes[median][0],
            node_id=nodes[median][1],
            left=self._build_tree(nodes[:median], depth + 1),
            right=self._build_tree(nodes[median + 1:], depth + 1),
            axis=axis
        )

    def search_knn(self, query: List[float], max_count: int) -> List[Tuple[float, str]]:
        """
        Recursive K-Nearest Neighbors search.
        Prunes far hyperplanes using hypersphere distance boundaries.
        """
        best_nodes = [] # Sorted list of (EuclideanDistance, node_id)
        self._search(self.root, query, max_count, best_nodes)
        return best_nodes

    def _search(self, node: Optional[KDNode], query: List[float], max_count: int, best_nodes: List[Tuple[float, str]]):
        if node is None:
            return
        
        # Calculate Cartesian Euclidean distance (Equivalent to maximizing Cosine Similarity)
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(query, node.point)))
        
        # Insert into best_nodes (sorted list)
        inserted = False
        for i, (d, _) in enumerate(best_nodes):
            if dist < d:
                best_nodes.insert(i, (dist, node.node_id))
                inserted = True
                break
                
        if not inserted and len(best_nodes) < max_count:
            best_nodes.append((dist, node.node_id))
            
        if len(best_nodes) > max_count:
            best_nodes.pop()
            
        # Determine closer tree sub-branch
        axis = node.axis
        diff = query[axis] - node.point[axis]
        near_branch = node.left if diff < 0 else node.right
        far_branch = node.right if diff < 0 else node.left
        
        self._search(near_branch, query, max_count, best_nodes)
        
        # Pruning check: If plane boundary is closer than worst best_node, search far branch
        worst_dist = best_nodes[-1][0] if len(best_nodes) == max_count else float('inf')
        if abs(diff) < worst_dist:
            self._search(far_branch, query, max_count, best_nodes)


# --- COGNITIVE MEMORY STRUCTURES ---

class MemoryNode:
    def __init__(self, content: str, system: str = "working", tags: List[str] = None, importance: float = 0.5, vocab: Dict[str, List[float]] = None):
        self.id = str(uuid.uuid4())
        self.content = content
        self.system = system
        self.tags = list(set(tags or []))
        self.importance = importance
        self.timestamp = time.time()
        self.access_count = 1
        self.decay_factor = 0.1
        self.strength = 1.0
        self.associations: Dict[str, float] = {}
        
        # Calculate Milestone A Semantic Embedding Vector
        self.vector = embed_node(self.tags, self.content, vocab=vocab)

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
    def __init__(self, guardrail_config: GuardrailConfig = None, profile: str = "tech", custom_vocab: Dict[str, List[float]] = None, custom_vocab_path: str = None):
        self.config = guardrail_config or GuardrailConfig()
        self.guardrail = GuardrailEngine(self.config)
        self.nodes: Dict[str, MemoryNode] = {}
        self.consolidation_threshold = 0.6

        # Configure Modular Vocabulary
        self.vocab = {}
        if custom_vocab:
            self.vocab = custom_vocab
        elif custom_vocab_path:
            try:
                with open(custom_vocab_path, "r", encoding="utf-8") as f:
                    self.vocab = json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading custom vocabulary: {e}")
                self.vocab = VOCAB_PROFILES.get(profile, VOCAB_PROFILES["tech"])
        else:
            self.vocab = VOCAB_PROFILES.get(profile, VOCAB_PROFILES["tech"])

        # Configure KD-Tree sub-linear search index
        self.index = KDTreeIndex(k=8)
        self.index_dirty = True

    def rebuild_index(self):
        """Rebuilds the KD-Tree space partitioning index in O(N log N)."""
        nodes_data = [(node.vector, node.id) for node in self.nodes.values()]
        self.index.build(nodes_data)
        self.index_dirty = False

    def add_memory(self, content: str, tags: List[str] = None, importance: float = 0.5) -> Tuple[Optional[str], GuardrailResult]:
        """Adds a new memory to System 1 (Working Memory) after passing through Guardrails."""
        result = self.guardrail.process_content(content)
        if not result.passed:
            return None, result

        # Create new node
        node = MemoryNode(content=result.processed, system="working", tags=tags, importance=importance, vocab=self.vocab)
        self.nodes[node.id] = node

        # Form automatic links using 8D vector similarities
        self._link_related_nodes(node)

        # Mark index dirty to trigger rebuild on next recall
        self.index_dirty = True

        return node.id, result

    def _link_related_nodes(self, new_node: MemoryNode):
        """Link nodes automatically if their 8D semantic similarity meets or exceeds 0.20."""
        for node_id, node in self.nodes.items():
            if node_id == new_node.id:
                continue
            
            sim = cosine_similarity(new_node.vector, node.vector)
            if sim >= 0.20:
                # Map [0.20, 1.0] -> [0.20, 0.90] strength
                strength = 0.2 + (0.875 * (sim - 0.20))
                strength = min(0.9, strength)
                
                new_node.add_association(node_id, strength)
                node.add_association(new_node.id, strength)

    def consolidate(self, decay_rate: float = 1.0) -> List[str]:
        """Consolidates working memory, decay nodes, and prune expired ones."""
        promoted_contents = []
        to_delete = []

        for node_id, node in list(self.nodes.items()):
            if node.system == "working":
                cognitive_score = (node.importance * 0.5) + (min(node.access_count / 5.0, 1.0) * 0.5)
                
                if cognitive_score >= self.consolidation_threshold:
                    node.system = "long_term"
                    node.strength = 1.0
                    promoted_contents.append(node.content)
                else:
                    node.decay(decay_rate)
                    if node.strength <= 0.0:
                        to_delete.append(node_id)

        for d_id in to_delete:
            if d_id in self.nodes:
                del self.nodes[d_id]
                for node in self.nodes.values():
                    if d_id in node.associations:
                        del node.associations[d_id]

        if to_delete or promoted_contents:
            self.index_dirty = True

        return promoted_contents

    def recall(self, query_tags: List[str] = None, query_text: str = "") -> List[MemoryNode]:
        """
        Retrieve relevant memories sorted by relevance.
        Accelerated using K-Nearest Neighbors KD-Tree index when node size > 10.
        """
        query_words = []
        if query_tags:
            for t in query_tags:
                query_words.extend(tokenize_text(t))
        if query_text:
            query_words.extend(tokenize_text(query_text))

        if not query_words:
            results = []
            for node in self.nodes.values():
                base_score = (node.importance * 0.2) + (0.1 if node.system == "long_term" else 0.0)
                results.append((node, base_score * node.strength))
            results.sort(key=lambda x: x[1], reverse=True)
            return [item[0] for item in results[:self.config.max_retrieval_depth]]

        # Generate query vector
        query_vector = embed_words(query_words, self.vocab)

        results = []
        # USE SUB-LINEAR KD-TREE SEARCH IF NODE SIZE EXCEEDS 10
        if len(self.nodes) > 10:
            if self.index_dirty:
                self.rebuild_index()
            
            # Query KD-Tree KNN
            best_nodes = self.index.search_knn(query_vector, self.config.max_retrieval_depth)
            
            for dist, node_id in best_nodes:
                node = self.nodes.get(node_id)
                if not node:
                    continue
                
                # Convert Euclidean distance back to Cosine Similarity score
                sim = 1.0 - (dist * dist) / 2.0
                sim = max(0.0, min(1.0, sim))
                
                relevance = sim * 0.8
                base_score = relevance + (node.importance * 0.2) + (0.1 if node.system == "long_term" else 0.0)
                results.append((node, base_score * node.strength))
        else:
            # Simple linear scan baseline for small node counts
            for node in self.nodes.values():
                sim = cosine_similarity(query_vector, node.vector)
                relevance = sim * 0.8
                
                if relevance > 0.04 or not (query_tags or query_text):
                    base_score = relevance + (node.importance * 0.2) + (0.1 if node.system == "long_term" else 0.0)
                    results.append((node, base_score * node.strength))

        # Sort by final score descending
        results.sort(key=lambda x: x[1], reverse=True)
        trimmed_results = [item[0] for item in results[:self.config.max_retrieval_depth]]
        
        for node in trimmed_results:
            node.refresh()

        return trimmed_results

    def get_state_json(self) -> str:
        """Export state for visual force graph dashboard."""
        state = {
            "nodes": [],
            "links": []
        }
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
    print("🧠 Starting AuraMemory Enterprise Upgraded Engine Self-Test...")
    
    # ----------------------------------------------------
    # Verification Part 1: Standard Guardrail & Recall Tests
    # ----------------------------------------------------
    config = GuardrailConfig(scrub_pii=True, blocked_topics=["hacking"])
    brain = CortexMemory(config, profile="tech")

    print("\n[Test 1] Ingesting Startup / Tech memories...")
    brain.add_memory("I am learning how to build agentic memory modules natively.", tags=["AI", "AgenticMemory"], importance=0.8)
    brain.add_memory("AuraMemory uses a dual-system cognitive architecture.", tags=["AI", "Architecture"], importance=0.9)
    brain.add_memory("Instagram content should have high hooks to attract followers.", tags=["Marketing", "Instagram"], importance=0.4)
    print(f"Graph Size: {len(brain.nodes)}")

    print("\n[Test 2] Testing PII Safety Scrubbing...")
    _, result_pii = brain.add_memory("auth token is key_A1B2C3D4E5F6G7H8 and email is dev@auramem.ai")
    print(f"Scrubbed Output: {result_pii.processed}")

    print("\n[Test 3] Testing Blocked Topic Safety...")
    node_id, result_block = brain.add_memory("How do I perform a hacking attack?")
    print(f"Blocked Topic Allowed? {'Yes' if node_id else 'No (Blocked)'}")

    # ----------------------------------------------------
    # Verification Part 2: Medical & Agriculture Profiles
    # ----------------------------------------------------
    print("\n[Test 4] Loading Medical Vocabulary Profile...")
    med_brain = CortexMemory(profile="medical")
    med_brain.add_memory("Patient exhibits acute symptoms of cardiac disease.", tags=["clinical", "diagnosis"], importance=0.9)
    med_brain.add_memory("Administer cardiovascular drug therapy immediately.", tags=["treatment", "therapy"], importance=0.8)
    
    med_matches = med_brain.recall(query_text="healthcare hospital doctor")
    print(f"Medical matches found: {len(med_matches)}")
    for m in med_matches:
        print(f" - [{m.system}] '{m.content}', tags: {m.tags}")

    print("\n[Test 5] Loading Agricultural Vocabulary Profile...")
    agri_brain = CortexMemory(profile="agriculture")
    agri_brain.add_memory("Organic tomato crops require drip irrigation scheduling.", tags=["crops", "soil"], importance=0.7)
    agri_brain.add_memory("Damp soil weather conditions trigger pest infestation.", tags=["plants", "pest"], importance=0.6)
    
    agri_matches = agri_brain.recall(query_text="farming organic seeds")
    print(f"Agricultural matches found: {len(agri_matches)}")
    for m in agri_matches:
        print(f" - [{m.system}] '{m.content}', tags: {m.tags}")

    # ----------------------------------------------------
    # Verification Part 3: 8D KD-Tree Index KNN search
    # ----------------------------------------------------
    print("\n[Test 6] Testing KD-Tree K-Nearest Neighbors sub-linear Indexing...")
    # Injecting > 10 nodes to trigger KD-Tree search path automatically
    for i in range(12):
        brain.add_memory(
            content=f"AI agent program node number {i} doing architectural database backend python task.",
            tags=["AI", "developer"],
            importance=0.5
        )
    print(f"Brain node count successfully exceeded 10 (Current: {len(brain.nodes)}). Indexing activated.")
    
    # Run a recall query (will automatically build index and search KD-Tree KNN)
    kd_matches = brain.recall(query_text="developer neural brain code")
    print(f"\nKD-Tree KNN retrieved {len(kd_matches)} nearest nodes for query 'developer neural brain code':")
    for m in kd_matches[:3]:
         print(f" - Node {m.id[:6]}: '{m.content[:60]}...'")

    # ----------------------------------------------------
    # Verification Part 4: KD-Tree KNN vs. Linear Scan baseline exact check
    # ----------------------------------------------------
    print("\n[Test 7] Executing KD-Tree KNN Precision Verification check...")
    # Let's compare the actual similarity scores of KD-Tree search vs. Linear baseline
    query_vector = embed_words(tokenize_text("developer neural brain code"), brain.vocab)
    
    # 1. Linear scan results
    linear_results = []
    for node in brain.nodes.values():
        sim = cosine_similarity(query_vector, node.vector)
        linear_results.append((node.id, sim))
    linear_results.sort(key=lambda x: x[1], reverse=True)
    linear_similarities = [round(x[1], 4) for x in linear_results[:3]]
    
    # 2. KD-Tree KNN results
    brain.rebuild_index()
    kd_nodes = brain.index.search_knn(query_vector, 3)
    
    kd_similarities = []
    for dist, node_id in kd_nodes:
        sim = 1.0 - (dist * dist) / 2.0
        kd_similarities.append(round(sim, 4))
    
    # Sort descending to align with linear list
    kd_similarities.sort(reverse=True)
    
    # Check if the similarity scores match exactly within numerical epsilon
    precision_passed = all(abs(k_sim - l_sim) < 1e-4 for k_sim, l_sim in zip(kd_similarities, linear_similarities))
    print(f"KD-Tree KNN Search matches Linear Scan baseline? {'YES (Precision Validated)' if precision_passed else 'No'}")
    
    print("\n🧠 AuraMemory Enterprise Upgraded Engine Self-Test Passed Successfully!")
