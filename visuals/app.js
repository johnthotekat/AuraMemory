/* AuraMemory Frontend Controller: app.js */

// --- GLOBAL STATE ---
let nodes = [];
let links = [];
let blockedTopics = ['hacking', 'malware', 'insider-trading'];
let piiScrubActive = true;
let topicBlockActive = true;
let decayRate = 0.10;
let maxDepth = 8;

let activePostIndex = 0;
let activeSlideIndex = 0;
let instagramPosts = [];

// Canvas Simulation Physics Config
const physics = {
    repulsion: 1800,
    attraction: 0.08,
    damping: 0.85,
    nodeRadius: 28,
    boundaryPadding: 40
};

// Drag and drop state
let draggedNode = null;
let hoveredNode = null;
let mouse = { x: 0, y: 0, px: 0, py: 0 };
let offset = { x: 0, y: 0 };

// --- NATIVE SEMANTIC EMBEDDINGS ENGINE ---
const SEMANTIC_VOCAB = {
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

// --- DOM ELEMENTS ---
let canvas, ctx;
let piiToggle, topicToggle, decaySlider, decayVal, depthSlider, depthVal;
let blockedKeywordsList, newKeywordInput;
let memoryInput, memoryTags, memoryImportance, terminalOutput;
let postSelect, igMediaCard, igSlideCount, igSlideHeadline, igSlideBody, igCaptionText, postThemeBadge, igIndicators;
let gitBranchVal, gitRemoteVal, githubReleaseText, gitStatusBadge;

// --- INITIALIZE APP ---
window.addEventListener('DOMContentLoaded', async () => {
    initDOMElements();
    setupCanvas();
    setupEventListeners();
    await loadWatcherData();
    seedInitialMemories();
    requestAnimationFrame(simulationLoop);
});

function initDOMElements() {
    canvas = document.getElementById('memory-canvas');
    ctx = canvas.getContext('2d');

    piiToggle = document.getElementById('guardrail-scrub-pii');
    topicToggle = document.getElementById('guardrail-blocked-topics');
    decaySlider = document.getElementById('param-decay');
    decayVal = document.getElementById('decay-val');
    depthSlider = document.getElementById('param-depth');
    depthVal = document.getElementById('depth-val');
    
    blockedKeywordsList = document.getElementById('blocked-keywords');
    newKeywordInput = document.getElementById('new-keyword');
    
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
}

function setupCanvas() {
    const resize = () => {
        const container = canvas.parentElement;
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight || 400;
    };
    resize();
    window.addEventListener('resize', resize);
}

function setupEventListeners() {
    // Control bindings
    piiToggle.addEventListener('change', (e) => {
        piiScrubActive = e.target.checked;
        logTerminal(`[GUARDRAIL] PII scrubbing ${piiScrubActive ? 'ENABLED' : 'DISABLED'}.`, 'warning');
    });
    
    topicToggle.addEventListener('change', (e) => {
        topicBlockActive = e.target.checked;
        logTerminal(`[GUARDRAIL] Topic restrictions ${topicBlockActive ? 'ENABLED' : 'DISABLED'}.`, 'warning');
    });

    decaySlider.addEventListener('input', (e) => {
        decayRate = parseFloat(e.target.value);
        decayVal.textContent = decayRate.toFixed(2);
    });

    depthSlider.addEventListener('input', (e) => {
        maxDepth = parseInt(e.target.value);
        depthVal.textContent = maxDepth;
    });

    // Canvas Mouse listeners
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;

        // Check if node is clicked
        draggedNode = findNodeAt(mouse.x, mouse.y);
        if (draggedNode) {
            offset.x = draggedNode.x - mouse.x;
            offset.y = draggedNode.y - mouse.y;
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;

        if (draggedNode) {
            draggedNode.x = mouse.x + offset.x;
            draggedNode.y = mouse.y + offset.y;
            draggedNode.vx = 0;
            draggedNode.vy = 0;
        }

        hoveredNode = findNodeAt(mouse.x, mouse.y);
        canvas.style.cursor = draggedNode ? 'grabbing' : (hoveredNode ? 'pointer' : 'default');
    });

    canvas.addEventListener('mouseup', () => {
        draggedNode = null;
    });

    canvas.addEventListener('mouseleave', () => {
        draggedNode = null;
        hoveredNode = null;
    });
}

// --- CONVERSATION WATCHER INTEGRATION ---
async function loadWatcherData() {
    try {
        logTerminal(`[SYSTEM] Accessing logs analysis reports...`);
        const response = await fetch('../data/watcher_data.json');
        if (!response.ok) throw new Error('Data file missing');
        
        const data = await response.json();
        instagramPosts = data.instagram_posts;
        
        // Populate selector
        postSelect.innerHTML = '';
        instagramPosts.forEach((post, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = post.title.split(':')[0];
            postSelect.appendChild(opt);
        });
        
        logTerminal(`[SYSTEM] Loaded Instagram scripts compiled by Watcher Agent.`, 'success');
        loadInstagramPost();
        
        // Extract and populate GitHub Release milestones
        const milestones = data.summary.milestones || [];
        updateGitHubReleaseNotes(milestones);
        
    } catch (err) {
        logTerminal(`[SYSTEM] Watcher Agent file compiled with fallback templates.`, 'info');
        // Fallback static data
        instagramPosts = [
            {
                "title": "Post 1: The AI Memory Lie Nobody Tells You",
                "hook": "❌ Traditional vector DBs are KILLING your AI agent's speed.",
                "theme": "Educational Hook",
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
                "theme": "Technical Tutorial",
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
        ];
        
        postSelect.innerHTML = '';
        instagramPosts.forEach((post, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = post.title.split(':')[0];
            postSelect.appendChild(opt);
        });
        loadInstagramPost();

        // Default milestones for fallback
        const milestones = [
            "System Core: Created cortex_memory.py containing the dual-system memory engine.",
            "Watcher Agent: Created watcher_agent.py to parse logs and write content.",
            "Visual Interface: Designed high-fidelity canvas graph for memory visualization.",
            "GitHub Sync Hub: Implemented automated github pusher agent and web control widget."
        ];
        updateGitHubReleaseNotes(milestones);
    }
}

function updateGitHubReleaseNotes(milestones) {
    let text = `# 🧠 AURAMEMORY: LAYERLESS NATIVE COGNITIVE MEMORY ENGINE (v1.0.0) 🚀\n\n`;
    text += `Standard RAG architectures rely on slow, complex vector database middleware wrappers. AuraMemory replaces this with a layerless, native cognitive engine executing dual-system memory loops inside agent processes.\n\n`;
    text += `## ⚡ Key Highlights\n`;
    text += `- **System 1 (Working Memory)**: Transient context nodes with automatic reinforcement and decay.\n`;
    text += `- **System 2 (Long-Term Associative Memory)**: Permanent cognitive knowledge consolidation via tag intersection matrices.\n`;
    text += `- **Configurable Guardrails**: Embedded active safety scrubbing (PII filters) and semantic topic blocks.\n`;
    text += `- **Stunning Glassmorphic Visualizer**: High-fidelity HTML5 Canvas with custom spring-physics simulation.\n\n`;
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
    postThemeBadge.textContent = post.theme;
    
    // Caption text assembly
    let captionText = `🔥 INSIGHTS FROM THE BRAIN: ${post.hook}\n\n`;
    post.slides.forEach(s => {
        captionText += `Slide ${s.slide_num}: ${s.headline}\n👉 ${s.body}\n\n`;
    });
    captionText += `💡 CTA: ${post.cta}\n\n`;
    captionText += `${post.hashtags}`;
    
    igCaptionText.value = captionText;
    
    // Setup carousel indicators
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
    const slide = post.slides[activeSlideIndex];
    
    igSlideCount.textContent = `SLIDE ${slide.slide_num}/${post.slides.length}`;
    igSlideHeadline.textContent = slide.headline;
    igSlideBody.textContent = slide.body;
    
    // Update active indicator dot
    const indicators = igIndicators.querySelectorAll('.indicator');
    indicators.forEach((ind, sIdx) => {
        if (sIdx === activeSlideIndex) ind.classList.add('active');
        else ind.classList.remove('active');
    });
}

function nextSlide() {
    const post = instagramPosts[activePostIndex];
    if (activeSlideIndex < post.slides.length - 1) {
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
    logTerminal(`[SYSTEM] Caption copied to clipboard successfully!`, 'success');
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
    logTerminal(`[SYSTEM] CLI Launcher Command copied to clipboard!`, 'success');
}


// --- NATIVE ENGINE SEED & SANDBOX ---
function seedInitialMemories() {
    createNode("I am learning how to build agentic memory modules natively.", ["AI", "AgenticMemory"], "working", 0.8, 1.0);
    createNode("AuraMemory uses a dual-system cognitive architecture.", ["AI", "Architecture"], "working", 0.9, 1.0);
    createNode("Instagram content should have high hooks to attract followers.", ["Marketing", "Instagram"], "working", 0.4, 1.0);
    
    // Re-link
    recalculateLinks();
}

function createNode(content, tags, system, importance, strength) {
    const x = Math.random() * (canvas.width - 150) + 75;
    const y = Math.random() * (canvas.height - 150) + 75;
    
    const node = {
        id: Math.random().toString(36).substring(2, 9),
        content,
        tags,
        system, // "working" or "long_term"
        importance,
        strength,
        accessCount: 1,
        x,
        y,
        vx: 0,
        vy: 0,
        vector: embedNode(tags, content)
    };
    nodes.push(node);
    return node;
}

function recalculateLinks() {
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
}

function findNodeAt(x, y) {
    for (const node of nodes) {
        const d = Math.hypot(node.x - x, node.y - y);
        if (d < physics.nodeRadius) return node;
    }
    return null;
}

// Sandbox Commit
function commitNewMemory() {
    const text = memoryInput.value.trim();
    if (!text) {
        logTerminal(`[SANDBOX] Input cannot be empty!`, 'error');
        return;
    }

    const rawTags = memoryTags.value.split(',').map(t => t.trim()).filter(t => t.length > 0);
    const importance = parseFloat(memoryImportance.value);

    logTerminal(`[PROCESS] Ingesting: "${text.substring(0, 45)}..."`);

    // 1. Guardrail PII Scrubbing
    let processedText = text;
    let piiViolations = [];
    
    if (piiScrubActive) {
        const emailRegex = /[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/gi;
        const keyRegex = /(?:key|token|auth|password|secret)[a-zA-Z0-9_\-\:\=\+\/]{6,32}/gi;
        
        if (emailRegex.test(processedText)) {
            piiViolations.push("EMAIL");
            processedText = processedText.replace(emailRegex, "<EMAIL_SCRUBBED>");
        }
        if (keyRegex.test(processedText)) {
            piiViolations.push("API_KEY");
            processedText = processedText.replace(keyRegex, "<API_KEY_SCRUBBED>");
        }
    }

    if (piiViolations.length > 0) {
        logTerminal(`[GUARDRAIL] PII Scrubbed: ${piiViolations.join(', ')}`, 'warning');
    }

    // 2. Guardrail Blocked Topics
    let blockedViolations = [];
    if (topicBlockActive) {
        blockedTopics.forEach(topic => {
            if (processedText.toLowerCase().includes(topic)) {
                blockedViolations.push(topic);
            }
        });
    }

    if (blockedViolations.length > 0) {
        logTerminal(`[GUARDRAIL] BLOCKED CATEGORY DETECTED: "${blockedViolations.join(', ')}". Entry REJECTED!`, 'error');
        triggerAlertNotification(`GUARDRAIL CRITICAL: Entry rejected because it references "${blockedViolations[0]}".`);
        memoryInput.value = '';
        return;
    }

    // Success - add node
    const node = createNode(processedText, rawTags, "working", importance, 1.0);
    
    // Calculate connections
    let newConnections = 0;
    nodes.forEach(n => {
        if (n.id !== node.id) {
            const sim = cosineSimilarity(node.vector, n.vector);
            if (sim >= 0.20) newConnections++;
        }
    });

    recalculateLinks();
    
    logTerminal(`[SYSTEM-1] Node committed. Vector computed. ID: ${node.id}. system: WORKING. Created ${newConnections} semantic links!`, 'success');
    memoryInput.value = '';
}

function recallMemoryQuery() {
    const rawTags = memoryTags.value.split(',').map(t => t.trim()).filter(t => t.length > 0);
    const queryText = memoryInput.value.trim();
    
    if (rawTags.length === 0 && !queryText) {
        logTerminal(`[SANDBOX] Enter tags or content above to recall matches.`, 'warning');
        return;
    }

    const qWords = [];
    rawTags.forEach(t => qWords.push(...tokenizeText(t)));
    if (queryText) qWords.push(...tokenizeText(queryText));

    logTerminal(`[RECALL] Scanning cognitive space for query tokens...`);
    
    const queryVector = embedWords(qWords);
    let matches = [];
    
    nodes.forEach(node => {
        const sim = cosineSimilarity(queryVector, node.vector);
        if (sim > 0.15) {
            matches.push({ node, sim });
            node.accessCount++;
            node.strength = Math.min(1.0, node.strength + 0.15); // refresh strength
        }
    });

    if (matches.length === 0) {
        logTerminal(`[RECALL] No nodes matches found in cognitive brain.`, 'warning');
    } else {
        matches.sort((a, b) => b.sim - a.sim);
        logTerminal(`[RECALL] Found ${matches.length} matching memory nodes! (Highest CosSim: ${matches[0].sim.toFixed(2)})`, 'success');
        matches.forEach(m => {
            logTerminal(` - Match: "${m.node.content.substring(0, 30)}..." [Similarity: ${m.sim.toFixed(2)}]`, 'info');
        });
    }
}

// Consolidation Cycle
function runConsolidationCycle() {
    logTerminal(`[CONSOLIDATION] Initiating cognitive consolidation worker...`);
    
    let promotedCount = 0;
    let prunedCount = 0;
    let remaining = [];

    nodes.forEach(node => {
        if (node.system === "working") {
            const cognitiveScore = (node.importance * 0.5) + (Math.min(node.accessCount / 4, 1.0) * 0.5);
            
            if (cognitiveScore >= 0.6) {
                // Promote
                node.system = "long_term";
                node.strength = 1.0; // permanent
                promotedCount++;
                logTerminal(`[SYSTEM-2] Node promoted to Long-Term associative network: "${node.content.substring(0, 25)}..."`, 'success');
            } else {
                // Decay
                node.strength = Math.max(0.0, node.strength - decayRate);
                if (node.strength <= 0.0) {
                    prunedCount++;
                    logTerminal(`[PRUNED] Short-term node decayed completely and deleted.`, 'warning');
                } else {
                    remaining.push(node);
                }
            }
        } else {
            remaining.push(node); // long_term is persistent
        }
    });

    nodes = remaining;
    recalculateLinks();

    logTerminal(`[CONSOLIDATION] Cycle finished. Promoted: ${promotedCount}, Decayed & Cleaned: ${prunedCount}.`, 'info');
}

function clearAllMemory() {
    nodes = [];
    links = [];
    logTerminal(`[SYSTEM] Cognitive state cleared. Brain has been reset.`, 'error');
}

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

function triggerAlertNotification(msg) {
    const alertBox = document.getElementById('canvas-alert');
    alertBox.querySelector('.alert-text').textContent = msg;
    alertBox.classList.add('show');
    
    // shake visualizer panel
    const canvasPanel = document.getElementById('panel-canvas');
    canvasPanel.style.borderColor = 'rgba(239, 68, 68, 0.6)';
    canvasPanel.style.transform = 'scale(0.99)';
    
    setTimeout(() => {
        alertBox.classList.remove('show');
        canvasPanel.style.borderColor = '';
        canvasPanel.style.transform = '';
    }, 3000);
}

// --- KEYWORD TAG MANAGEMENT ---
function removeKeyword(kw) {
    blockedTopics = blockedTopics.filter(t => t !== kw);
    renderKeywords();
    logTerminal(`[GUARDRAIL] Restricted keyword removed: "${kw}"`, 'warning');
}

function addKeyword() {
    const kw = newKeywordInput.value.trim().toLowerCase();
    if (kw && !blockedTopics.includes(kw)) {
        blockedTopics.push(kw);
        newKeywordInput.value = '';
        renderKeywords();
        logTerminal(`[GUARDRAIL] Custom restricted keyword registered: "${kw}"`, 'success');
    }
}

function renderKeywords() {
    blockedKeywordsList.innerHTML = '';
    blockedTopics.forEach(kw => {
        const span = document.createElement('span');
        span.className = 'keyword-tag';
        span.innerHTML = `${kw} <button class="close-tag-btn" onclick="removeKeyword('${kw}')">×</button>`;
        blockedKeywordsList.appendChild(span);
    });
}


// --- 2D CANVAS FORCE PHYSICS ENGINE ---
function simulationLoop() {
    updateNodePhysics();
    renderGraph();
    requestAnimationFrame(simulationLoop);
}

function updateNodePhysics() {
    const w = canvas.width;
    const h = canvas.height;

    // Node Repulsion (push away from each other)
    for (let i = 0; i < nodes.length; i++) {
        const n1 = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
            const n2 = nodes[j];
            
            const dx = n2.x - n1.x;
            const dy = n2.y - n1.y;
            const dist = Math.hypot(dx, dy) || 1;
            
            if (dist < 250) {
                // Coulomb force formula simulation
                const force = physics.repulsion / (dist * dist);
                const fx = (dx / dist) * force;
                const fy = (dy / dist) * force;
                
                if (n1 !== draggedNode) {
                    n1.vx -= fx;
                    n1.vy -= fy;
                }
                if (n2 !== draggedNode) {
                    n2.vx += fx;
                    n2.vy += fy;
                }
            }
        }
    }

    // Link Attraction (pull together if related)
    links.forEach(link => {
        const n1 = nodes.find(n => n.id === link.source);
        const n2 = nodes.find(n => n.id === link.target);
        
        if (n1 && n2) {
            const dx = n2.x - n1.x;
            const dy = n2.y - n1.y;
            const dist = Math.hypot(dx, dy) || 1;
            
            // Hooke's Law simulation
            const targetDist = 120;
            const force = (dist - targetDist) * physics.attraction * link.strength;
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;
            
            if (n1 !== draggedNode) {
                n1.vx += fx;
                n1.vy += fy;
            }
            if (n2 !== draggedNode) {
                n2.vx -= fx;
                n2.vy -= fy;
            }
        }
    });

    // Center Gravity pulling nodes back to center
    nodes.forEach(node => {
        if (node === draggedNode) return;
        
        const cx = w / 2;
        const cy = h / 2;
        node.vx += (cx - node.x) * 0.003;
        node.vy += (cy - node.y) * 0.003;

        // Apply velocities & damping
        node.x += node.vx;
        node.y += node.vy;
        node.vx *= physics.damping;
        node.vy *= physics.damping;

        // Contain in boundaries
        const r = physics.nodeRadius;
        node.x = Math.max(r + physics.boundaryPadding, Math.min(w - r - physics.boundaryPadding, node.x));
        node.y = Math.max(r + physics.boundaryPadding, Math.min(h - r - physics.boundaryPadding, node.y));
    });
}

function renderGraph() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Draw Links
    links.forEach(link => {
        const n1 = nodes.find(n => n.id === link.source);
        const n2 = nodes.find(n => n.id === link.target);
        
        if (n1 && n2) {
            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(n2.x, n2.y);
            
            const alpha = 0.06 + (0.2 * link.strength);
            ctx.strokeStyle = `rgba(139, 92, 246, ${alpha})`;
            ctx.lineWidth = 1.5 + (2 * link.strength);
            ctx.stroke();
        }
    });

    // 2. Draw Nodes
    nodes.forEach(node => {
        const isHovered = (node === hoveredNode);
        const isS1 = (node.system === "working");
        
        ctx.save();
        
        // Glow effect
        ctx.shadowBlur = isHovered ? 18 : 8;
        ctx.shadowColor = isS1 ? '#06B6D4' : '#8B5CF6';
        
        // Node Body Fill
        ctx.beginPath();
        ctx.arc(node.x, node.y, physics.nodeRadius, 0, Math.PI * 2);
        
        const grad = ctx.createRadialGradient(node.x, node.y, 2, node.x, node.y, physics.nodeRadius);
        if (isS1) {
            // Working Memory Blue Gradient (applied strength modifies alpha)
            grad.addColorStop(0, `rgba(6, 182, 212, ${0.4 * node.strength})`);
            grad.addColorStop(1, `rgba(13, 148, 136, ${0.85 * node.strength})`);
            ctx.strokeStyle = `rgba(6, 182, 212, ${0.9 * node.strength})`;
        } else {
            // Long Term Purple Gradient
            grad.addColorStop(0, 'rgba(139, 92, 246, 0.45)');
            grad.addColorStop(1, 'rgba(79, 70, 229, 0.95)');
            ctx.strokeStyle = 'rgba(139, 92, 246, 0.95)';
        }
        
        ctx.fillStyle = grad;
        ctx.lineWidth = isHovered ? 3.5 : 2;
        ctx.fill();
        ctx.stroke();
        
        // Draw inside content snippet
        ctx.shadowBlur = 0; // reset shadow for text
        ctx.fillStyle = '#FFF';
        ctx.font = "bold 14px 'Outfit', sans-serif";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        const textSymbol = isS1 ? "S1" : "S2";
        ctx.fillText(textSymbol, node.x, node.y - 2);
        
        // Draw strength rating for System 1 nodes
        if (isS1) {
            ctx.fillStyle = '#22D3EE';
            ctx.font = "8px 'Fira Code', monospace";
            ctx.fillText(`${node.strength.toFixed(2)}`, node.x, node.y + 12);
        } else {
            ctx.fillStyle = '#C084FC';
            ctx.font = "8px 'Fira Code', monospace";
            ctx.fillText("INF", node.x, node.y + 12);
        }

        ctx.restore();
        
        // 3. Hover Node Tooltip Box overlay
        if (isHovered) {
            ctx.save();
            ctx.shadowBlur = 10;
            ctx.shadowColor = 'rgba(0,0,0,0.5)';
            
            const boxW = 200;
            const boxH = 65;
            const bx = Math.max(10, Math.min(canvas.width - boxW - 10, node.x - boxW / 2));
            const by = Math.max(10, node.y - physics.nodeRadius - boxH - 8);
            
            // Drawer Tooltip Panel
            ctx.fillStyle = 'rgba(13, 13, 23, 0.92)';
            ctx.strokeStyle = isS1 ? 'rgba(6, 182, 212, 0.6)' : 'rgba(139, 92, 246, 0.6)';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.roundRect(bx, by, boxW, boxH, 8);
            ctx.fill();
            ctx.stroke();
            
            // Render text
            ctx.fillStyle = '#FFF';
            ctx.font = "10px 'Space Grotesk', sans-serif";
            ctx.textAlign = 'left';
            ctx.textBaseline = 'top';
            
            // Wrap text helper
            const text = node.content;
            let line = '';
            let lineY = by + 8;
            for(let n=0; n<text.length; n++) {
                line += text[n];
                if (line.length > 32 || n === text.length - 1) {
                    ctx.fillText(line + (n < text.length-1 ? '-' : ''), bx + 10, lineY);
                    line = '';
                    lineY += 12;
                    if (lineY > by + boxH - 20) break;
                }
            }
            
            // Draw tags inside tooltip
            ctx.fillStyle = isS1 ? '#67E8F9' : '#D8B4FE';
            ctx.font = "italic 8px 'Space Grotesk', sans-serif";
            ctx.fillText(`Tags: ${node.tags.join(', ')}`, bx + 10, by + boxH - 12);
            
            ctx.restore();
        }
    });
}
