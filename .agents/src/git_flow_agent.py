from .agent_base import BaseAgent
from ..git_manager import GitManager

class GitFlowAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="GitFlowAgent",
            role="Manages Git branches, commits, and basic workflow operations."
        )
        self.git_manager = GitManager(repo_path="/app/repo")
        self.load_skill("agent_git_workflow", self.git_workflow_skill)

    def git_workflow_skill(self, action: str, **kwargs):
        """
        Skill to perform various git workflow actions.
        - action: 'create_branch', 'commit'
        """
        self.logger.info(f"Executing Git workflow action: {action}")
        try:
            if action == "create_branch":
                branch_name = self.git_manager.create_branch(
                    task_id=kwargs.get("task_id"),
                    description=kwargs.get("description")
                )
                return {"status": "success", "branch_name": branch_name}
            elif action == "commit":
                self.git_manager.commit(message=kwargs.get("message"))
                return {"status": "success", "message": "Commit successful."}
            else:
                raise ValueError(f"Unknown git workflow action: {action}")
        except Exception as e:
            self.logger.error(f"An error occurred during git action '{action}': {e}", exc_info=True)
            return {"status": "error", "message": str(e)}