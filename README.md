# Smart Complaint Management Agent

An AI-assisted complaint triage prototype built with LangGraph, LangChain, and OpenRouter. The agent classifies an incoming customer complaint, routes it based on priority, retrieves troubleshooting guidance for routine cases, and generates a customer-facing response.

## Overview

Each complaint passes through a four-stage workflow:

1. **Classification:** An LLM returns a structured analysis containing a category, a priority, and a reason, validated with Pydantic.
2. **Routing:** High-priority complaints are escalated for human review. All other complaints go to solution search.
3. **Solution search:** A tool queries a local JSON knowledge base for troubleshooting guidance matching the complaint category.
4. **Response generation:** An LLM drafts a customer response that reflects the classification, retrieved solutions, and escalation status.

## Architecture

```
complaint
   │
   ▼
classify ──► priority_router ──┬── high ────────► escalate ──┐
                               │                             ▼
                               └── low / medium ► search ──► respond ──► final response
```

| Component | Location | Responsibility |
|---|---|---|
| Workflow graph | `app/graph.py` | Defines the LangGraph nodes, routing, and LLM calls |
| Shared state | `app/state.py` | `ComplaintState` typed dictionary passed between nodes |
| Output schema | `app/schemas.py` | `ComplaintAnalysis` Pydantic model for structured classification |
| Search tool | `app/tools.py` | `search_solutions` LangChain tool over the knowledge base |
| Entry point | `app/main.py` | Runs sample complaints and prints the results |
| Knowledge base | `data/knowledge_base.json` | Illustrative troubleshooting guidance by category |
| Sample inputs | `data/sample_complaints.json` | Test complaints with illustrative expected labels |
| Ticket schema | `schema.sql` | SQLite table definition for complaint tickets (not yet wired into the workflow) |

### Categories and priorities

- **Categories:** `technical_support`, `payment`, `account_access`, `service_request`, `general_inquiry`
- **Priorities:** `low`, `medium`, `high`

Suspected unauthorized account access, security incidents, duplicate charges, and urgent time-sensitive failures are classified as high priority.

## Prerequisites

- Python 3.10 or later
- An [OpenRouter](https://openrouter.ai/) API key

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create your environment file from the template:

   ```bash
   cp .env.example .env
   ```

4. Set the following values in `.env`:

   | Variable | Description |
   |---|---|
   | `OPENROUTER_API_KEY` | Your OpenRouter API key |
   | `OPENROUTER_MODEL` | A chat model available to your OpenRouter account |

## Usage

Run the application from the project root so that the `app` package resolves correctly:

```bash
python -m app.main
```

The entry point processes three built-in sample complaints and prints the classification, routing decision, retrieved solutions, and final customer response for each.

## Project structure

```
.
├── app/
│   ├── __init__.py
│   ├── graph.py        # LangGraph workflow and LLM nodes
│   ├── main.py         # Application entry point
│   ├── schemas.py      # Pydantic output models
│   ├── state.py        # Graph state definition
│   └── tools.py        # Knowledge base search tool
├── data/
│   ├── knowledge_base.json
│   └── sample_complaints.json
├── .env.example
├── requirements.txt
└── schema.sql
```

## Security

- Do not commit `.env` or share your OpenRouter API key. `.env` is listed in `.gitignore`.
- Rotate any key that has been committed to version control, even if it was later removed.

## Limitations

This is a prototype intended for learning and experimentation.

- The knowledge base is illustrative and is not connected to a real support system.
- Escalation only flags a complaint for review. No real support team is notified.
- Ticket IDs and records are not yet persisted. `schema.sql` defines the planned SQLite table, but the workflow does not write to it.
- Generated responses must not claim that an issue has been resolved or that a support team has been contacted. The prompts enforce this, but generated text should still be reviewed before use.
