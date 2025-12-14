# Autogenesis 🧬

**The Self-Evolving AI Developer**

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-green.svg)]()
[![AI: Groq](https://img.shields.io/badge/AI-Groq%20LPU-orange.svg)]()
[![AI: Gemini](https://img.shields.io/badge/AI-Gemini%202.0-blue.svg)]()

> *Typical coding assistants reset every session. Autogenesis remembers, learns, and grows with you.*

---

![Autogenesis Dashboard](assets/dashboard.png)

## 🔮 What is Autogenesis?

Autogenesis is an autonomous software engineer that lives in your browser. It doesn't just autocomplete code; it **plans, architects, builds, tests, and deploys** full-stack applications from a single prompt.

But the real magic is in its **growth mechanics**:
*   **Memory**: It remembers every project you've built.
*   **XP System**: Every feature you implement earns XP.
*   **Skill Tree**: As it levels up, it unlocks new capabilities (e.g., Python Lv1 -> Python Lv5).
*   **RLHF Training**: Rate its code (1-5 stars) to train a custom model adapter via **Oumi**.

---

## ✨ Features at a Glance

| Feature | Description | Tech Provider |
| :--- | :--- | :--- |
| **⚡ Instant Builds** | Generates full-stack apps in seconds using LPUs. | **Groq** |
| **🧠 Deep Logic** | Handles complex architecture & reasoning. | **Gemini 2.0** |
| **💾 Long-Term Memory** | Tracks project history & evolution. | **Kestra** |
| **🎯 Self-Correction** | Auto-fixes bugs & dependency errors. | **CodeRabbit** |
| **🚀 Instant Deploy** | One-click public hosting. | **Vercel** |
| **🎓 Adaptive Learning** | Learns from your feedback ratings. | **Oumi** |

---

## 📸 Visual Tour

### Live Preview & Editing
*Watch code turn into reality instantly with full-screen previews.*
![Glassmorphism Calculator](assets/demo_preview.png)

### The AI Skill Tree
*Watch your agent evolve from "Baby" to "Sage" as you build more app.*
![Skill Tree](assets/skill_tree.png)

### Production-Ready Code
*Clean, well-structured code with automated error checking.*
![Code Editor](assets/code_view.png)

---

## 🚀 Quick Start

### 1. Requirements
*   Node.js 18+
*   Python 3.9+

### 2. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your GROQ_API_KEY
python -m uvicorn api:app --reload
```

### 3. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` and start building!

---

## 🛠️ Architecture

Autogenesis uses a multi-agent system to simulate a real dev team:

1.  **The Architect** (Gemini): Plans the project structure.
2.  **The Coder** (Groq): Writes high-speed code logic.
3.  **The Reviewer** (CodeRabbit): Checks for bugs and security.
4.  **The DevOps** (Vercel): Handles deployment pipelines.

---

## 🤝 Community

Built for the **2025 AI Hackathon**.

*   **Groq** for speed.
*   **Gemini** for intelligence.
*   **Kestra** for orchestration.
*   **Oumi** for training.

---

*(c) 2025 Autogenesis Team. Open Source.*
