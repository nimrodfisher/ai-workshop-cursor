## AI Workshop (Cursor)  Supabase Postgres + GitHub MCP

This project is a minimal scaffold for running AI-powered analysis for data teams:

- **Supabase Postgres**: connect directly to your Supabase-hosted Postgres database.
- **GitHub MCP (external)**: intended to be used from an MCP-capable client (e.g. Cursor / Claude Desktop) to provide repository context for query building and documentation lookup.

This repo does **not** expose a UI  it is meant to be used from scripts, notebooks, or an AI coding environment (like Cursor).

### 1. Setup

1. Create and activate a virtual environment (optional but recommended):

`ash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
`

2. Install dependencies:

`ash
pip install -r requirements.txt
`

3. Create your .env file from the template:

`ash
cp .env.example .env
`

4. Edit .env and fill in your real Supabase Postgres credentials.

### 2. Testing the database connection

After configuring .env, run:

`ash
python db.py
`

You should see a message indicating the current database time if the connection is successful.

### 3. Next steps

- Add analysis scripts (for example, nalysis/ with question-driven SQL queries).
- Wire this project into your MCP-capable editor (Cursor / Claude) so the AI can:
  - Read this repository for context.
  - Use a GitHub MCP server (configured in your editor) to pull repo context from GitHub.
- Extend db.py with helper functions for frequently used queries.
