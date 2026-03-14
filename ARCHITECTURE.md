# Autonomous Code Evolution System - Arquitetura e Definições (ETAPA 1)

## 1. Arquitetura do Sistema

O sistema é projetado como uma plataforma distribuída de agentes autônomos orquestrados para evoluir bases de código.

### Componentes Principais:
1.  **Orquestrador Central (n8n + Runtime Customizado)**: Gerencia o ciclo de vida da solicitação, invocando agentes e mantendo o estado do fluxo.
2.  **Camada de Agentes (Antigravity/OpenClaw)**: Conjunto de 20 agentes especializados que executam tarefas atômicas ou complexas usando "skills".
3.  **Memória & Dados (PostgreSQL + pgvector)**:
    *   Armazena o estado das tarefas.
    *   Armazena embeddings de código e documentação para recuperação semântica (RAG).
    *   Interface via **MCP Server** (Model Context Protocol).
4.  **Gestão de Projetos (Plane Kanban)**: Fonte da verdade para o status das tarefas e roadmap.
5.  **Controle de Versão (Git Automation)**: Manipulação direta de repositórios, branches e Pull Requests.
6.  **Sistema de Skills**: Scripts executáveis (Python/Bash/Node) localizados em `orchestrator/skills` e `.agents/skills` que conferem capacidades práticas aos agentes (ex: `run_test`, `migrate_db`, `git_commit`).

### Diagrama Lógico:
`Request` -> `Orchestrator` -> `Plane (Task Creation)` -> `Agents Swarm` <-> `MCP Server/DB` -> `Git (PR)`

---

## 2. Descrição dos 20 Agentes Autônomos

Os agentes são divididos em clusters de especialidade:

### Cluster de Planejamento & Gerenciamento
1.  **RequirementAnalystAgent**: Analisa a solicitação em linguagem natural, identifica ambiguidades e define o escopo.
2.  **SystemArchitectAgent**: Define a arquitetura da solução, padrões de design e componentes afetados.
3.  **TaskManagerAgent**: Cria, atualiza e move cards no Plane Kanban. Define dependências entre tarefas.
4.  **OrchestratorAgent**: Monitora o progresso global, resolve bloqueios e reinicia agentes se necessário.

### Cluster de Dados & Backend
5.  **DbSchemaAgent**: Projeta alterações no esquema do banco de dados (DDL) e cria migrações.
6.  **SqlOptimizerAgent**: Escreve e otimiza queries complexas, analisando planos de execução via MCP.
7.  **BackendLogicAgent**: Implementa a lógica de negócios, serviços e controladores.
8.  **ApiSpecAgent**: Define e atualiza contratos de API (OpenAPI/Swagger/GraphQL).

### Cluster de Frontend & UX
9.  **FrontendComponentAgent**: Gera ou atualiza componentes de UI (React/Vue/etc.).
10. **StateManagementAgent**: Gerencia a lógica de estado do frontend (Redux/Context/Stores).

### Cluster de Qualidade & Segurança
11. **TestGenAgent**: Gera testes unitários e de integração para o código novo.
12. **SecurityAuditorAgent**: Analisa o código gerado em busca de vulnerabilidades (OWASP Top 10) e segredos expostos.
13. **CodeReviewAgent**: Simula um revisor humano, verificando estilo, complexidade ciclomática e boas práticas.
14. **DependencyManagerAgent**: Gerencia `package.json`, `requirements.txt`, etc., garantindo versões seguras.

### Cluster de Operações & DevOps
15. **GitFlowAgent**: Gerencia branches (`feature/xxx`), commits semânticos e resolução de conflitos básicos.
16. **PrManagerAgent**: Cria descrições detalhadas de Pull Requests e solicita aprovação.
17. **CiCdConfigAgent**: Mantém arquivos de pipeline (GitHub Actions/GitLab CI).
18. **DockerDevAgent**: Mantém `Dockerfile` e `docker-compose.yml` atualizados.

### Cluster de Inteligência & Contexto
19. **ContextRetrievalAgent**: Usa pgvector para encontrar código similar ou documentação relevante no histórico.
20. **KnowledgeBaseAgent**: Atualiza a documentação técnica do projeto após as mudanças.

---

## 3. Fluxo de Execução

1.  **Ingestão**:
    *   Usuário submete: "Adicionar autenticação 2FA no login".
    *   **RequirementAnalystAgent** processa e estrutura o pedido.

2.  **Planejamento**:
    *   **SystemArchitectAgent** desenha a solução (Tabela `users_2fa`, rotas API, UI Screen).
    *   **TaskManagerAgent** cria tarefas no Plane: "Criar Tabela", "API Backend", "Tela Frontend".

3.  **Execução (Iterativa)**:
    *   *Sub-fluxo Banco de Dados*: **DbSchemaAgent** cria migration -> **GitFlowAgent** comita.
    *   *Sub-fluxo Backend*: **BackendLogicAgent** cria endpoint -> **TestGenAgent** cria testes -> **SecurityAuditorAgent** valida.
    *   *Uso de Skills*: Agentes invocam scripts em `.agents/skills` para rodar linters ou testes reais.
    *   *Contexto*: Agentes consultam **MCP Server** para entender a estrutura atual da classe `User`.

4.  **Consolidação**:
    *   **CodeReviewAgent** faz a varredura final.
    *   **PrManagerAgent** abre o Pull Request.
    *   **TaskManagerAgent** move cards para "Review".

5.  **Conclusão**:
    *   Sistema aguarda aprovação humana no PR.
    *   Após merge, **KnowledgeBaseAgent** atualiza docs.