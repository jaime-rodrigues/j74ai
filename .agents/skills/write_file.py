import os

metadata = {
    "name": "write_file",
    "description": "Writes content to a specified file path within the repository.",
    "args": {
        "path": "The relative path to the file to write (e.g., src/main.py)",
        "content": "The content to write to the file"
    }
}

def execute(path: str, content: str, **kwargs):
    # Assume repository root is at ./target_repo relative to the agent's execution
    repo_root = kwargs.get("repo_root", "./target_repo")
    full_path = os.path.join(repo_root, path)

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return {"status": "success", "message": f"File written to {full_path}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to write file {full_path}: {e}"}
