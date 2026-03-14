from .agent_base import BaseAgent

# --- Planning Cluster ---

class RequirementAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("RequirementAnalyst", "Analyzes user requests and defines scope.")

class SystemArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__("SystemArchitect", "Defines architecture and components.")

class TaskManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("TaskManager", "Manages Kanban tasks and dependencies.")

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Orchestrator", "Coordinates global workflow.")

# --- Data & Backend Cluster ---

class DbSchemaAgent(BaseAgent):
    def __init__(self):
        super().__init__("DbSchema", "Handles DDL and Migrations.")

class SqlOptimizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SqlOptimizer", "Optimizes complex queries.")

class BackendLogicAgent(BaseAgent):
    def __init__(self):
        super().__init__("BackendLogic", "Implements business logic.")

class ApiSpecAgent(BaseAgent):
    def __init__(self):
        super().__init__("ApiSpec", "Manages API contracts.")

# --- Frontend & UX Cluster ---

class FrontendComponentAgent(BaseAgent):
    def __init__(self):
        super().__init__("FrontendComponent", "Generates UI components.")

class StateManagementAgent(BaseAgent):
    def __init__(self):
        super().__init__("StateManagement", "Handles frontend state logic.")

# --- Quality & Security Cluster ---

class TestGenAgent(BaseAgent):
    def __init__(self):
        super().__init__("TestGen", "Generates tests.")

class SecurityAuditorAgent(BaseAgent):
    def __init__(self):
        super().__init__("SecurityAuditor", "Checks for vulnerabilities.")

class CodeReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeReview", "Reviews code style and complexity.")

class DependencyManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("DependencyManager", "Manages dependencies.")

# --- Operations & DevOps Cluster ---

class GitFlowAgent(BaseAgent):
    def __init__(self):
        super().__init__("GitFlow", "Handles Git operations.")

class PrManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("PrManager", "Creates and manages Pull Requests.")

class CiCdConfigAgent(BaseAgent):
    def __init__(self):
        super().__init__("CiCdConfig", "Configures CI/CD pipelines.")

class DockerDevAgent(BaseAgent):
    def __init__(self):
        super().__init__("DockerDev", "Manages Docker configurations.")

# --- Intelligence & Context Cluster ---

class ContextRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__("ContextRetrieval", "Retrieves relevant context.")

class KnowledgeBaseAgent(BaseAgent):
    def __init__(self):
        super().__init__("KnowledgeBase", "Updates documentation.")
