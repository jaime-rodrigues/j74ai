from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="Autonomous Factory - MCP Server (Database)")

def get_db_connection():
    return psycopg2.connect(os.getenv("DB_URL"))

class TableQuery(BaseModel):
    table: str

@app.get("/tools")
def list_tools():
    """Expõe as ferramentas disponíveis para os agentes via MCP."""
    return {
        "tools": [
            "get_tables", "get_columns", "get_triggers", 
            "get_constraints", "get_relations", "get_indexes", 
            "get_procedures", "get_dictionary"
        ]
    }

@app.post("/tools/get_columns")
def get_columns(query: TableQuery):
    """Exemplo de ferramenta do MCP para ler colunas do Postgres."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s;
        """, (query.table,))
        columns = [{"name": row[0], "type": row[1]} for row in cursor.fetchall()]
        return {"table": query.table, "columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()