import os
import sys
from skill_loader import SkillLoader

def main():
    # Define paths relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    orchestrator_skills_dir = os.path.join(base_dir, "..", "skills")
    agent_skills_dir = os.path.join(base_dir, "..", "..", ".agents", "skills")

    loader = SkillLoader()

    print("--- Initializing Skill Loader ---")
    
    # Load Orchestrator specific skills
    print(f"Loading orchestrator skills from: {orchestrator_skills_dir}")
    loader.load_skills_from_directory(orchestrator_skills_dir, category="orchestrator")

    # Load Agent capabilities
    print(f"Loading agent skills from: {agent_skills_dir}")
    loader.load_skills_from_directory(agent_skills_dir, category="agent")

    print("\n--- Available Skills ---")
    for name, meta in loader.list_skills().items():
        skill_type = meta.get('type', 'executable').capitalize()
        print(f"[{meta['category'].upper()}] ({skill_type}) {name}: {meta['description']}")

    # Example execution (uncomment to test if skills exist)
    # try:
    #     loader.execute_skill("example_orchestrator_ping")
    # except Exception as e:
    #     print(e)

if __name__ == "__main__":
    main()
