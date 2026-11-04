# Smart Complaint Management Agent

A small hands-on project using Python, LangChain, LangGraph, OpenRouter, and SQLite.

## Project scope

The agent accepts a complaint, identifies its category and priority, looks up relevant guidance in a local JSON knowledge base, optionally creates a ticket, and returns a structured response.

## Starter files

- `data/knowledge_base.json`: sample support guidance used by the solution-search tool.
- `data/sample_complaints.json`: test inputs and illustrative expected labels.
- `schema.sql`: SQLite ticket table definition.
- `app/main.py`: application entry point to implement together.
- `.env.example`: environment-variable template.
- `requirements.txt`: initial Python dependencies.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`.
4. Add your OpenRouter API key and choose a model currently available to your account.

Do not commit `.env` or share your API key.

## Planned implementation order

1. Verify an OpenRouter chat completion.
2. Define structured complaint output with Pydantic.
3. Implement the four Python tools.
4. Build a LangChain tool-calling agent.
5. Orchestrate the flow with LangGraph.
6. Add SQLite ticket creation.
7. Test against `data/sample_complaints.json`.

## Important limitations

This is a learning prototype. The sample knowledge base is illustrative and is not connected to a real support provider. Ticket IDs and ticket records are local to the prototype. The agent must not claim that a real-world issue has been fixed or that a real support team has been contacted.
