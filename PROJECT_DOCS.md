# AUTOGENESIS - Complete Project Documentation

## Project Overview

**Autogenesis** is an autonomous, self-learning AI coding agent that plans, generates, reviews, tests, and deploys complete software projects from natural language descriptions.

---

## Core Capabilities

### 1. Autonomous Code Generation
- Generates multi-file projects (HTML, CSS, JS, Python, etc.)
- Language-aware prompting ensures correct syntax per file type
- Cleans markdown artifacts from AI output

### 2. Self-Improvement System
- XP-based leveling (0-100%)
- Growth stages: Baby → Child → Teen → Adult → Expert → Sage
- Learns from each project generated
- Tracks languages learned, files created, projects completed

### 3. Auto Unit Test Generation
- Creates pytest/Jest tests for generated code
- Tests all functions with edge cases
- Saves as `test_*.py` or `*.test.js`

### 4. Auto CI/CD Pipeline
- Generates `.github/workflows/main.yml`
- Runs on push/PR
- Installs dependencies, runs tests, builds, deploys

### 5. Auto Dockerfile
- Production-ready container configuration
- Proper base image selection
- Dependency installation

### 6. Code Review Loop
- AI reviews generated code
- Identifies issues
- Auto-fixes problems iteratively

### 7. Live Preview
- Real-time HTML/CSS/JS preview in iframe
- Browser chrome UI (red/yellow/green dots)
- Toggle show/hide

### 8. Voice Input
- Web Speech API integration
- Speak project descriptions
- Chrome/Edge browser support

---

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Runtime |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Groq API (llama-3.3-70b) | Primary AI provider |
| Gemini API | Fallback AI provider |
| Server-Sent Events (SSE) | Real-time streaming |

### Frontend
| Technology | Purpose |
|------------|---------|
| Next.js 16 | React framework |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| Web Speech API | Voice input |

### DevOps
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| GitHub Actions | CI/CD |
| Vercel | Deployment |

---

## Sponsor Integrations (5/5 Required)

### 1. Cline CLI ✅
**File:** `cli/autogenesis.py`

Complete command-line interface for autonomous coding:
```bash
autogenesis generate "Build a REST API"  # Generate project
autogenesis fix main.py --error "Error"  # Auto-fix bugs
autogenesis test main.py                 # Generate tests
autogenesis stats                        # View AI stats
```

**Features:**
- Full project generation from CLI
- Auto-fix code based on error messages
- Test generation for any file
- AI learning statistics display

---

### 2. Kestra AI Agent ✅
**File:** `kestra/flows/summarize_memory.yaml`

AI agent that summarizes data and makes decisions:

**Task 1: Data Summarization**
- Reads project memory (JSON)
- Counts total projects, files
- Tracks language diversity
- Calculates average XP per project

**Task 2: AI Decision Making**
- Recommends diversifying languages if < 3 used
- Suggests complex projects if XP rate low
- Unlocks "advanced mode" at 10+ projects

**Triggers:**
- Daily schedule (9 AM)
- Webhook on milestones

---

### 3. Oumi RL Fine-Tuning ✅
**File:** `backend/oumi_rl.py`

Reinforcement Learning integration:

**Feedback Collection:**
```python
collect_feedback(code, rating, idea)  # 1-5 star rating
```

**Preference Pair Generation:**
- Creates (prompt, chosen, rejected) triplets
- Positive examples: rating >= 4
- Negative examples: rating < 4

**Training:**
- Uses Direct Preference Optimization (DPO)
- Model: Llama-2-7b-hf (configurable)
- Saves checkpoints for continuous improvement

---

### 4. Vercel Deployment ✅
**File:** `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {"src": "backend/api.py", "use": "@vercel/python"},
    {"src": "frontend/package.json", "use": "@vercel/next"}
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "backend/api.py"},
    {"src": "/(.*)", "dest": "frontend/$1"}
  ]
}
```

---

### 5. CodeRabbit ✅
**File:** `.coderabbit.yaml`

Full PR review configuration:
- Auto-review all PRs (including drafts)
- Assertive review profile
- Security vulnerability detection
- Code quality suggestions
- Documentation checks
- Enabled linters: shellcheck, ruff, markdownlint

---

## Architecture

```
autogenesis/
├── backend/
│   ├── agent/
│   │   ├── agent.py          # Groq/Gemini API wrapper
│   │   ├── planner.py        # Project planning
│   │   ├── coder.py          # Code generation
│   │   ├── reviewer.py       # Code review
│   │   ├── memory.py         # Project memory
│   │   ├── intelligence.py   # XP/leveling system
│   │   ├── capabilities.py   # Tests, CI/CD, Dockerfile
│   │   └── orchestrator.py   # Main pipeline
│   ├── api.py                # FastAPI endpoints
│   └── oumi_rl.py            # Oumi integration
├── frontend/
│   └── src/app/page.tsx      # Main UI
├── cli/
│   └── autogenesis.py        # Cline CLI
├── kestra/
│   └── flows/summarize_memory.yaml
├── .coderabbit.yaml
├── vercel.json
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/run-stream` | POST | Generate project (SSE streaming) |
| `/run` | POST | Generate project (non-streaming) |
| `/intelligence` | GET | Get AI stats |
| `/export` | GET | Download project ZIP |
| `/ping` | GET | Server ping |

---

## Key Differentiators

1. **Truly Autonomous** - Plans, codes, tests, deploys without human intervention
2. **Self-Learning** - Gets smarter with each project
3. **Multi-File** - Generates complete project structures
4. **Production-Ready Output** - Includes tests, CI/CD, Docker
5. **Real-Time** - SSE streaming shows progress live
6. **Voice Control** - Speak your project idea
7. **All 5 Sponsors** - Complete integration

---

## Metrics

| Metric | Value |
|--------|-------|
| Backend files | 15+ |
| Frontend components | 1 (single page app) |
| API endpoints | 6 |
| AI capabilities | 8 |
| Sponsor integrations | 5/5 |
| Lines of code | ~2000+ |

---

## Demo Flow

1. User speaks or types project idea
2. AI plans project structure
3. Generates source files (language-aware)
4. Generates unit tests
5. Creates CI/CD pipeline
6. Creates Dockerfile
7. Reviews code for issues
8. Updates XP and level
9. Shows live preview (web projects)
10. User downloads ZIP with everything

---

## Hackathon Alignment

| Requirement | Implementation |
|-------------|----------------|
| Autonomous AI agent | ✅ Full pipeline automation |
| Complete automation tools | ✅ Tests, CI/CD, Docker |
| Cline CLI | ✅ 4 commands |
| Kestra summarization + decisions | ✅ Both tasks |
| Oumi RL fine-tuning | ✅ Feedback + training |
| Vercel deployment | ✅ Config ready |
| CodeRabbit PR reviews | ✅ Full config |

---

## Unique Selling Points

1. **AI Growth System** - Gamified learning that's visible to users
2. **Complete Output** - Not just code, but tests + CI/CD + Docker
3. **Live Preview** - See web projects render in real-time
4. **Memory-Based Learning** - Uses past projects to inform new ones
5. **CLI + Web** - Both interfaces for different use cases
6. **Decision-Making AI** - Kestra agent makes recommendations

---

*Built for Hackathon 2024*
