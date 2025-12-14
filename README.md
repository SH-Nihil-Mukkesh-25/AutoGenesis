# Autogenesis 🧬

**The AI Developer That Grows with You.**

Autogenesis is an autonomous coding agent that plans, writes, tests, and deploys full-stack applications. Unlike standard code assistants, it has **long-term memory**, an **evolving skill tree**, and **reinforcement learning** mechanics that improve its performance over time.

![Autogenesis Dashboard](assets/dashboard.png)

---

## 🚀 Key Features

*   **⚡ Instant Code Generation**: Powered by **Groq Llama 3**, generating full-stack apps in seconds.
*   **🧠 Deep Reasoning**: **Google Gemini 2.0** fallback for complex logical architecture.
*   **🌳 Growing Skill Tree**: The more you build, the smarter it gets. Unlocks new languages and patterns.
*   **💾 Long-Term Memory**: Remembers past projects and code styles using **Kestra**.
*   **🚀 One-Click Deployment**: Deploys instantly to **Vercel** with a public URL.
*   **🎓 Self-Improvement**: Uses **Oumi RLHF** to fine-tune based on your ratings.

### Visual Demo

| **Live Preview** | **Skill Tree Growth** |
| :---: | :---: |
| ![Glassmorphism Calculator](assets/demo_preview.png) | ![Skill Tree](assets/skill_tree.png) |

*Full code view and terminal:*
![Code Editor](assets/code_view.png)

---

---

## 🛠️ Tech Stack & Architecture

Autogenesis is built on a modern, scalable stack:

*   **Frontend**: Next.js 14, TypeScript, Tailwind CSS (Glassmorphism UI)
*   **Backend**: Python FastAPI, Dockerized
*   **AI Engines**: Groq (Llama 3.3), Google Gemini 2.0 Flash
*   **Orchestration**: Kestra (Memory/Workflows)
*   **Training**: Oumi (RLHF/DPO)
*   **CI/CD**: Vercel & Render
*   **Code Review**: CodeRabbit & Cline

---

## 📦 Installation

### Prerequisites
*   Node.js 18+
*   Python 3.9+
*   Docker (optional, for containerized backend)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/autogenesis.git
cd autogenesis
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your keys
cp .env.example .env
# Edit .env and add GROQ_API_KEY / GEMINI_API_KEY
```

Run the server:
```bash
python -m uvicorn api:app --reload
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to start building!

---

## 🤖 Using the Agent

1.  **Describe your idea**: "Build a personal portfolio with a dark theme."
2.  **Wait for Planning**: The agent breaks it down into files (HTML, CSS, JS).
3.  **Live Preview**: Watch the code appear and run instantly in the browser.
4.  **Deploy**: Click "Deploy to Vercel" to go live.
5.  **Rate & Improve**: Rate the code to train the **Oumi** model for next time.

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

**Sponsors & Tools Used:**
*   [Groq](https://groq.com)
*   [Google Gemini](https://deepmind.google/technologies/gemini/)
*   [Kestra](https://kestra.io)
*   [Oumi](https://oumi.ai)
*   [CodeRabbit](https://coderabbit.ai)
*   [Vercel](https://vercel.com)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
