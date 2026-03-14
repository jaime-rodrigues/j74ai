import os
import requests
from typing import Optional, List

class GitHubManager:
    """
    Manages interactions with the GitHub API.
    """
    def __init__(self, repo_owner: str, repo_name: str):
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.token = os.getenv("GITHUB_PAT")
        if not self.token:
            raise ValueError("GITHUB_PAT environment variable not set.")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _request(self, method: str, endpoint: str, json: Optional[dict] = None) -> dict:
        try:
            response = requests.request(method, f"{self.api_url}{endpoint}", headers=self.headers, json=json)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            if response.status_code == 204: # No Content
                return {}
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise PermissionError(f"GitHub API authentication failed. Check your GITHUB_PAT. Details: {e.response.text}")
            raise e # Re-raise other HTTP errors

    def create_pull_request(self, title: str, head: str, base: str, body: str = "") -> dict:
        """Creates a pull request."""
        endpoint = "/pulls"
        data = {
            "title": title, "head": head, "base": base, "body": body
        }
        return self._request("POST", endpoint, json=data)