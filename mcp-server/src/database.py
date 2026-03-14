import os
import asyncpg
from pgvector.asyncpg import register_vector
from typing import Optional

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        dsn = os.getenv("DATABASE_URL")
        if not dsn:
            raise ValueError("DATABASE_URL env var not set")
        
        self.pool = await asyncpg.create_pool(dsn)
        
        # Register pgvector type
        async with self.pool.acquire() as conn:
            await register_vector(conn)
            
        print("Connected to PostgreSQL + pgvector")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def fetch_context(self, query_embedding: list[float], limit: int = 5):
        """
        Retrieves relevant code snippets using vector similarity.
        Assumes a table 'code_embeddings' exists with a 'embedding' vector column.
        """
        if not self.pool:
            raise ConnectionError("Database not connected")

        sql = """
            SELECT file_path, content, embedding <=> $1 as distance
            FROM code_embeddings
            ORDER BY distance
            LIMIT $2
        """
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, query_embedding, limit)
            return [dict(row) for row in rows]

db = Database()
