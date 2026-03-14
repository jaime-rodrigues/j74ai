import httpx
import os

def analyze_schema(table_name: str) -> str:
    """
    Skill para o DBAAgent analisar uma tabela via MCP Server.
    """
    mcp_url = os.getenv("MCP_URL", "http://mcp-server:8000")
    
    # Consulta a Camada 4 - MCP Server
    response = httpx.post(f"{mcp_url}/tools/get_columns", json={"table": table_name})
    
    if response.status_code == 200:
        data = response.json()
        columns_info = "\n".join([f"- {col['name']} ({col['type']})" for col in data.get("columns", [])])
        return f"Análise da tabela {table_name}:\n{columns_info}"
    
    return f"Erro ao acessar schema: {response.text}"