-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table for storing code embeddings (RAG)
CREATE TABLE IF NOT EXISTS code_embeddings (
    id SERIAL PRIMARY KEY,
    file_path TEXT NOT NULL,
    content TEXT,
    embedding vector(768), -- Dimension depends on the model (e.g., OpenAI text-embedding-ada-002 is 1536, SBERT is 768)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Agent Long-term Memory
CREATE TABLE IF NOT EXISTS agent_memory (
    id SERIAL PRIMARY KEY,
    agent_name TEXT NOT NULL,
    context TEXT,
    embedding vector(768),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for tracking Task Execution History
CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    task_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,
    result JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
