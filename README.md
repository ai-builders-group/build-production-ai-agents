# Build a Production-Ready AI Agent

**A professional, project-based curriculum to build, harden, and deploy an AI Codebase Analyst using LangGraph, Pydantic, and Docker.**

---

## 🚀 About This Project
This repository is the official "Open Source Lab" for the book **[Production-Ready AI Agents](https://www.amazon.com/dp/B0G43PPDSP)**.

Most AI tutorials stop at a Jupyter Notebook. This project starts there, but quickly moves into production engineering. You will build **The AI Codebase Analyst**: an autonomous agent that ingests a local code repository, understands the file structure, and answers complex queries about the code via an interactive UI.

### The "Lab" vs. The "Textbook"
*   **This Repository (The How):** Provides the code, the patterns, and the step-by-step implementation guide.
*   **The Book (The Why):** Covers the architectural theory, state machine design patterns, and the deep engineering decisions behind building scalable agents. [Get the book here](https://www.amazon.com/dp/B0G43PPDSP).

---

## 🛠️ The Tech Stack
We define "Production-Ready" as **Stateful, Reliable, and Observable.**

*   **🧠 Logic:** [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful orchestration)
*   **🛡️ Reliability:** [Pydantic](https://docs.pydantic.dev/) (Structured output & validation)
*   **💾 Memory:** FAISS & Vector Stores (RAG)
*   **🖥️ Interface:** [Chainlit](https://docs.chainlit.io/get-started/overview) (Interactive UI)
*   **🚀 Deployment:** Docker & Google Cloud Run

---

## 📚 The Curriculum

The course is divided into 4 sprints. You can find the detailed instructions for each lesson in the `/curriculum` folder.

**Module 1: The Core Engine**
*   **Lesson 1:** Professional Workspace Setup & Observability
*   **Lesson 2:** The Agent as a State Machine (LangGraph)
*   **Lesson 3:** Binding Tools & Reasoning

**Module 2: The Knowledge Base (RAG)**
*   **Lesson 4:** Ingestion Pipeline (Load, Split, Embed, Store)
*   **Lesson 5:** The Retrieval Tool (Connecting the Brain to the Memory)

**Module 3: Production Pillars**
*   **Lesson 6:** Structured Output (Enforcing Pydantic Schemas)
*   **Lesson 7:** Security & Guardrails (Preventing Injection)
*   **Lesson 8:** Resilience (Retries, Fallbacks, and Error Handling)

**Module 4: Shipping It**
*   **Lesson 9:** The Interactive UI (Chainlit Integration)
*   **Lesson 10:** Containerization (Docker & CI/CD)

---

## 👨‍💻 How to Use This Repository

This repo uses **Git Tags** to manage the curriculum. You can code along from scratch, or jump to the solution for any specific lesson.

### 1. Start Here
Clone the repo. You will land on the `starter` branch. This contains the boilerplate infrastructure but no solution code.

```
git clone https://github.com/ai-builders-group/build-production-ai-agents.git
cd build-production-ai-agents
```

Open the file `curriculum/START_HERE_Welcome.pdf` to begin.


### 2. Stuck? Check the Solution
We have created immutable tags for the completion of every lesson. If you are stuck on Lesson 3, you can peek at the solution code.

**To view the solution for a specific lesson:**
```git checkout lesson-3-complete```

**To return to your workspace:**
```git checkout starter```

### 3. The Final Build
To see the finished, 100% production-ready application:
```git checkout main```

---

## 💬 Community & Support

You are not building alone.

*   **Need Help?** Join the `#course-help` channel in our Discord.
*   **Found a bug?** Open a GitHub Issue.
*   **Discussion:** Share your build and get feedback.

👉 **[Join the AI Builders HQ Discord]([YOUR_DISCORD_LINK_HERE](https://hq.aibuildersgroup.ai/))**

---

## License
This project is open-source (MIT). Feel free to fork it, break it, and rebuild it.

**Built by [AI Builders Group](https://aibuildersgroup.ai)**  
*Architecting the future of AI Agents.*
