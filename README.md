<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=3B82F6&center=true&vCenter=true&width=600&lines=Tably+AI;Ask+your+data+anything." alt="Tably AI" />

<br/>

**Ask your SQL database questions in plain English.**
It writes the query, runs it, hands you the results — all locally, no cloud.

<br/>

[![Live Demo](https://img.shields.io/badge/Project%20Page-Live%20→-3b82f6?style=for-the-badge&logoColor=white)](https://aumaswar.github.io/TablyAI/readme.html)
&nbsp;
![Angular](https://img.shields.io/badge/Angular-21-dd0031?style=for-the-badge&logo=angular&logoColor=white)
&nbsp;
![FastAPI](https://img.shields.io/badge/FastAPI-0.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=for-the-badge&logo=python&logoColor=white)

<br/>

</div>

---

## What it does

You type *"Show me the top 10 customers by revenue"* — Tably AI reads your live schema, writes the SQL, executes it safely, and gives you back a clean table you can export to Excel. Everything runs on your machine. No API keys. No data leaving your network.

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | Angular 21 |
| Backend | FastAPI + Uvicorn |
| Database | SQL Server 2019/2022 via pyodbc |
| AI | LM Studio · Qwen2.5-Coder-7B (local) |
| Auth | JWT + bcrypt |
| Export | xlsx |

---

## Quick Start

```bash
# 1 — Backend
cd ai-backend
pip install -r requirements.txt
uvicorn main_langchain:app --reload

# 2 — Frontend
cd ai-frontend
npm install
ng serve
```

> Make sure LM Studio is running with a model loaded on `http://127.0.0.1:1234/v1` before starting the backend.

Open `http://localhost:4200` and you're in.

---

## Ports

| Port | Service |
|------|---------|
| `4200` | Angular frontend |
| `8000` | FastAPI backend |
| `1234` | LM Studio local API |
| `1433` | SQL Server |

---

## Security

- JWT authentication on every endpoint
- Role-based access control (admin / viewer)
- Read-only enforcement — only `SELECT` gets through
- DDL/DML fully blocked — no `INSERT`, `UPDATE`, `DROP`, `ALTER`

---

<div align="center">

**[→ Full project page — setup guide, screenshots, API reference](https://aumaswar.github.io/TablyAI/readme.html)**

<br/>

*Built for people who have data but not time to write SQL.*

</div>
