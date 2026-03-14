from typing import Dict, Any, List
import logging

class BaseAgent:
    """
    Abstract Base Class for all Autonomous Agents.
    Defines the standard interface for receiving tasks and executing skills.
    """
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory: List[Dict] = []  # Short-term memory (conversation history)
        self.skills: Dict[str, Any] = {}
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.name)

    def load_skill(self, skill_name: str, skill_func: Any):
        """Register a capability for this agent."""
        self.skills[skill_name] = skill_func
        self.logger.info(f"Skill loaded: {skill_name}")

    def plan(self, task_description: str) -> List[str]:
        """
        Analyze the task and break it down into steps.
        This would typically involve an LLM call.
        """
        self.logger.info(f"Planning task: {task_description}")
        return ["analyze_context", "execute_action", "verify_result"]

    def execute(self, task: str, **context):
        """
        Main execution loop.
        1. Receive task
        2. Plan steps
        3. Execute skills
        """
        self.logger.info(f"Starting execution for: {task}")
        plan = self.plan(task)
        
        results = {}
        for step in plan:
            self.logger.info(f"Executing step: {step}")
            # In a real scenario, map steps to specific skills dynamically
            if step == "analyze_context" and "agent_analyze_code" in self.skills:
                results[step] = self.skills["agent_analyze_code"](file_path=context.get("file_path"))
            
        return results

    def _update_memory(self, content: str):
        self.memory.append({"role": "system", "content": content})
