import os


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


TOOL_MAP = {
    "read_file": read_file,
    "list_directory": list_directory,
}


def execute_tool(name, args):
    tool = TOOL_MAP.get(name)
    if not tool:
        return f"Error: Unknown tool '{name}'"
    return tool(**args)
