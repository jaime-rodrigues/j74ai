# Autonomous Code Evolution System - Estrutura do Repositório (ETAPA 2)

## Organização de Pastas

A estrutura do projeto segue um padrão modular, separando a orquestração, os agentes, as habilidades (skills) e a infraestrutura.

```text
/
├── .agents/                 # Configurações e recursos dos Agentes Autônomos
│   ├── configs/             # Definições JSON/YAML de cada um dos 20 agentes
│   ├── memory/              # Armazenamento local temporário (se não usar DB)
│   └── skills/              # Skills executáveis compartilhadas pelos agentes (Python/Bash)
│
├── orchestrator/            # Núcleo do sistema (n8n + Runtime Customizado)
│   ├── src/                 # Código fonte do runtime do orquestrador
│   ├── workflows/           # Arquivos JSON de workflows do n8n
│   └── skills/              # Skills específicas de orquestração (ex: disparar pipeline)
│
├── mcp-server/              # Model Context Protocol Server
│   ├── src/                 # Implementação do servidor MCP
│   └── adapters/            # Conectores para PostgreSQL, Git, FileSystem
│
├── infrastructure/          # Infraestrutura e Deploy
│   ├── docker/              # Dockerfiles e configs de container
│   │   ├── agents/
│   │   ├── orchestrator/
│   │   └── mcp/
│   ├── database/            # Scripts de inicialização do Postgres/pgvector
│   └── docker-compose.yml   # Definição dos serviços (gerado na Etapa 3)
│
├── shared/                  # Bibliotecas compartilhadas entre componentes
│   ├── utils/
│   └── types/
│
├── docs/                    # Documentação do projeto
│
└── scripts/                 # Scripts auxiliares de setup e manutenção
```

## Definição das Pastas de Skills

As skills são a "mão na massa" dos agentes. Elas residem em dois locais principais:

1.  **`.agents/skills/`**: Skills de uso geral dos agentes de trabalho.
    *   Exemplos: `run_linter.py`, `git_commit.sh`, `db_migrate.py`.
    *   Estrutura interna sugerida:
        *   `coding/` (refatoração, geração)
        *   `ops/` (git, docker)
        *   `data/` (sql, pandas)

2.  **`orchestrator/skills/`**: Skills de alto nível para controle de fluxo.
    *   Exemplos: `assign_task_plane.js`, `trigger_deployment.sh`.

## Detalhamento dos Arquivos Principais (Placeholder)

*   `.agents/configs/agents_manifest.json`: Lista e configuração dos 20 agentes.
*   `mcp-server/config.yaml`: Configuração de conexão com DB e Repositórios.
