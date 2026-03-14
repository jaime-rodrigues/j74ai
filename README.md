# Autonomous Code Evolution System (ACES)

O ACES é uma plataforma distribuída de agentes autônomos de engenharia de software, projetada para interpretar solicitações de melhoria, planejar tarefas técnicas e evoluir automaticamente uma base de código. O sistema orquestra agentes especializados para lidar com tudo, desde arquitetura e alterações de esquema de banco de dados até geração de código, testes e controle de versão, culminando em um pull request pronto para revisão humana.

## Princípios Fundamentais

*   **Autonomia**: Agentes operam de forma independente em tarefas especializadas.
*   **Orquestração**: Um motor de fluxo de trabalho central gerencia o processo de ponta a ponta.
*   **Consciência de Contexto**: Um sistema de Geração Aumentada por Recuperação (RAG) fornece aos agentes o contexto relevante da base de código e da documentação existentes.
*   **Humano-no-Loop**: A saída final é sempre um pull request, garantindo a supervisão e aprovação humana antes que qualquer alteração seja mesclada.

## Visão Geral da Arquitetura

O sistema é composto por vários componentes principais que trabalham em conjunto:

1.  **Orquestrador (n8n)**: Gerencia o fluxo de trabalho de alto nível, desde a ingestão da solicitação até a criação final do PR.
2.  **Enxame de Agentes (Agent Swarm)**: Uma coleção de agentes de IA especializados que executam tarefas específicas de engenharia de software (ex: codificação, testes, operações git).
3.  **Servidor MCP (Model Context Protocol)**: Um serviço que fornece uma interface semântica para a base de conhecimento do projeto (código, documentos, etc.) armazenada em um banco de dados PostgreSQL com a extensão `pgvector`.
4.  **Banco de Dados (Postgres + pgvector)**: Armazena estados de tarefas e embeddings para o sistema RAG.
5.  **Gerenciamento de Projetos (Plane Kanban)**: A fonte da verdade para o status da tarefa, integrada ao fluxo de trabalho do agente.

### Fluxo Lógico
`Solicitação` -> `Orquestrador` -> `Plane (Criação de Tarefa)` -> `Enxame de Agentes` <-> `Servidor MCP/DB` -> `Git (PR)`

## Stack de Tecnologia

*   **Orquestração**: n8n.io
*   **Conteinerização**: Docker, Docker Compose
*   **Banco de Dados**: PostgreSQL com extensão `pgvector`
*   **Gerenciamento de Projetos**: Plane
*   **Runtimes dos Agentes**: Baseado em Python (compatível com frameworks como Antigravity/OpenClaw)
*   **Controle de Versão**: Git

## Estrutura do Repositório

O projeto é organizado em componentes modulares:

```text
/
├── .agents/                 # Configurações, skills e runtime dos agentes
├── orchestrator/            # Workflows do n8n e lógica de orquestração customizada
├── mcp-server/              # Servidor do Model Context Protocol para RAG
├── infrastructure/          # Configs do Docker e scripts de banco de dados
├── shared/                  # Bibliotecas compartilhadas
├── docs/                    # Documentação do projeto
└── scripts/                 # Scripts auxiliares para setup e manutenção
```

## Como Começar

### Pré-requisitos

*   Docker e Docker Compose
*   Git
*   Um arquivo `.env` (veja a seção de Configuração)

### Instalação e Inicialização

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repo>
    cd <nome-do-repo>
    ```

2.  **Crie o arquivo de ambiente:**
    Crie um arquivo `.env` na raiz do projeto. Veja a seção `Configuração` abaixo para as variáveis necessárias.

3.  **Execute o script de inicialização:**
    Este script irá construir as imagens Docker, iniciar todos os serviços e realizar verificações de saúde.
    ```bash
    chmod +x ./scripts/start.sh
    ./scripts/start.sh
    ```

4.  **Acesse os serviços:**
    *   **UI do Orquestrador (n8n)**: `http://localhost:5678`
    *   **API do Servidor MCP**: `http://localhost:8000`
    *   **API do Plane**: `http://localhost:8081`

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis. Elas são usadas pelo `docker-compose.yml` para configurar os serviços.

```env
# Credenciais do PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=aces_db

# Credenciais de Admin do n8n
N8N_USER=admin
N8N_PASS=admin

# Chave da API da OpenAI (para o agente de geração de código)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Identidade do Git para commits automáticos
# Usado pelo GitFlowAgent para autoria dos commits.
GIT_AUTHOR_NAME="ACES Agent"
GIT_AUTHOR_EMAIL="bot@your-domain.com"

# Token de Acesso Pessoal (PAT) do GitHub
# Necessário para criar Pull Requests. Deve ter escopo de 'repo'.
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_REPO_OWNER=your-github-username
GITHUB_REPO_NAME=your-repo-name

# Token da API do Plane (para integração com o Kanban)
# Gere isso a partir da sua instância do Plane
PLANE_API_TOKEN=pln_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
PLANE_PROJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Como Funciona

A lógica principal é definida como um fluxo de trabalho no n8n (`orchestrator/workflows/code_generation_pipeline.json`).

1.  **Ingestão da Solicitação**: Uma nova tarefa é acionada (ex: via webhook de um formulário).
2.  **Criação de Tarefa no Kanban**: O `TaskManagerAgent` cria uma nova issue no Plane.
3.  **Criação de Branch Git**: O `GitFlowAgent` cria uma feature branch para a tarefa.
4.  **Recuperação de Contexto (RAG)**: O `ContextRetrievalAgent` (através do Servidor MCP) encontra trechos de código e documentação relevantes.
5.  **Geração de Código (LLM)**: Um modelo de geração de código (ex: GPT-4) escreve o código com base na solicitação e no contexto recuperado.
6.  **Escrita em Disco**: Um agente salva o código gerado no sistema de arquivos.
7.  **Commit das Alterações**: O `GitFlowAgent` commita o novo código com uma mensagem semântica.
8.  **Atualização do Kanban**: O `TaskManagerAgent` move a tarefa para a coluna "Em Revisão".
9.  **Criação de Pull Request**: (Passo final) O `PrManagerAgent` cria um pull request para revisão humana.