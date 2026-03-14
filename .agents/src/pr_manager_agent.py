from .agent_base import BaseAgent
from ..github_manager import GitHubManager
from ..git_manager import GitManager
import os

class PrManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PrManagerAgent",
            role="Manages pull requests and communicates with the GitHub API."
        )
        # These should be dynamically configured or from env vars
        repo_owner = os.getenv("GITHUB_REPO_OWNER", "your-owner")
        repo_name = os.getenv("GITHUB_REPO_NAME", "your-repo")
        self.github_manager = GitHubManager(repo_owner=repo_owner, repo_name=repo_name)
        self.git_manager = GitManager(repo_path="/app/repo")
        self.load_skill("create_pr", self.create_pr_skill)

    def create_pr_skill(self, title: str, body: str, base_branch: str = "main"):
        """
        Skill to create a pull request on GitHub.
        """
        try:
            current_branch = self.git_manager.get_current_branch()
            self.logger.info(f"Pushing branch '{current_branch}' to origin...")
            self.git_manager.push(branch=current_branch)

            self.logger.info(f"Creating Pull Request from '{current_branch}' to '{base_branch}'...")
            pr_data = self.github_manager.create_pull_request(title=title, head=current_branch, base=base_branch, body=body)
            self.logger.info(f"Successfully created PR: {pr_data.get('html_url')}")
            return {"status": "success", "pr_url": pr_data.get('html_url')}
        except PermissionError as e:
            self.logger.error(f"Authentication Error during PR creation: {e}")
            return {"status": "error", "error_type": "authentication", "message": str(e)}
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during PR creation: {e}")
            return {"status": "error", "error_type": "unknown", "message": str(e)}