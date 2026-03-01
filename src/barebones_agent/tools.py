import os
import io
import contextlib
import traceback

from barebones_agent.rag import rag_search


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error reading file: {e}"


def list_directory(path):
    try:
        entries = os.listdir(path)
        return "\n".join(entries) if entries else "Directory is empty."
    except FileNotFoundError:
        return f"Error: Directory not found: {path}"
    except Exception as e:
        return f"Error listing directory: {e}"


def run_python(code):
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, {})
        return buffer.getvalue() or "Code executed successfully."
    except Exception:
        return traceback.format_exc()


TOOL_MAP = {
    "read_file": read_file,
    "list_directory": list_directory,
    "run_python": run_python,
    "rag_search": rag_search,
}


def execute_tool(name, args):
    tool = TOOL_MAP.get(name)
    if not tool:
        return f"Error: Unknown tool '{name}'"
    return tool(**args)
