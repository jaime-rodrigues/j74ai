---
name: Padrões Comuns (Clientes)
description: Padrões de implementação frequentes encontrados nos projetos em src\Clientes, incluindo SelectSQL, loops e UI.
---

# Padrões Comuns (Clientes)

Esta habilidade detalha as implementações mais frequentes encontradas nas customizações de clientes (`src\Clientes`).

## 1. Construção de Consultas (SelectSQL)
Em vez de concatenar strings manualmente, use a classe `SQL.SelectSQL` para construir queries estruturadas.

**Exemplo**:
```csharp
SQL.SelectSQL sql = new SQL.SelectSQL();
sql.Campos = "aaa_codigo, aaa_descricao, dmaaa.dm_id";
sql.Tabela = Aplicacao.getTabSQL("dmaaa");
sql.Associacoes.Add("left join " + Aplicacao.getTabSQL("dmabd") + " on (abd_codigo = aaa_caixa)");
sql.Condicoes.Add("dmaaa.dm_deletado = 0");
sql.Condicoes.Add("aaa_ativo = 'S'");
sql.Ordem = "aaa_descricao";

DataTable dt = Aplicacao.ConsultarSQL(sql.GerarSQL());
```
*   **Vantagem**: Facilita a manutenção e adição de `JOINs` e `Unions` (`sql.Unioes.Add(...)`).

## 2. Iteração de Dados (foreach)
O padrão mais comum é iterar sobre as linhas de um `DataTable` ou os registros de uma `DBTabela`.

**DataTable**:
```csharp
foreach (DataRow dr in dt.Rows)
{
    string codigo = dr["aaa_codigo"].ToString();
    decimal valor = dr["aaa_valor"].ToDecimal(); // Use o método de extensão .ToDecimal()
}
```

**DBTabela (Registros Filtrados)**:
```csharp
foreach (DataRow dr in dbTabela.Tabela.Rows)
{
    // Lógica aqui
}
```

## 3. Indicador de Carregamento (AguardarV2.Processar)
O método estático `Processar` é a forma moderna e recomendada de exibir diálogos de espera. Ele gerencia automaticamente a criação (`Show`), o tratamento de exceções (`try-catch`) e o fechamento (`Fechar`) do formulário.

### Possibilidades de Uso

**Uso Básico com Progresso**:
```csharp
AguardarV2.Processar(this.Form, "Processando Dados", false, true, total, true, false, (ag) => {
    foreach (DataRow dr in dt.Rows) {
        ag.Descricao = "Processando: " + dr["codigo"];
        // ... lógica ...
        ag.IncrementaProgresso();
        if (ag.Cancelado) break; // Verificação de cancelamento se bPermiteCancelar = true
    }
});
```

**Uso com Tratamento de Erro Integrado**:
```csharp
AguardarV2.Processar(this.Form, "Calculando Estoque", false, false, 0, false, false, 
    (ag) => {
        // Lógica do processo
    }, 
    (ex) => {
        FormErro.Show("Erro durante o cálculo", ex);
    }
);
```

### Parâmetros do Processar:
1. `formPai`: O formulário atual (`this.Form` ou `this`).
2. `sTitulo`: Texto principal exibido.
3. `bUsaLogs`: Mostra/Esconde o painel de histórico/grid inferior.
4. `bUsaProgresso`: Mostra/Esconde a barra de progresso.
5. `iQtdProcessos`: Valor máximo do progresso.
6. `bMostraTempos`: Calcula e exibe tempo decorrido/restante.
7. `bPermiteCancelar`: Exibe botão de cancelar (requer checar `ag.Cancelado`).
8. `callback`: Ação a ser executada (`ag` é a instância do controle).
9. `errorCallback` (Opcional): Ação executada em caso de exceção.

## 4. Manipulação de Dados (DBTabela)
Padrões para inserção/edição e busca em tabelas relacionadas.

**Localizar e Salvar**:
```csharp
DBTabela dbXAE = TelaDmaaa.Tabela.Filhos["dmxae"];

if (!dbXAE.Localizar("01", valorChave1, valorChave2)) 
    dbXAE.Inserir();
else 
    dbXAE.Editar();

dbXAE["coluna"].Valor = novoValor;

if (!dbXAE.Salvar())
    dbXAE.Cancelar();
```

## 5. Manipulação de DataTable
Uso de filtros locais e colunas calculadas.

**Filtro Local (Select)**:
```csharp
DataRow[] rows = dt.Select("status = 'A' AND valor > 100");
```

**Coluna Calculada**:
```csharp
dt.Columns.Add("diferenca", typeof(decimal), "valor_contado - valor_calculado");
```

## Melhores Práticas
- **Extensões de Tipo**: Use `.ToDecimal()`, `.ToDateTime()`, `.ToInt32()` disponíveis no namespace `DevMaster.Classes` para conversões seguras.
- **Strings de SQL**: Use `\n` ao final de cada linha de string SQL para facilitar a depuração no log.
- **Joins**: Sempre inclua `dm_deletado = 0` em todas as tabelas envolvidas no `JOIN`.
