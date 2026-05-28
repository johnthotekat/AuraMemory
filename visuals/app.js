/* AuraMemory Sovereign Console Controller: app.js */

// --- GLOBAL STATE ---
let nodes = [];
let links = [];
let activeWorkspace = 'default';
let storageMode = 'sqlite'; // dynamically adjusted by stepper recommendations
let piiScrubActive = true;
let topicBlockActive = true;
let decayRate = 0.10;
let maxDepth = 8;

// Simulated configuration profiles
let activeProfile = {
    env: 'edge',
    workload: 'single'
};

// Stepper states
let currentStep = 1;
let egoBeliefs = [];

// Instagram creator studio studio data
let activePostIndex = 0;
let activeSlideIndex = 0;
let instagramPosts = [];

// Affective centoid coordinates values
let centroids = {
    curiosity: 0.85,
    caution: 0.20,
    sociability: 0.60,
    sovereignty: 0.75,
    creativity: 0.90
};

// D3 Force Directed Graph Simulation
let svg, simulation, linkGroup, nodeGroup;
const nodeRadius = 25;

// --- NATIVE SEMANTIC 8D EMBEDDINGS SYSTEM ---
const SEMANTIC_VOCAB = {
    "ai": [1.0, 0.2, 0.0, 0.0, 0.0, 0.1, 0.3, 0.0],
    "machine": [0.8, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0],
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
};

const STOPWORDS = new Set([
    "the", "a", "an", "in", "on", "at", "for", "with", "is", "are", "am", "was",
    "were", "be", "been", "being", "to", "and", "or", "of", "how", "do", "i", "we",
    "my", "our", "you", "your", "he", "she", "they", "it", "this", "that", "these",
    "those", "have", "has", "had", "by", "but", "not", "from", "as", "about"
]);

function tokenizeText(text) {
    if (!text) return [];
    text = text.replace(/([a-z])([A-Z])/g, '$1 $2');
    text = text.replace(/[^\w\s\-]/g, ' ');
    const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 0);
    return words.filter(w => !STOPWORDS.has(w));
}

function stemWord(word) {
    word = word.trim().toLowerCase();
    if (word.length <= 3) return word;
    if (word.endsWith("ing")) return word.substring(0, word.length - 3);
    if (word.endsWith("ed")) return word.substring(0, word.length - 2);
    if (word.endsWith("es")) return word.substring(0, word.length - 2);
    if (word.endsWith("s") && !word.endsWith("ss")) return word.substring(0, word.length - 1);
    if (word.endsWith("tic")) return word.substring(0, word.length - 3);
    return word;
}

function embedWord(word) {
    word = word.toLowerCase();
    if (SEMANTIC_VOCAB[word]) return SEMANTIC_VOCAB[word];
    const stemmed = stemWord(word);
    if (SEMANTIC_VOCAB[stemmed]) return SEMANTIC_VOCAB[stemmed];
    for (const vocabWord in SEMANTIC_VOCAB) {
        if (vocabWord.length > 3 && (vocabWord.includes(stemmed) || stemmed.includes(vocabWord))) {
            return SEMANTIC_VOCAB[vocabWord];
        }
    }
    return Array(8).fill(0.0);
}

function embedWords(words) {
    if (!words || words.length === 0) return Array(8).fill(0.0);
    let vector = Array(8).fill(0.0);
    let count = 0;
    words.forEach(w => {
        const v = embedWord(w);
        if (v.some(x => x !== 0.0)) {
            for (let i = 0; i < 8; i++) vector[i] += v[i];
            count++;
        }
    });
    if (count === 0) return Array(8).fill(0.0);
    for (let i = 0; i < 8; i++) vector[i] /= count;
    return normalizeVector(vector);
}

function normalizeVector(vec) {
    const mag = Math.sqrt(vec.reduce((sum, x) => sum + x * x, 0));
    if (mag === 0.0) return Array(8).fill(0.0);
    return vec.map(x => x / mag);
}

function cosineSimilarity(vecA, vecB) {
    const dot = vecA.reduce((sum, a, idx) => sum + a * vecB[idx], 0);
    const magA = Math.sqrt(vecA.reduce((sum, x) => sum + x * x, 0));
    const magB = Math.sqrt(vecB.reduce((sum, x) => sum + x * x, 0));
    if (magA === 0.0 || magB === 0.0) return 0.0;
    return dot / (magA * magB);
}

function embedNode(tags, content) {
    let tagWords = [];
    tags.forEach(t => {
        tagWords = tagWords.concat(tokenizeText(t));
    });
    const contentWords = tokenizeText(content);
    
    const tagVec = embedWords(tagWords);
    const contentVec = embedWords(contentWords);
    
    const hasTags = tagVec.some(x => x !== 0.0);
    const hasContent = contentVec.some(x => x !== 0.0);
    
    if (!hasTags && !hasContent) {
        return Array(8).fill(0.1);
    } else if (!hasTags) {
        return contentVec;
    } else if (!hasContent) {
        return tagVec;
    }
    
    let blended = [];
    for (let i = 0; i < 8; i++) {
        blended.push(0.7 * tagVec[i] + 0.3 * contentVec[i]);
    }
    return normalizeVector(blended);
}

// --- DOM ELEMENTS CONTROLLERS ---
let piiToggle, topicToggle, decaySlider, decayVal, depthSlider, depthVal;
let memoryInput, memoryTags, memoryImportance, terminalOutput;
let postSelect, igMediaCard, igSlideCount, igSlideHeadline, igSlideBody, igCaptionText, postThemeBadge, igIndicators;
let gitBranchVal, gitRemoteVal, githubReleaseText, gitStatusBadge;
let onboardingOverlay, activeStorageBadge, activeNodesCountLabel;
let sidebarWorkspaceList, padlockBeliefInput, detailGlassCard, dreamSparkAlert;

// --- INITIALIZE APPLICATION ---
window.addEventListener('DOMContentLoaded', async () => {
    initDOMElements();
    setupD3Graph();
    setupEventListeners();
    await loadAgentConfig();
    await loadWatcherData();
    seedInitialMemories();
    updateRecommendation();
    
    // Check if onboarding completed previously
    if (localStorage.getItem('auramem_onboarding_complete') === 'true') {
        onboardingOverlay.classList.add('dismissed');
        logTerminal("[SYSTEM] Native Commander Dashboard online. Storage: SQLite Relational.", "success");
    } else {
        logTerminal("[SYSTEM] Stepper overlay active. Awaiting developer profiling...");
    }
});

// Dynamic configuration APIs endpoints
let agentConfig = {
    agents: {
        strategist: { enabled: true },
        pusher: { enabled: true },
        watcher: { enabled: true }
    }
};

async function loadAgentConfig() {
    try {
        const response = await fetch('/api/config');
        if (response.ok) {
            agentConfig = await response.json();
            logTerminal("[REGISTRY] Dynamic configurations synchronized from local REST endpoints.", "success");
        }
    } catch (e) {
        // Dynamic REST fallback
        const cached = localStorage.getItem('auramem_agents_config');
        if (cached) {
            agentConfig = JSON.parse(cached);
        }
    }
    updateWorkspacesSidebar();
}

function initDOMElements() {
    piiToggle = document.getElementById('guardrail-scrub-pii');
    topicToggle = document.getElementById('guardrail-blocked-topics');
    decaySlider = document.getElementById('param-decay');
    decayVal = document.getElementById('decay-val');
    depthSlider = document.getElementById('param-depth');
    depthVal = document.getElementById('depth-val');
    
    memoryInput = document.getElementById('memory-input');
    memoryTags = document.getElementById('memory-tags');
    memoryImportance = document.getElementById('memory-importance');
    terminalOutput = document.getElementById('terminal-output');

    postSelect = document.getElementById('post-select');
    igMediaCard = document.getElementById('ig-media-card');
    igSlideCount = document.getElementById('ig-slide-count');
    igSlideHeadline = document.getElementById('ig-slide-headline');
    igSlideBody = document.getElementById('ig-slide-body');
    igCaptionText = document.getElementById('ig-caption-textarea');
    postThemeBadge = document.getElementById('post-theme-badge');
    igIndicators = document.getElementById('ig-indicators');

    gitBranchVal = document.getElementById('git-branch-val');
    gitRemoteVal = document.getElementById('git-remote-val');
    githubReleaseText = document.getElementById('github-release-textarea');
    gitStatusBadge = document.getElementById('git-status-badge');
    
    onboardingOverlay = document.getElementById('onboarding-overlay');
    activeStorageBadge = document.getElementById('active-storage-mode');
    activeNodesCountLabel = document.getElementById('active-nodes-count');
    sidebarWorkspaceList = document.getElementById('agent-workspace-list');
    padlockBeliefInput = document.getElementById('padlock-belief-input');
    detailGlassCard = document.getElementById('detail-glass-card');
    dreamSparkAlert = document.getElementById('dream-spark-alert');
}

function setupEventListeners() {
    piiToggle.addEventListener('change', (e) => {
        piiScrubActive = e.target.checked;
        logTerminal(`[GUARDRAIL] PII scrubbing filter is ${piiScrubActive ? 'ACTIVE' : 'INACTIVE'}.`, 'warning');
    });
    
    topicToggle.addEventListener('change', (e) => {
        topicBlockActive = e.target.checked;
        logTerminal(`[GUARDRAIL] Restricted category enforcement ${topicBlockActive ? 'ACTIVE' : 'INACTIVE'}.`, 'warning');
    });

    decaySlider.addEventListener('input', (e) => {
        decayRate = parseFloat(e.target.value);
        decayVal.textContent = decayRate.toFixed(2);
    });

    depthSlider.addEventListener('input', (e) => {
        maxDepth = parseInt(e.target.value);
        depthVal.textContent = maxDepth;
    });
}

// --- STEPPER ONBOARDING INTERACTION ---
function selectProfile(type, value) {
    activeProfile[type] = value;
    
    // Manage active buttons class
    const envEdge = document.getElementById('env-edge');
    const envDaemon = document.getElementById('env-daemon');
    const wSingle = document.getElementById('workload-single');
    const wSwarm = document.getElementById('workload-swarm');
    
    if (type === 'env') {
        if (value === 'edge') {
            envEdge.classList.add('active');
            envDaemon.classList.remove('active');
        } else {
            envDaemon.classList.add('active');
            envEdge.classList.remove('active');
        }
    } else if (type === 'workload') {
        if (value === 'single') {
            wSingle.classList.add('active');
            wSwarm.classList.remove('active');
        } else {
            wSwarm.classList.add('active');
            wSingle.classList.remove('active');
        }
    }
    
    updateRecommendation();
}

function updateRecommendation() {
    const title = document.getElementById('rec-path-title');
    const explanation = document.getElementById('rec-path-explanation');
    const configBlock = document.getElementById('rec-config-code');
    const badge = document.getElementById('rec-path-badge');
    const recBox = document.querySelector('.recommendation-box');
    
    if (activeProfile.env === 'edge' && activeProfile.workload === 'single') {
        // Path A: JSONL
        storageMode = 'jsonl';
        badge.textContent = 'PATH A';
        title.textContent = 'Zero-Dependency JSONL Log Engine';
        explanation.textContent = 'Ideal for browser sandboxes and single-agent edge tasks. Ephemeral process-local append logging with instant edge retrieval and zero database overhead.';
        recBox.classList.remove('sqlite-rec');
        
        configBlock.textContent = JSON.stringify({
            "storage_mode": "jsonl",
            "db_path": "data/cortex_memory.jsonl",
            "system1_decay_rate": 0.10,
            "max_retrieval_depth": 8
        }, null, 2);
    } else {
        // Path B: SQLite Relational
        storageMode = 'sqlite';
        badge.textContent = 'PATH B';
        title.textContent = 'SQLite-Unified Relational Engine';
        explanation.textContent = 'Ideal for swarm concurrency and multi-agent daemons. Swaps storage to a transactional database engine, preventing write-contention lock corruption natively.';
        recBox.classList.add('sqlite-rec');
        
        configBlock.textContent = JSON.stringify({
            "storage_mode": "sqlite",
            "db_path": "data/cortex_memory.db",
            "system1_decay_rate": 0.10,
            "max_retrieval_depth": 8
        }, null, 2);
    }
}

function goToStep(step) {
    // Hide active step content
    document.querySelectorAll('.step-content').forEach(c => c.classList.remove('active'));
    document.getElementById(`step-${step}-content`).classList.add('active');
    
    // Update step dots
    document.querySelectorAll('.step-dot').forEach((dot, idx) => {
        const dotNum = idx + 1;
        dot.classList.remove('active', 'complete');
        if (dotNum < step) {
            dot.classList.add('complete');
        } else if (dotNum === step) {
            dot.classList.add('active');
        }
    });
    
    currentStep = step;
}

// Ingest immutable core ego anchors
function injectEgoDNA() {
    const belief1 = document.getElementById('ego-belief-1').value.trim();
    const belief2 = document.getElementById('ego-belief-2').value.trim();
    const belief3 = document.getElementById('ego-belief-3').value.trim();
    
    if (!belief1 || !belief2 || !belief3) {
        alert("Ego beliefs cannot be empty! Please seed all three fields to grow the agent core soul.");
        return;
    }
    
    egoBeliefs = [belief1, belief2, belief3];
    
    // Purge old nodes to seed Ego freshly
    nodes = [];
    links = [];
    
    // Add permanent Golden Ego Anchor Nodes
    egoBeliefs.forEach((belief, idx) => {
        const egoNode = {
            id: `ego_anchor_${idx + 1}`,
            content: belief,
            tags: ["EgoCore", "Directive"],
            system: "long_term",
            importance: 1.0,
            strength: 1.0, // Immutable infinite strength indicator
            accessCount: 10,
            x: 200 + idx * 150,
            y: 200 + (idx % 2 === 0 ? 60 : -60),
            fx: 200 + idx * 150, // fix positions initially so they anchor the gravity centroid
            fy: 200 + (idx % 2 === 0 ? 60 : -60),
            vector: embedNode(["EgoCore", "Directive"], belief)
        };
        nodes.push(egoNode);
    });
    
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
    
    // Push custom seeding report to step 4 console logs
    const diagTerminal = document.getElementById('diagnostic-terminal');
    diagTerminal.innerHTML = `
        <div class="con-line cyan">[SYSTEM] Core soul injected. Gravitational Ego anchors generated.</div>
        <div class="con-line cyan"> -> Anchor Node #1 ID: ego_anchor_1 (Mass: 2.0x, Strength: LOCKED INF)</div>
        <div class="con-line cyan"> -> Anchor Node #2 ID: ego_anchor_2 (Mass: 2.0x, Strength: LOCKED INF)</div>
        <div class="con-line cyan"> -> Anchor Node #3 ID: ego_anchor_3 (Mass: 2.0x, Strength: LOCKED INF)</div>
        <div class="con-line">[SYSTEM] Ready to boot Model Context Protocol connection handshakes.
    `;
    
    goToStep(4);
}

function bootHandshake() {
    const diagTerminal = document.getElementById('diagnostic-terminal');
    const bootBtn = document.getElementById('diag-boot-btn');
    const backBtn = document.getElementById('diag-back-btn');
    const launchBtn = document.getElementById('diag-launch-btn');
    
    bootBtn.disabled = true;
    backBtn.classList.add('hidden');
    
    let logs = [
        { text: "[09:41:02] [GATEWAY] Locating local process daemon...", delay: 200 },
        { text: "[09:41:02] [JSON-RPC 2.0] Transmitting tools initialize handshake frame...", delay: 500 },
        { text: "[09:41:02] [JSON-RPC 2.0] Sent: {'jsonrpc': '2.0', 'method': 'initialize', 'id': 1}", delay: 800 },
        { text: "[09:41:03] [JSON-RPC 2.0] Received INITIALIZE response. Protocol: v2024-11-05. Secure client confirmed.", delay: 1100, type: 'cyan' },
        { text: "[09:41:03] [CORTEX] Ingesting multi-agent sandboxing verification suite...", delay: 1400 },
        { text: "[09:41:03] [SANDBOX] Agent isolating namespaces default -> hermes verified cleanly. [NO WORKSPACE BLEEDING]", delay: 1700, type: 'cyan' },
        { text: "[09:41:03] [SQLITE] Testing sharded relational hot-swapping under write contention...", delay: 2000 },
        { text: "[09:41:04] [SQLITE] Relational write-safety confirmed. core/config.json updated to 'sqlite'.", delay: 2300, type: 'cyan' },
        { text: "[09:41:04] [DATABASE] Zero data loss relational migrations verified. [100% CORRECTNESS]", delay: 2600, type: 'success' },
        { text: "✓ MCP NATIVE GATEWAY ONLINE [100% CORRECTNESS]. System secure.", delay: 2900, type: 'success' }
    ];
    
    logs.forEach(log => {
        setTimeout(() => {
            const div = document.createElement('div');
            div.className = `con-line ${log.type || ''}`;
            div.textContent = log.text;
            diagTerminal.appendChild(div);
            diagTerminal.scrollTop = diagTerminal.scrollHeight;
            
            // On complete
            if (log.type === 'success' && log.text.includes("MCP NATIVE")) {
                bootBtn.classList.add('hidden');
                launchBtn.classList.remove('hidden');
            }
        }, log.delay);
    });
}

function dismissOnboarding() {
    onboardingOverlay.classList.add('dismissed');
    localStorage.setItem('auramem_onboarding_complete', 'true');
    
    // Set dynamic indicators
    activeStorageBadge.textContent = storageMode.toUpperCase();
    activeStorageBadge.className = `metric-value font-mono ${storageMode === 'sqlite' ? 'purple-glow' : 'cyan-glow'}`;
    
    logTerminal("[SYSTEM] Onboarding stepper diagnostics passed. Sovereign Commander Console active.", "success");
    logTerminal(`[SYSTEM] Initialized dual-system memory engine on path: data/cortex_memory.${storageMode === 'sqlite' ? 'db' : 'jsonl'}`);
    
    // Release fixed positions of Ego Anchors so they interact organically
    nodes.forEach(n => {
        if (n.id.startsWith("ego_anchor_")) {
            n.fx = null;
            n.fy = null;
        }
    });
    simulation.alpha(1).restart();
}

// --- WORKSPACE LIBRARY SIDEBAR ---
let activeAgentList = [
    { id: 'default', engine: 'SQLITE', rate: '0.10', active: true },
    { id: 'hermes', engine: 'SQLITE', rate: '0.15', active: false },
    { id: 'claw_bot', engine: 'JSONL', rate: '0.05', active: false }
];

function updateWorkspacesSidebar() {
    sidebarWorkspaceList.innerHTML = '';
    activeAgentList.forEach(agent => {
        const div = document.createElement('div');
        div.className = `agent-workspace-card ${agent.id === activeWorkspace ? 'active' : ''}`;
        div.onclick = () => switchWorkspace(agent.id);
        div.innerHTML = `
            <div class="card-header-row">
                <span class="agent-id-tag font-mono">${agent.id}</span>
                <span class="engine-indicator">${agent.engine}</span>
            </div>
            <div class="card-body-row">
                <span class="card-sub-info">Decay rate: ${agent.rate} / sweep</span>
                <span class="card-status-dot ${agent.id === activeWorkspace ? 'active' : ''}"></span>
            </div>
        `;
        sidebarWorkspaceList.appendChild(div);
    });
    
    activeNodesCountLabel.textContent = nodes.length;
}

function switchWorkspace(namespace) {
    if (namespace === activeWorkspace) return;
    
    logTerminal(`[SYSTEM] Switching workspace namespace: ${activeWorkspace} ➔ ${namespace}...`, 'info');
    activeWorkspace = namespace;
    
    // Emulate switching and seeding memories unique to namespace
    nodes = [];
    links = [];
    
    // Seed golden ego anchors unique to workspace
    egoBeliefs.forEach((belief, idx) => {
        nodes.push({
            id: `ego_anchor_${idx + 1}`,
            content: belief,
            tags: ["EgoCore", "Directive"],
            system: "long_term",
            importance: 1.0,
            strength: 1.0,
            accessCount: 10,
            x: 300,
            y: 250,
            vector: embedNode(["EgoCore", "Directive"], belief)
        });
    });
    
    if (namespace === 'default') {
        seedInitialMemories();
    } else if (namespace === 'hermes') {
        createNode("Hermes agent must process sub-millisecond core queries.", ["AI", "Hermes"], "working", 0.8, 1.0);
        createNode("Multi-agent pipelines can suffer structural friction under loose sandboxing.", ["Architecture", "Safety"], "working", 0.7, 1.0);
    } else {
        createNode("Claw Bot sequential search actions crawler.", ["Claw", "Web"], "working", 0.6, 1.0);
    }
    
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
    updateWorkspacesSidebar();
}

function createNewAgentNamespace() {
    const input = document.getElementById('new-workspace-id');
    const val = input.value.trim().toLowerCase().replace(/[^a-z0-9_-]/g, '');
    
    if (!val) {
        alert("Enter a valid namespace alphanumeric ID.");
        return;
    }
    
    // Check if exists
    if (activeAgentList.some(a => a.id === val)) {
        alert("Namespace already registered.");
        return;
    }
    
    activeAgentList.push({
        id: val,
        engine: storageMode.toUpperCase(),
        rate: '0.10',
        active: false
    });
    
    logTerminal(`[REGISTRY] New sandboxed multi-agent namespace created: '${val}'. Ready for telemetry.`, 'success');
    input.value = '';
    updateWorkspacesSidebar();
    switchWorkspace(val);
}

// --- CONVERSATION WATCHER DATA SYNC ---
async function loadWatcherData() {
    try {
        const response = await fetch('../data/watcher_data.json');
        if (!response.ok) throw new Error("Missing watcher data JSON file.");
        
        const data = await response.json();
        instagramPosts = data.instagram_posts;
        
        postSelect.innerHTML = '';
        instagramPosts.forEach((post, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = post.title.split(':')[0];
            postSelect.appendChild(opt);
        });
        
        loadInstagramPost();
        
        const milestones = data.summary.milestones || [];
        updateGitHubReleaseNotes(milestones);
        logTerminal("[SYSTEM] Watcher Agent reports successfully mapped inside the bottom accordion reviewed drawer.", "success");
        
    } catch (err) {
        // Fallback structures if file is not found
        instagramPosts = [
            {
                "title": "Post 1: The AI Memory Lie Nobody Tells You",
                "hook": "❌ Traditional vector DBs are KILLING your AI agent's speed.",
                "theme": "Educational Hook",
                "slides": [
                    { "slide_num": 1, "headline": "The AI Memory Lie 🧠", "body": "Everyone thinks AI agents remember things because of 'Vector Databases'. But middleware wrappers slow down agents and add unnecessary layers. Here is how we build NATIVE memory..." },
                    { "slide_num": 2, "headline": "The Middleware Problem 🔌", "body": "LLM -> Tool Call -> Vector DB -> Embeddings -> Search -> Prompt Inject. This is NOT how humans think. It makes AI feel laggy and disconnected. We need a dual-system cognitive brain." },
                    { "slide_num": 3, "headline": "System 1 vs System 2 ⚡️", "body": "- System 1 (Working Memory): Ephemeral, high-decay, holds immediate chat tokens.\n- System 2 (Long-Term): Consolidated knowledge that is permanently linked through semantic tag weight." }
                ],
                "cta": "💡 Want to build native AI brains that think like humans? Comment 'MEMORY' and I'll send you the Github repository link directly!",
                "hashtags": "#AIAgents #AgenticMemory #SoftwareEngineering"
            }
        ];
        
        postSelect.innerHTML = '';
        instagramPosts.forEach((post, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = post.title.split(':')[0];
            postSelect.appendChild(opt);
        });
        loadInstagramPost();
        
        updateGitHubReleaseNotes([
            "System Core: Created cortex_memory.py containing the dual-system memory engine.",
            "Watcher Agent: Created watcher_agent.py to parse logs and write content.",
            "Visual Interface: Designed high-fidelity canvas graph for memory visualization."
        ]);
    }
}

function updateGitHubReleaseNotes(milestones) {
    let text = `# 🧠 AURAMEMORY: LAYERLESS NATIVE COGNITIVE MEMORY ENGINE (v1.1.17) 🚀\n\n`;
    text += `Standard RAG architectures rely on slow, complex vector database middleware wrappers. AuraMemory replaces this with a layerless, native cognitive engine executing dual-system memory loops inside agent processes.\n\n`;
    text += `## 🚀 Active Milestones\n`;
    milestones.forEach(m => {
        text += `- ${m}\n`;
    });
    text += `\nStar us on GitHub to follow active development! ⭐`;
    githubReleaseText.value = text;
}

function loadInstagramPost() {
    activePostIndex = parseInt(postSelect.value);
    activeSlideIndex = 0;
    
    const post = instagramPosts[activePostIndex];
    if (!post) return;
    
    postThemeBadge.textContent = post.theme;
    
    let captionText = `🔥 INSIGHTS FROM THE BRAIN: ${post.hook}\n\n`;
    post.slides.forEach(s => {
        captionText += `Slide ${s.slide_num}: ${s.headline}\n👉 ${s.body}\n\n`;
    });
    captionText += `💡 CTA: ${post.cta}\n\n`;
    captionText += `${post.hashtags}`;
    
    igCaptionText.value = captionText;
    
    igIndicators.innerHTML = '';
    post.slides.forEach((_, sIdx) => {
        const ind = document.createElement('span');
        ind.className = `indicator ${sIdx === 0 ? 'active' : ''}`;
        igIndicators.appendChild(ind);
    });
    
    renderMockPhoneSlide();
}

function renderMockPhoneSlide() {
    const post = instagramPosts[activePostIndex];
    if (!post) return;
    const slide = post.slides[activeSlideIndex];
    if (!slide) return;
    
    igSlideCount.textContent = `SLIDE ${slide.slide_num}/${post.slides.length}`;
    igSlideHeadline.textContent = slide.headline;
    igSlideBody.textContent = slide.body;
    
    const indicators = igIndicators.querySelectorAll('.indicator');
    indicators.forEach((ind, sIdx) => {
        if (sIdx === activeSlideIndex) ind.classList.add('active');
        else ind.classList.remove('active');
    });
}

function nextSlide() {
    const post = instagramPosts[activePostIndex];
    if (post && activeSlideIndex < post.slides.length - 1) {
        activeSlideIndex++;
        renderMockPhoneSlide();
    }
}

function prevSlide() {
    if (activeSlideIndex > 0) {
        activeSlideIndex--;
        renderMockPhoneSlide();
    }
}

function copyCaptionText() {
    igCaptionText.select();
    document.execCommand('copy');
    logTerminal(`[SYSTEM] Instagram Caption copied to clipboard successfully!`, 'success');
}

function copyGitHubReleaseNotes() {
    githubReleaseText.select();
    document.execCommand('copy');
    logTerminal(`[SYSTEM] GitHub Release Notes copied to clipboard successfully!`, 'success');
}

function copyCLICommand() {
    const codeElem = document.getElementById('cli-command-code');
    const range = document.createRange();
    range.selectNode(codeElem);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
    logTerminal(`[SYSTEM] CLI Sync command copied!`, 'success');
}

// --- D3.JS FORCE DIRECTED GRAPH WEB GRAPH ---
function setupD3Graph() {
    const container = document.getElementById('svg-graph-container');
    const width = container.clientWidth;
    const height = container.clientHeight || 520;
    
    svg = d3.select("#memory-svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .call(d3.zoom().on("zoom", (event) => {
            containerGroup.attr("transform", event.transform);
        }))
        .append("g");
        
    const containerGroup = svg.append("g");
    
    // Setup D3 simulation forces
    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id).distance(120).strength(d => d.strength))
        .force("charge", d3.forceManyBody().strength(-1500).distanceMax(250))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(nodeRadius + 15))
        .on("tick", ticked);
        
    linkGroup = containerGroup.append("g").attr("class", "links");
    nodeGroup = containerGroup.append("g").attr("class", "nodes");
}

function ticked() {
    const container = document.getElementById('svg-graph-container');
    const w = container.clientWidth;
    const h = container.clientHeight || 520;

    linkGroup.selectAll("line")
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
        
    nodeGroup.selectAll(".node")
        .attr("transform", d => {
            // Keep in bounds
            d.x = Math.max(nodeRadius + 20, Math.min(w - nodeRadius - 20, d.x));
            d.y = Math.max(nodeRadius + 20, Math.min(h - nodeRadius - 20, d.y));
            return `translate(${d.x}, ${d.y})`;
        });
}

function updateD3Graph() {
    // 1. Data Bind Links
    const l = linkGroup.selectAll("line")
        .data(links, d => `${d.source}-${d.target}`);
        
    l.exit().remove();
    
    const lEnter = l.enter().append("line")
        .attr("stroke", "rgba(139, 92, 246, 0.2)")
        .attr("stroke-width", d => 1.5 + d.strength * 2.5);
        
    const mergedLinks = lEnter.merge(l);
    
    // 2. Data Bind Nodes
    const n = nodeGroup.selectAll(".node")
        .data(nodes, d => d.id);
        
    n.exit().transition()
        .duration(600)
        .style("opacity", 0)
        .style("transform", "scale(0.1)")
        .remove();
        
    const nEnter = n.enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
            
    // Nodes Inner Gradient circle
    nEnter.append("circle")
        .attr("r", nodeRadius)
        .attr("stroke-width", 2)
        .attr("class", d => d.system === 'long_term' ? (d.id.startsWith("ego_") ? 'stroke-gold' : 'stroke-purple') : 'stroke-cyan')
        .style("fill", d => {
            if (d.system === 'long_term') {
                return d.id.startsWith("ego_") ? 'url(#grad-gold)' : 'url(#grad-purple)';
            }
            return 'url(#grad-cyan)';
        });
        
    // Text labels S1/S2/Ego
    nEnter.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "-2px")
        .attr("fill", "#FFF")
        .style("font-family", "Outfit")
        .style("font-size", "11px")
        .style("font-weight", "700")
        .text(d => d.id.startsWith("ego_anchor_") ? "EGO" : (d.system === 'long_term' ? "S2" : "S1"));
        
    // Subtext strength rating
    nEnter.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "10px")
        .attr("fill", d => d.system === 'long_term' ? (d.id.startsWith("ego_") ? '#FBBF24' : '#D8B4FE') : '#67E8F9')
        .style("font-family", "Fira Code")
        .style("font-size", "8px")
        .text(d => d.system === 'long_term' ? "INF" : d.strength.toFixed(2));
        
    // Interactivity bindings
    nEnter.on("mouseover", (event, d) => {
        showFloatingNodeDetails(d);
        // Recalculate intermediate sparks overlays on-the-fly
        scanSynapticGaps(d);
    }).on("mouseout", () => {
        // Keep card open unless they click away
    });
    
    // Pulse ring overlays if pulse timer is active
    nEnter.filter(d => d.pulseTimer > 0)
        .append("circle")
        .attr("class", "pulse-ring")
        .attr("r", nodeRadius + 10)
        .attr("fill", "none")
        .attr("stroke", d => d.system === 'long_term' ? '#8B5CF6' : '#06B6D4')
        .attr("stroke-width", 2)
        .style("opacity", 0.7)
        .transition()
        .duration(1200)
        .attr("r", nodeRadius + 28)
        .style("opacity", 0)
        .remove();

    const mergedNodes = nEnter.merge(n);
    
    // Update forces data
    simulation.nodes(nodes);
    simulation.force("link").links(links);
    simulation.alpha(0.3).restart();
    
    // Add SVG Gradients once
    if (d3.select("#svg-grads").empty()) {
        const defs = d3.select("#memory-svg").append("defs").attr("id", "svg-grads");
        
        // Cyan S1
        const gCyan = defs.append("radialGradient").attr("id", "grad-cyan");
        gCyan.append("stop").attr("offset", "0%").attr("stop-color", "rgba(6, 182, 212, 0.45)");
        gCyan.append("stop").attr("offset", "100%").attr("stop-color", "rgba(13, 148, 136, 0.95)");

        // Purple S2
        const gPurple = defs.append("radialGradient").attr("id", "grad-purple");
        gPurple.append("stop").attr("offset", "0%").attr("stop-color", "rgba(139, 92, 246, 0.5)");
        gPurple.append("stop").attr("offset", "100%").attr("stop-color", "rgba(79, 70, 229, 0.95)");

        // Gold Ego
        const gGold = defs.append("radialGradient").attr("id", "grad-gold");
        gGold.append("stop").attr("offset", "0%").attr("stop-color", "rgba(251, 191, 36, 0.6)");
        gGold.append("stop").attr("offset", "100%").attr("stop-color", "rgba(217, 119, 6, 0.95)");
    }
}

// Drag behaviors
function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function recalculateSemanticLinks() {
    links = [];
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const n1 = nodes[i];
            const n2 = nodes[j];
            
            const sim = cosineSimilarity(n1.vector, n2.vector);
            if (sim >= 0.20) {
                const strength = 0.2 + (0.875 * (sim - 0.20));
                links.push({
                    source: n1.id,
                    target: n2.id,
                    strength: Math.min(0.9, strength)
                });
            }
        }
    }
    
    activeNodesCountLabel.textContent = nodes.length;
}

// --- AFFECTIVE CENTROID GAUGES MATH ---
function calculateEmotionalCentroids() {
    if (nodes.length === 0) return;
    
    // Centroid Vector Math
    let centroid = Array(8).fill(0.0);
    nodes.forEach(node => {
        // Double weight Ego anchors for gravity centroids
        const w = node.id.startsWith("ego_") ? 2.5 : 1.0;
        for (let i = 0; i < 8; i++) {
            centroid[i] += node.vector[i] * w * (node.strength || 1.0);
        }
    });
    
    // Average
    const N = nodes.length;
    for (let i = 0; i < 8; i++) centroid[i] /= N;
    
    // Map dimensions to 5 circular dial affective coordinates
    centroids.curiosity = Math.min(1.0, Math.max(0.1, (centroid[0] * 1.5) + (centroid[6] * 0.5)));
    centroids.caution = Math.min(1.0, Math.max(0.1, (centroid[2] * 0.8) + (centroid[3] * 1.8)));
    centroids.sociability = Math.min(1.0, Math.max(0.1, (centroid[4] * 1.4) + (centroid[5] * 0.8)));
    centroids.sovereignty = Math.min(1.0, Math.max(0.1, (centroid[2] * 1.5) + (centroid[1] * 0.7)));
    centroids.creativity = Math.min(1.0, Math.max(0.1, (centroid[7] * 1.6) + (centroid[0] * 0.6)));
    
    // Animate dials
    animateDial('curiosity', centroids.curiosity);
    animateDial('caution', centroids.caution);
    animateDial('sociability', centroids.sociability);
    animateDial('sovereignty', centroids.sovereignty);
    animateDial('creativity', centroids.creativity);
}

function animateDial(label, val) {
    const circle = document.getElementById(`gauge-${label}`);
    const labelVal = document.getElementById(`val-${label}`);
    if (!circle || !labelVal) return;
    
    const maxDash = 100;
    const percentage = Math.round(val * 100);
    circle.setAttribute("stroke-dasharray", `${percentage}, ${maxDash}`);
    labelVal.textContent = val.toFixed(2);
}

// Sliders adversarial simulation loops
function simulateAdversarial(val) {
    const percentLabel = document.getElementById('slider-val-adversarial');
    percentLabel.textContent = `${val}%`;
    
    const modifier = parseFloat(val) / 100;
    
    // Recalculate caution dials artificially surging
    centroids.caution = Math.min(1.0, 0.20 + (modifier * 0.78));
    centroids.sovereignty = Math.min(1.0, 0.75 + (modifier * 0.22));
    centroids.curiosity = Math.max(0.05, 0.85 - (modifier * 0.7));
    
    animateDial('caution', centroids.caution);
    animateDial('sovereignty', centroids.sovereignty);
    animateDial('curiosity', centroids.curiosity);
    
    // Artificially compact nodes by adjusting force repulsion strength down
    // (Mind turns defensive and packs semantic nodes tight!)
    const defensiveRepulsion = -1500 + (modifier * 1000);
    simulation.force("charge", d3.forceManyBody().strength(defensiveRepulsion).distanceMax(250));
    simulation.alpha(0.5).restart();
}

function simulateLearning(val) {
    const percentLabel = document.getElementById('slider-val-learning');
    percentLabel.textContent = `${val}%`;
    
    const modifier = parseFloat(val) / 100;
    
    // Recalculate dial curiosity surging
    centroids.curiosity = Math.min(1.0, 0.1 + (modifier * 0.9));
    centroids.creativity = Math.min(1.0, 0.3 + (modifier * 0.7));
    centroids.caution = Math.max(0.05, 0.20 - (modifier * 0.15));
    
    animateDial('curiosity', centroids.curiosity);
    animateDial('creativity', centroids.creativity);
    animateDial('caution', centroids.caution);
    
    // Scale nodes repulsion out (Mind is curious and expanding semantic links space!)
    const curiousRepulsion = -1500 - (modifier * 1200);
    simulation.force("charge", d3.forceManyBody().strength(curiousRepulsion).distanceMax(250));
    simulation.alpha(0.5).restart();
}

// --- INTERACTIVE SANDBOX INGUEST & RECALLS ---
function createNode(content, tags, system, importance, strength) {
    const node = {
        id: `node_${Math.random().toString(36).substring(2, 8)}`,
        content,
        tags,
        system,
        importance,
        strength,
        accessCount: 1,
        x: 300 + (Math.random() - 0.5) * 80,
        y: 250 + (Math.random() - 0.5) * 80,
        vector: embedNode(tags, content)
    };
    nodes.push(node);
    return node;
}

function commitNewMemory() {
    const text = memoryInput.value.trim();
    if (!text) {
        logTerminal("[SANDBOX] Input memory content cannot be empty!", "error");
        return;
    }
    
    const tagsInput = memoryTags.value.split(',').map(t => t.trim()).filter(t => t.length > 0);
    const importance = parseFloat(memoryImportance.value);
    
    logTerminal(`[PROCESS] Analysing ingestion entry: "${text.substring(0, 45)}..."`);
    
    // 1. Scrub PII
    let processedText = text;
    let scrubbedItems = [];
    
    if (piiScrubActive) {
        const emailRegex = /[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/gi;
        const keyRegex = /(?:key|token|auth|password|secret)[a-zA-Z0-9_\-\:\=\+\/]{5,32}/gi;
        
        if (emailRegex.test(processedText)) {
            scrubbedItems.push("EMAIL");
            processedText = processedText.replace(emailRegex, "<EMAIL_SCRUBBED>");
        }
        if (keyRegex.test(processedText)) {
            scrubbedItems.push("API_KEY");
            processedText = processedText.replace(keyRegex, "<API_KEY_SCRUBBED>");
        }
    }
    
    if (scrubbedItems.length > 0) {
        logTerminal(`[GUARDRAIL] PII Ingestion filter active. Scrubbed elements: ${scrubbedItems.join(", ")}`, 'warning');
    }
    
    // 2. Block restricted topics
    let topicViolations = [];
    if (topicBlockActive) {
        const blockedWords = ['malware', 'hacking', 'insider-trading', 'malicious'];
        blockedWords.forEach(word => {
            if (processedText.toLowerCase().includes(word)) {
                topicViolations.push(word.toUpperCase());
            }
        });
    }
    
    if (topicViolations.length > 0) {
        logTerminal(`[GUARDRAIL] CRITICAL: Category restriction violation on "${topicViolations.join(", ")}". Ingestion rejected!`, 'error');
        triggerAlertNotification(`GUARDRAIL ENFORCEMENT: Entry rejected due to blocked category directive "${topicViolations[0]}".`);
        memoryInput.value = '';
        return;
    }
    
    // Add Node
    const node = createNode(processedText, tagsInput, "working", importance, 1.0);
    node.pulseTimer = 180;
    
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
    
    logTerminal(`[SYSTEM-1] Node committed successfully. ID: ${node.id}. system: WORKING. Recalculated semantic connections.`, 'success');
    memoryInput.value = '';
}

function recallMemoryQuery() {
    const text = memoryInput.value.trim();
    const tagsInput = memoryTags.value.split(',').map(t => t.trim()).filter(t => t.length > 0);
    
    if (!text && tagsInput.length === 0) {
        logTerminal("[SANDBOX] Input tags or search text above to recall associative nodes.", "warning");
        return;
    }
    
    const tokens = [];
    tagsInput.forEach(t => tokens.push(...tokenizeText(t)));
    if (text) tokens.push(...tokenizeText(text));
    
    logTerminal(`[RECALL] Crawling semantic KD-tree associative vector fields...`);
    
    const queryVector = embedWords(tokens);
    let matches = [];
    
    nodes.forEach(node => {
        const sim = cosineSimilarity(queryVector, node.vector);
        if (sim >= 0.20) {
            matches.push({ node, sim });
            node.accessCount++;
            node.strength = Math.min(1.0, node.strength + 0.15); // refresh working strength
            node.pulseTimer = 180;
        }
    });
    
    if (matches.length === 0) {
        logTerminal("[RECALL] Zero relevant nodes located inside the associative workspaces.", "warning");
    } else {
        matches.sort((a, b) => b.sim - a.sim);
        logTerminal(`[RECALL] Retrieval finished. Located ${matches.length} matching nodes! (Highest CosSim: ${matches[0].sim.toFixed(2)})`, 'success');
        matches.forEach(m => {
            logTerminal(` - Node: "${m.node.content.substring(0, 30)}..." [Similarity: ${m.sim.toFixed(2)}]`, 'info');
        });
        updateD3Graph();
        calculateEmotionalCentroids();
    }
}

// Ingest Ego permanent anchors from the Dashboard Lockbox panel
function commitEgoFromDashboard() {
    const input = document.getElementById('padlock-belief-input');
    const val = input.value.trim();
    
    if (!val) {
        logTerminal("[SANDBOX] Padlock belief input cannot be empty!", "error");
        return;
    }
    
    const egoNode = {
        id: `ego_anchor_${nodes.length + 1}`,
        content: val,
        tags: ["EgoCore", "Lockbox"],
        system: "long_term",
        importance: 1.0,
        strength: 1.0, // Permanent locked infinite strength
        accessCount: 5,
        x: 300,
        y: 250,
        vector: embedNode(["EgoCore", "Lockbox"], val)
    };
    
    nodes.push(egoNode);
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
    
    logTerminal(`[EGOCORE] Seeded new permanent locked anchor node: "${val.substring(0, 30)}..."`, 'success');
    input.value = '';
}

// Floating details glass card inside center panel
function showFloatingNodeDetails(node) {
    const idLabel = document.getElementById('detail-node-id');
    const sysLabel = document.getElementById('detail-node-system');
    const bodyText = document.getElementById('detail-node-content');
    const accessLabel = document.getElementById('detail-node-access');
    const strengthLabel = document.getElementById('detail-node-strength');
    const tagsLabel = document.getElementById('detail-node-tags');
    
    idLabel.textContent = node.id;
    sysLabel.textContent = node.id.startsWith("ego_") ? "EGO CORE" : (node.system === 'long_term' ? "System 2" : "System 1");
    sysLabel.className = `detail-node-system ${node.id.startsWith("ego_") ? 'bg-gold' : (node.system === 'long_term' ? 'bg-purple' : 'bg-cyan')}`;
    
    bodyText.textContent = node.content;
    accessLabel.textContent = node.accessCount;
    strengthLabel.textContent = node.system === 'long_term' ? "INF" : node.strength.toFixed(2);
    tagsLabel.textContent = `[${node.tags.join(', ')}]`;
    
    detailGlassCard.classList.remove('hidden');
}

// Synaptic Gap bridge generator scanning
function scanSynapticGaps(hovered) {
    if (nodes.length < 2) return;
    
    // Find a node that has a low-intermediate cosine similarity to target
    let bestBridge = null;
    let minDiffSim = 0.20;
    
    nodes.forEach(node => {
        if (node.id !== hovered.id && !node.id.startsWith("ego_")) {
            const sim = cosineSimilarity(hovered.vector, node.vector);
            // Intermediate bridge threshold
            if (sim > 0.08 && sim < 0.22) {
                bestBridge = node;
                minDiffSim = sim;
            }
        }
    });
    
    if (bestBridge) {
        document.getElementById('spark-term-a').textContent = `"${hovered.tags[0] || 'term_A'}"`;
        document.getElementById('spark-term-b').textContent = `"${bestBridge.tags[0] || 'term_B'}"`;
        dreamSparkAlert.querySelector('#dream-spark-alert button').onclick = () => synthesizeConceptBridge(hovered, bestBridge);
        dreamSparkAlert.classList.remove('hidden');
    } else {
        dreamSparkAlert.classList.add('hidden');
    }
}

function dismissSparkAlert() {
    dreamSparkAlert.classList.add('hidden');
}

function synthesizeConceptBridge(nodeA, nodeB) {
    if (!nodeA || !nodeB) {
        dismissSparkAlert();
        return;
    }
    
    // Create intermediate bridge node dynamically
    const bridgeText = `Synthesized bridge combining workspace concept [${nodeA.tags.join(",")}] and [${nodeB.tags.join(",")}]`;
    const bridgeTags = [...new Set([...nodeA.tags, ...nodeB.tags, "Bridge"])];
    
    const node = createNode(bridgeText, bridgeTags, "working", 0.7, 1.0);
    node.pulseTimer = 180;
    
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
    
    logTerminal(`[SYNAPSE] Synthesis Bridge locked: Created intermediate node ${node.id} linking '${nodeA.id}' and '${nodeB.id}'.`, 'success');
    dismissSparkAlert();
}

function runConsolidationCycle() {
    logTerminal("[CONSOLIDATION] Spinning up dual-system memory consolidator worker...");
    
    let promoted = [];
    let decayed = [];
    let remaining = [];
    
    nodes.forEach(node => {
        if (node.id.startsWith("ego_")) {
            remaining.push(node); // Ego locks never decay
            return;
        }
        
        if (node.system === 'working') {
            const cogScore = (node.importance * 0.4) + (Math.min(node.accessCount / 5, 1.0) * 0.6);
            if (cogScore >= 0.55) {
                // Promote LTM
                node.system = 'long_term';
                node.strength = 1.0; // inf
                promoted.push(node.id);
                logTerminal(`[SYSTEM-2] Consolidated & Promoted: "${node.content.substring(0, 32)}..." ➔ S2`, 'success');
            } else {
                // Decay S1
                node.strength = node.strength - decayRate;
                if (node.strength <= 0.0) {
                    decayed.push(node.id);
                    logTerminal(`[PRUNED] Short-term S1 node decayed completely. Deleted: ${node.id}`, 'warning');
                } else {
                    remaining.push(node);
                }
            }
        } else {
            remaining.push(node);
        }
    });
    
    nodes = remaining;
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
    
    logTerminal(`[CONSOLIDATION] Worker finished. Promoted to S2: ${promoted.length}. Decayed & Purged: ${decayed.length}.`, 'info');
}

// Custom trigger alerts and screen shakes
function triggerAlertNotification(msg) {
    const alertBox = document.getElementById('canvas-alert');
    const alertText = document.getElementById('canvas-alert-text');
    alertText.textContent = msg;
    
    alertBox.classList.add('show');
    
    // Screen shake the visualizer panel
    const canvasPanel = document.querySelector('.visualizer-panel');
    canvasPanel.classList.add('shake-panel');
    canvasPanel.style.borderColor = 'rgba(239, 68, 68, 0.7)';
    
    setTimeout(() => {
        alertBox.classList.remove('show');
        canvasPanel.classList.remove('shake-panel');
        canvasPanel.style.borderColor = '';
    }, 3000);
}

// Seed initial memory nodes
function seedInitialMemories() {
    createNode("I am learning how to build agentic memory modules natively.", ["AI", "AgenticMemory"], "working", 0.8, 1.0);
    createNode("AI Architecture Design: Zero-Dependency Dual-System Core", ["AI", "Architecture"], "working", 0.9, 1.0);
    createNode("Instagram content should have high hooks to attract followers.", ["Marketing", "Instagram"], "working", 0.4, 1.0);
    
    recalculateSemanticLinks();
    updateD3Graph();
    calculateEmotionalCentroids();
}

// Clear sandbox stdio logs
function clearLogs() {
    terminalOutput.innerHTML = '';
}

function logTerminal(msg, type = 'info') {
    const line = document.createElement('div');
    line.className = `log-line log-${type}`;
    line.textContent = `${new Date().toLocaleTimeString()} ${msg}`;
    terminalOutput.appendChild(line);
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

// --- COGNITIVE EVOLUTION BOTTOM SHELF ACCORDION ---
function toggleEvolutionDrawer() {
    const panel = document.querySelector('.evolution-drawer-panel');
    const indicator = document.getElementById('drawer-toggle-indicator');
    
    if (panel.classList.contains('collapsed')) {
        panel.classList.remove('collapsed');
        indicator.textContent = '▲';
    } else {
        panel.classList.add('collapsed');
        indicator.textContent = '▼';
    }
}

function toggleAccordionItem(element) {
    const item = element.parentElement;
    const allItems = document.querySelectorAll('.accordion-item');
    const isOpen = item.classList.contains('open');
    
    // Close others
    allItems.forEach(i => i.classList.remove('open'));
    
    if (!isOpen) {
        item.classList.add('open');
    }
}

// Emulate AuraWiki compilation
function compileAuraWiki() {
    logTerminal("[CORTEX] Initiating AuraWiki Markdown obsidian double-linked compiler...", "info");
    setTimeout(() => {
        logTerminal("✓ Compiled Wiki index: reports/agentic_memory_report.md compiled successfully.", "success");
    }, 600);
}
