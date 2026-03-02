# Barebones Agent

A minimal AI agent with 4 tools, built for learning.

Uses the [ReAct](https://arxiv.org/abs/2210.03629) pattern — the agent thinks before it acts:

```
(thought) → (action) → (observation) → ... → final answer
```

📝 **[Read the blog post](https://ghimirermn.github.io/llm-agent)** for a detailed explanation of how this agent works.

## Tools

- `read_file(path)` — reads a file
- `list_directory(path)` — lists a directory
- `run_python(code)` — executes a Python code snippet
- `rag_search(query, path)` — searches documents for content relevant to a query (TF-IDF)

## Project Structure

```
src/barebones_agent/
├── __init__.py
├── agent.py    — main loop (LLM ↔ tools)
├── prompt.py   — system prompt
├── rag.py      — RAG search (TF-IDF)
└── tools.py    — tool implementations
```

## Setup

1. Get a free key from [console.groq.com](https://console.groq.com)
2. Add to `.env`:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. Install and run:
   ```
   uv sync
   uv pip install -e .
   uv run barebones-agent
   ```

## Example

```
You: list files in this folder and tell me what the readme says

  (thought) To list the files and read the readme, I first need to
  list the files in the folder to confirm the readme exists.

  (action) list_directory({'path': '.'})
  (observation) .env, .git, .venv, pyproject.toml,
  README.md, src, uv.lock

  (action) read_file({'path': 'README.md'})
  (observation) # Barebones Agent ...

Agent: The README describes a minimal AI agent with 4 tools, built for
learning. It outlines the agent's loop, tools, setup, and provides an
example of how the agent works.
```

## Note

There can be edge cases, error handling and retries are intentionally left out to keep things simple. This repo is only for learning purposes.
