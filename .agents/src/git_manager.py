import subprocess
import os
from typing import List, Optional

class GitManager:
    """
    Wrapper for Git CLI operations.
    Executes commands in the repository root.
    """
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)

    def _run_git(self, args: List[str]) -> str:
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {' '.join(args)}\nError: {e.stderr}")

    def init_repo(self):
        return self._run_git(["init"])

    def get_current_branch(self) -> str:
        return self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    def checkout_branch(self, branch_name: str, create: bool = False):
        args = ["checkout"]
        if create:
            args.append("-b")
        args.append(branch_name)
        return self._run_git(args)

    def stage_files(self, files: Optional[List[str]] = None):
        if not files:
            return self._run_git(["add", "."])
        return self._run_git(["add"] + files)

    def commit(self, message: str):
        return self._run_git(["commit", "-m", message])

    def push(self, remote: str = "origin", branch: str = None):
        if not branch:
            branch = self.get_current_branch()
        # In a real scenario, we might need to handle authentication here or rely on SSH keys/Env vars
        return self._run_git(["push", remote, branch])

    def status(self) -> str:
        return self._run_git(["status", "--short"])

    def create_branch_from_task(self, task_id: str, description: str):
        """Generates a semantic branch name."""
        clean_desc = description.lower().replace(" ", "-").replace("/", "-")
        branch_name = f"feature/{task_id}-{clean_desc}"
        return self.checkout_branch(branch_name, create=True)
