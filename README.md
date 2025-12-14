# Autogenesis

**Self-learning AI agent that plans, codes, tests, and deploys — autonomously.**

## Quick Start

```bash
# Backend
cd backend && pip install -r requirements.txt
python -m uvicorn api:app --reload

# Frontend
cd frontend && npm install && npm run dev

# CLI (Cline)
python cli/autogenesis.py generate "Build a calculator"
```

## Features

| Feature | Description |
|---------|-------------|
| Multi-file Generation | Creates complete projects with proper structure |
| Auto Unit Tests | Generates test files for your code |
| Auto CI/CD | Creates GitHub Actions workflows |
| Auto Dockerfile | Production-ready Docker configs |
| Live Preview | Real-time HTML/CSS/JS preview |
| Voice Input | Speak your project idea |
| Learning System | AI gains XP and levels up |

---

## Sponsor Integrations

### 1. Cline CLI

```bash
# Generate a project
python cli/autogenesis.py generate "REST API with auth"

# Auto-fix bugs
python cli/autogenesis.py fix main.py --error "TypeError"

# Generate tests
python cli/autogenesis.py test main.py

# View AI stats
python cli/autogenesis.py stats
```

### 2. Kestra AI Agent

Located at `kestra/flows/summarize_memory.yaml`:

- Summarizes all generated projects
- Analyzes language diversity
- Makes decisions based on data
- Triggers daily or on milestones

```bash
# Run with Kestra
kestra flow execute company.autogenesis autogenesis-ai-summarizer
```

### 3. Oumi RL Fine-Tuning

Located at `backend/oumi_rl.py`:

```bash
# Collect feedback
python oumi_rl.py feedback "def hello(): pass" 5 "hello world"

# Train with feedback
python oumi_rl.py train

# View RL stats
python oumi_rl.py stats
```

### 4. Vercel Deployment

Configured in `vercel.json`:

```bash
vercel --prod
```

### 5. CodeRabbit

Configured in `.coderabbit.yaml`:

- Auto-reviews all PRs
- Security vulnerability detection
- Code quality suggestions
- Documentation checks

---

## Project Structure

```
autogenesis/
├── backend/           # FastAPI server
│   ├── agent/         # AI modules
│   ├── api.py         # REST endpoints
│   └── oumi_rl.py     # Oumi integration
├── frontend/          # Next.js UI
├── cli/               # Cline CLI
├── kestra/            # Kestra flows
├── vercel.json        # Vercel config
└── .coderabbit.yaml   # CodeRabbit config
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/run-stream` | POST | Generate project (SSE) |
| `/intelligence` | GET | Get AI stats |
| `/export` | GET | Download ZIP |

---
