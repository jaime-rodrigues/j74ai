import os
import sys

# Add parent directory to path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from git_manager import GitManager

metadata = {
    "name": "agent_git_workflow",
    "description": "Handles git branching, staging, and committing based on task info.",
    "args": {
        "action": "create_branch | commit | push",
        "task_id": "Optional: Task ID for branch naming",
        "message": "Optional: Commit message"
    }
}

def execute(action: str, task_id: str = "T001", message: str = "wip: automated change", **kwargs):
    # Assume repository is mounted or located at a specific path
    repo_path = kwargs.get("repo_path", "./target_repo")
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        git = GitManager(repo_path)
        try:
            git.init_repo()
        except:
            pass # Already initialized
    else:
        git = GitManager(repo_path)

    try:
        if action == "create_branch":
            desc = kwargs.get("description", "auto-feature")
            result = git.create_branch_from_task(task_id, desc)
            return {"status": "success", "branch": result}

        elif action == "commit":
            git.stage_files()
            result = git.commit(message)
            return {"status": "success", "commit_output": result}

        elif action == "push":
            result = git.push()
            return {"status": "success", "push_output": result}

        else:
            return {"status": "error", "message": f"Unknown action: {action}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
