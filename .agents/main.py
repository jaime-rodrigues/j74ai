import os
import sys

# Add the parent directory to the path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import *
from orchestrator.src.skill_loader import SkillLoader

def main():
    """
    Main entrypoint for the Agent Swarm.
    Initializes all agents and loads their skills.
    """
    print("--- Initializing Agent Swarm ---")

    # 1. Load all available skills
    skill_loader = SkillLoader()
    agent_skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    skill_loader.load_skills_from_directory(agent_skills_dir, category="agent")
    
    # 2. Instantiate all agents
    agents = {
        "RequirementAnalyst": RequirementAnalystAgent(),
        "SystemArchitect": SystemArchitectAgent(),
        "TaskManager": TaskManagerAgent(),
        "DbSchema": DbSchemaAgent(),
        "BackendLogic": BackendLogicAgent(),
        "TestGen": TestGenAgent(),
        "GitFlow": GitFlowAgent(),
        "CodeReview": CodeReviewAgent(),
        # ... instantiate others as needed
    }

    print(f"\n--- {len(agents)} Agents Instantiated ---")

    # 3. Assign skills to a specific agent
    code_reviewer = agents["CodeReview"]
    analyze_skill = skill_loader.get_skill("agent_analyze_code")
    
    if analyze_skill:
        code_reviewer.load_skill("agent_analyze_code", analyze_skill)

    # 4. Simulate a task execution
    print("\n--- Simulating Task for CodeReviewAgent ---")
    task_description = "Review the file 'src/main.py' for quality issues."
    
    # The context would be provided by the orchestrator
    context = {"file_path": "src/main.py"}
    
    result = code_reviewer.execute(task_description, **context)
    print("\n--- Task Result ---")
    print(result)

if __name__ == "__main__":
    main()
