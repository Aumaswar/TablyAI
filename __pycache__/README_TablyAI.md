# TablyAI

<div align="center">

# TablyAI
### Chat with Your Database Using AI

Convert natural language into SQL queries and get instant database insights through an intuitive chat interface.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Angular](https://img.shields.io/badge/Angular-20-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![LangChain](https://img.shields.io/badge/LangChain-AI-purple)

</div>

---

## Overview

TablyAI is an AI-powered database assistant that allows users to interact with databases using plain English.

Instead of writing complex SQL queries manually, users can ask questions such as:

```text
Show all customers from Gujarat
List top 10 products by sales
How many orders were placed this month?
Show employee names and departments
```

TablyAI automatically:

1. Connects to the selected database
2. Extracts schema information
3. Understands user intent
4. Generates SQL queries
5. Executes queries safely
6. Returns formatted results

---

## Screenshots

```md
![Dashboard](screenshots/dashboard.png)
![Database Connection](screenshots/database-connection.png)
![Chat Interface](screenshots/chat-interface.png)
![Results](screenshots/results.png)
```

---

## Key Features

### Natural Language Queries
Ask questions in plain English and receive database results instantly.

### Intelligent Schema Understanding
Automatically understands tables, columns, relationships, foreign keys, and data types.

### Dynamic Metadata Retrieval
View available databases, tables, and columns before generating queries.

### AI Powered SQL Generation
Uses LangChain and Groq LLMs to generate context-aware SQL queries.

### Query Validation
Checks generated SQL before execution to reduce invalid queries.

### Result Visualization
Displays query outputs in a structured tabular format.

---

## Architecture

```text
┌───────────────────┐
│ Angular Frontend  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ FastAPI Backend   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Metadata Engine   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ LangChain Layer   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Groq LLM          │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ SQL Generator     │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ MySQL Database    │
└───────────────────┘
```

---

## How It Works

1. User connects a database.
2. Backend retrieves metadata.
3. Metadata is provided to LangChain.
4. User submits a natural language query.
5. Groq generates SQL based on schema and intent.
6. SQL is validated and executed.
7. Results are returned to the frontend.

---

## Tech Stack

### Frontend
- Angular 20
- TypeScript
- HTML
- CSS

### Backend
- FastAPI
- Python

### AI Layer
- LangChain
- Groq

### Database
- MySQL

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Aumaswar/TablyAI.git
cd TablyAI
```

### Backend Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_key_here
```

### Run Backend

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd ai-frontend
npm install
ng serve
```

---

## Security

- Environment variable protection
- SQL validation before execution
- No hardcoded secrets
- Metadata-driven query generation

---

## Future Enhancements

- PostgreSQL support
- Oracle support
- Query explanation engine
- Query optimization suggestions
- Dashboard analytics
- Export to Excel
- Multi-database support

---

## Author

Noah Aswar

Built using Angular, FastAPI, LangChain, Groq, and MySQL.

---

## License

MIT License
