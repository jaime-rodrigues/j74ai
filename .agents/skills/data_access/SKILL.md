---
name: Acesso a Dados
description: Execução de SQL, interações com banco de dados e gerenciamento de tabelas de dados para a solução DevMaster.
---

# Acesso a Dados

Esta habilidade cobre como interagir com o banco de dados PostgreSQL na solução DevMaster usando as classes de acesso a dados do framework.

## Consultando Dados

### Busca Rápida (PegarValor)
Use `DBTabela.PegarValor` para recuperar um único valor de uma tabela com base em uma condição. Esta é a maneira mais rápida de obter uma informação específica.

**Exemplo**:
```csharp
object valor = DBTabela.PegarValor("dmabd", "abd_pdv", "abd_codigo = '001'");
```

### Executando SQL Customizado (ConsultarSQL)
Para consultas mais complexas que retornam múltiplas colunas ou linhas, use `Aplicacao.ConsultarSQL`. Ele retorna um `DataTable`.

**Exemplo**:
```csharp
SQL.SelectSQL sql = new SQL.SelectSQL();
sql.Campos = "*";
sql.Tabela = Aplicacao.getTabSQL("dmzzz");
sql.Condicoes.Add("dm_deletado = 0");

DataTable dt = Aplicacao.ConsultarSQL(sql.GerarSQL());
```

### Trabalhando com Instâncias de DBTabela
Para operações CRUD completas ou ao trabalhar com relacionamentos Mestre-Detalhe, instancie `DBTabela`.

**Exemplo**:
```csharp
DBTabela tabVendas = new DBTabela("dmvendas");
tabVendas.Abrir();
// ... operações ...
```

## Formatação de SQL
Sempre use `SQL.AjustaValor` para formatar valores em consultas SQL para evitar injeção e lidar corretamente com conversões de tipo (datas, decimais, etc.).

**Exemplo**:
```csharp
string sql = "SELECT * FROM dmaaa WHERE aaa_data = " + SQL.AjustaValor(DateTime.Now, DBTipoCampo.Data);
```

## Melhores Práticas
1. **Sempre verifique `dm_deletado`**: O DevMaster usa soft deletes. Sempre inclua `dm_deletado = 0` em suas cláusulas `WHERE`, a menos que você precise especificamente de registros deletados.
2. **Use Prefixos**: Tabelas e colunas no DevMaster usam prefixos de 3 letras (ex: `abd_` para `dmabd`).
3. **Lide com Nulos**: Ao usar `PegarValor`, verifique por `null` ou `DBNull.Value` antes de fazer o cast.
4. **Transações**: Use `DBTransacao` ao realizar múltiplas operações de escrita relacionadas para garantir a atomicidade.
