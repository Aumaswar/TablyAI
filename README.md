# Tably AI

> Ask your SQL database questions in plain English. It writes the query, runs it, hands you the results.

**[→ View Full Project Page](https://aumaswar.github.io/tablyai/readme.html)**

---

Built with Angular, FastAPI, and a locally hosted LLM via LM Studio. No cloud. No data leaving your machine.

**Stack:** `Angular 21` · `FastAPI` · `LM Studio` · `SQL Server` · `JWT Auth`

---

### Quick Start

```bash
# Backend
cd ai-backend
pip install -r requirements.txt
uvicorn main_langchain:app --reload

# Frontend
cd ai-frontend
npm install
ng serve
```

Then open `http://localhost:4200`

---

### Ports

| Port | Service |
|------|---------|
| 4200 | Angular frontend |
| 8000 | FastAPI backend |
| 1234 | LM Studio local API |
| 1433 | SQL Server |

---

*Full setup guide, screenshots, and API reference on the **[project page](https://aumaswar.github.io/tablyai/readme.html)**.*
