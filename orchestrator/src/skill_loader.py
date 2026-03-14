import os
import importlib.util
import inspect
from typing import Dict, Any, Callable

class SkillLoader:
    def __init__(self):
        self.skills: Dict[str, Callable] = {}
        self.metadata: Dict[str, Any] = {}

    def load_skills_from_directory(self, directory: str, category: str = "general"):
        """
        Recursively loads python scripts from a directory as skills.
        Expected structure in python files:
        def execute(**kwargs): ...
        metadata = {"name": "...", "description": "..."}
        """
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    path = os.path.join(root, file)
                    self._load_skill(path, category)

    def _load_skill(self, path: str, category: str):
        try:
            module_name = os.path.basename(path).replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "execute") and hasattr(module, "metadata"):
                    skill_name = module.metadata.get("name", module_name)
                    self.skills[skill_name] = module.execute
                    self.metadata[skill_name] = {
                        "path": path,
                        "category": category,
                        "description": module.metadata.get("description", ""),
                        "args": module.metadata.get("args", {})
                    }
                    print(f"Loaded skill: {skill_name} ({category})")
                else:
                    # Skip files that don't follow the skill protocol
                    pass
        except Exception as e:
            print(f"Failed to load skill from {path}: {e}")

    def get_skill(self, name: str) -> Callable:
        return self.skills.get(name)

    def list_skills(self):
        return self.metadata

    def execute_skill(self, name: str, **kwargs):
        skill_func = self.get_skill(name)
        if skill_func:
            print(f"Executing skill: {name}...")
            return skill_func(**kwargs)
        else:
            raise ValueError(f"Skill {name} not found.")
