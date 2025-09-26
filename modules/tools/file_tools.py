# modules/tools/file_tools.py
import os
import glob
from pathlib import Path

def _inside_sandbox(p: Path) -> bool:
    try:
        p.resolve().relative_to(SANDBOX_ROOT.resolve())
        return True
    except Exception:
        return False

def norm(path: str) -> Path:
    p = (SANDBOX_ROOT / path).resolve() if not os.path.isabs(path) else Path(path).resolve()
    if not _inside_sandbox(p):
        raise PermissionError(f"Path outside sandbox: {p}")
    return p

def list_dir(path=".", show_hidden=False):
    """List directory contents"""
    try:
        items = []
        for item in os.listdir(path):
            if not show_hidden and item.startswith('.'):
                continue
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                items.append(f"📁 {item}/")
            else:
                items.append(f"📄 {item}")
        return items
    except Exception as e:
        return [f"Error: {str(e)}"]

def read_text(path):
    """Read text file contents"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_text(path, content):
    """Write text to file"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File written: {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def ensure_dirs(path):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory created: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

def find_files(root=".", query=""):
    """Find files matching query"""
    try:
        matches = []
        for file_path in glob.glob(f"{root}/**/*{query}*", recursive=True):
            if os.path.isfile(file_path):
                matches.append(file_path)
        return matches[:20]  # Limit results
    except Exception as e:
        return [f"Error: {str(e)}"]