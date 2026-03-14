import os
import sys

# Add parent directory to path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from plane_client import PlaneClient

metadata = {
    "name": "agent_kanban_update",
    "description": "Updates the status of tasks in the Plane Kanban board.",
    "args": {
        "action": "create | update | list",
        "task_title": "Required for create",
        "task_id": "Required for update",
        "new_state": "Required for update (e.g. In Progress, Done)"
    }
}

def execute(action: str, task_title: str = "", task_id: str = "", new_state: str = "", **kwargs):
    client = PlaneClient()
    
    if action == "create":
        if not task_title:
            return {"error": "Missing task_title"}
        result = client.create_issue(task_title, kwargs.get("description", "Auto-generated"))
        return {"status": "created", "issue": result}
        
    elif action == "update":
        if not task_id or not new_state:
            return {"error": "Missing task_id or new_state"}
        result = client.update_issue_state(task_id, new_state)
        return {"status": "updated", "issue": result}
        
    elif action == "list":
        result = client.list_issues(kwargs.get("filter"))
        return {"status": "success", "count": len(result), "issues": result}
        
    else:
        return {"error": f"Unknown action: {action}"}
