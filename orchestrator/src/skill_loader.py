import os
import importlib.util
import re
import inspect
from typing import Dict, Any, Callable

class SkillLoader:
    def __init__(self):
        self.skills: Dict[str, Callable] = {}
        self.metadata: Dict[str, Any] = {}

    def load_skills_from_directory(self, directory: str, category: str = "general"):
        """
        Recursively loads python scripts (.py) and knowledge documents (.md) from a directory.
        - .py files are treated as executable skills.
        - .md files are treated as knowledge skills.
        """
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return

        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith(".py") and not file.startswith("__"):
                    self._load_executable_skill(path, category)
                elif file.endswith(".md"):
                    self._load_knowledge_skill(path, category)

    def _parse_md_frontmatter(self, path: str) -> Dict[str, str]:
        """Parses simple key: value frontmatter from a markdown file."""
        metadata = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # A simple parser for --- frontmatter ---
                match = re.match(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if match:
                    frontmatter = match.group(1)
                    for line in frontmatter.splitlines():
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
        except Exception as e:
            print(f"Could not parse frontmatter from {path}: {e}")
        return metadata

    def _load_knowledge_skill(self, path: str, category: str):
        """Loads metadata from a .md skill file."""
        try:
            md_meta = self._parse_md_frontmatter(path)
            skill_name = md_meta.get("name")
            if skill_name:
                self.metadata[skill_name] = {
                    "path": path,
                    "category": category,
                    "type": "knowledge",
                    "description": md_meta.get("description", ""),
                }
                print(f"Loaded knowledge skill: {skill_name} ({category})")
        except Exception as e:
            print(f"Failed to load knowledge skill from {path}: {e}")

    def _load_executable_skill(self, path: str, category: str):
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
                        "type": "executable",
                        "description": module.metadata.get("description", ""),
                        "args": module.metadata.get("args", {})
                    }
                    print(f"Loaded executable skill: {skill_name} ({category})")
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
            print(f"Executing skill '{name}'...")
            return skill_func(**kwargs)
        else:
            raise ValueError(f"Executable skill '{name}' not found or is a knowledge-only skill.")
