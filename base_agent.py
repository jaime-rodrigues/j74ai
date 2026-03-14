import httpx
import importlib
import os

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.openclaw_url = os.getenv("OPENCLAW_URL", "http://openclaw:8081")
        self.skills = {}

    def load_skill(self, skill_name: str, module_path: str):
        """Carrega dinamicamente skills do orquestrador ou de .agents/skills"""
        try:
            module = importlib.import_module(module_path)
            self.skills[skill_name] = getattr(module, skill_name)
            print(f"Skill {skill_name} carregada com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar skill {skill_name}: {e}")

    def execute_via_openclaw(self, action: str, payload: dict):
        """
        Integração com a Camada 5 - OpenClaw.
        Delega a execução real (file edit, shell, git) para o executor sandboxed.
        """
        print(f"[{self.name}] Solicitando OpenClaw para executar: {action}")
        response = httpx.post(f"{self.openclaw_url}/execute", json={
            "action": action,
            "parameters": payload
        })
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Falha na execução OpenClaw: {response.text}")

    def write_code(self, filepath: str, code_content: str):
        """Exemplo prático de uso do OpenClaw para edição de arquivos."""
        return self.execute_via_openclaw("file.write", {
            "path": filepath,
            "content": code_content
        })
        
    def run_tests(self, command: str):
        """Exemplo prático de uso do OpenClaw para execução de comandos."""
        return self.execute_via_openclaw("shell.run", {
            "command": command
        })