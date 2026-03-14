import os
import subprocess
import logging
from slugify import slugify

class GitManager:
    """
    Manages local Git repository operations like branching, committing, and pushing.
    Also handles the initial git user configuration from environment variables.
    """
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configure Git user identity for the container from environment variables
        author_name = os.getenv("GIT_AUTHOR_NAME")
        author_email = os.getenv("GIT_AUTHOR_EMAIL")

        if author_name and author_email:
            self._run_command(["git", "config", "--global", "user.name", author_name])
            self._run_command(["git", "config", "--global", "user.email", author_email])
            self.logger.info(f"Git identity configured for {author_name} <{author_email}>.")
        else:
            self.logger.warning("GIT_AUTHOR_NAME or GIT_AUTHOR_EMAIL not set. Commits may fail.")

    def _run_command(self, command: list[str], check=True) -> subprocess.CompletedProcess:
        """Helper to run a git command."""
        return subprocess.run(command, cwd=self.repo_path, check=check, capture_output=True, text=True)

    def create_branch(self, task_id: str, description: str):
        """Creates and checks out a new feature branch."""
        branch_name = f"feature/{task_id}-{slugify(description)}"
        self.logger.info(f"Creating and checking out new branch: {branch_name}")
        self._run_command(["git", "checkout", "-b", branch_name])
        return branch_name

    def commit(self, message: str):
        """Adds all changes and commits them."""
        self.logger.info("Adding all changes to staging area...")
        self._run_command(["git", "add", "."])
        self.logger.info(f"Committing with message: '{message}'")
        self._run_command(["git", "commit", "-m", message])