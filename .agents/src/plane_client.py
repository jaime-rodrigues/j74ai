import os
import json
import requests
from typing import Dict, Any, List, Optional

class PlaneClient:
    """
    Client for interacting with the Plane Kanban API.
    """
    def __init__(self, base_url: str = None, api_token: str = None, project_id: str = None):
        self.base_url = base_url or os.getenv("PLANE_API_URL", "http://localhost:8000/api/v1")
        self.api_token = api_token or os.getenv("PLANE_API_TOKEN", "")
        self.project_id = project_id or os.getenv("PLANE_PROJECT_ID", "")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def create_issue(self, title: str, description: str, priority: str = "Medium") -> Dict[str, Any]:
        """
        Creates a new issue in the backlog.
        """
        if not self.api_token:
             print("Warning: PLANE_API_TOKEN not set. Simulating creation.")
             return {"id": "mock-123", "title": title, "state": "Backlog"}

        url = f"{self.base_url}/workspaces/current/projects/{self.project_id}/issues/"
        payload = {
            "name": title,
            "description_html": description,
            "priority": priority
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create issue: {e}")
            return {}

    def update_issue_state(self, issue_id: str, state_id: str) -> Dict[str, Any]:
        """
        Moves a card to a different column (State).
        """
        if not self.api_token:
             print(f"Simulating update for issue {issue_id} to state {state_id}")
             return {"id": issue_id, "state": state_id}

        url = f"{self.base_url}/workspaces/current/projects/{self.project_id}/issues/{issue_id}/"
        payload = {"state": state_id}
        
        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to update issue: {e}")
            return {}

    def list_issues(self, state_filter: str = None) -> List[Dict]:
        """
        Lists issues, optionally filtering by state.
        """
        if not self.api_token:
            return [{"id": "mock-1", "name": "Test Task", "state": "To Do"}]

        url = f"{self.base_url}/workspaces/current/projects/{self.project_id}/issues/"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if state_filter:
                return [i for i in data if i.get("state") == state_filter]
            return data
        except Exception as e:
            print(f"Failed to list issues: {e}")
            return []
