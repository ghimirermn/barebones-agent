# Barebones Agent

A minimal AI agent with 2 tools, built for learning.

Uses the [ReAct](https://arxiv.org/abs/2210.03629) pattern — the agent thinks before it acts:

```
(thought) → (action) → (observation) → ... → final answer
```

## Tools

- `read_file(path)` — reads a file
- `list_directory(path)` — lists a directory

## Setup

1. Get a free key from [console.groq.com](https://console.groq.com)
2. Add to `.env`:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. Install and run:
   ```
   uv add groq python-dotenv
   uv run python agent.py
   ```

## Example

```
You: list files in this folder and tell me what the readme says

  (thought) To list the files and read the readme, I first need to
  list the files in the folder to confirm the readme exists.

  (action) list_directory({'path': '.'})
  (observation) .env, .git, .venv, agent.py, prompt.py, pyproject.toml,
  README.md, requirements.txt, tools.py, uv.lock, __pycache__

  (action) read_file({'path': 'README.md'})
  (observation) # Barebones Agent ...

Agent: The README describes a minimal AI agent with 2 tools, built for
learning. It outlines the agent's loop, tools, setup, and provides an
example of how the agent works.
```
