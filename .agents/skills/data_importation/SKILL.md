---
name: Importação de Dados
description: Padrões e métodos para importação de dados de outros sistemas usando as classes ImportarDados e ImportaUtils.
---

# Importação de Dados

Esta habilidade detalha o padrão utilizado para importar dados de sistemas legados para a solução DevMaster, focando no uso das classes `ImportarDados` e `ImportaUtils` frequentemente encontradas nos projetos em `src\Clientes`.

## Estrutura Geral da Importação

A rotina de importação geralmente é centralizada em um método, como `ImportaDados.Importar()`, que usa uma interface para perguntar ao usuário quais módulos importar e os parâmetros do banco de dados de origem.

### 1. Parâmetros e Diálogo Inicial (InputBox)
O processo inicia solicitando os parâmetros da importação por meio de um `InputBox` configurável.

**Exemplo:**
```csharp
public static void Importar()
{
    Dictionary<string, object> dcParams = InputBox.Show<Dictionary<string, object>>(
        "Importação de Dados", 
        "Informe o tipo de cadastro para ser importado do sistema antigo.",
        new InputBoxCampo[] {
            new InputBoxCampo("database", "Database/Conexão", InputBox.Tipo.Texto, 200, 0, @"c:\Banco\Banco.fdb", "", "", "", ""),
            new InputBoxCampo("trans", "Usar transação", InputBox.Tipo.Texto, 1, 0, "N", "", "S=Sim;N=Não", "", ""),
            new InputBoxCampo("limpar", "Limpar", InputBox.Tipo.Texto, 1, 0, "N", "", "S=Sim;N=Não", "", ""),
            new InputBoxCampo("dmaam", "Clientes", InputBox.Tipo.Texto, 1, 0, "N", "@", "S=Sim;N=Não", "", ""),
            new InputBoxCampo("dmaaa", "Produtos", InputBox.Tipo.Texto, 1, 0, "N", "@", "S=Sim;N=Não", "", ""),
            // Adicione os outros módulos a importar
        }
    );

    if (dcParams == null) return;
    
    // Processamento da importação
}
```

### 2. Controle de Progresso e Transação (AguardarV2)
A importação é encapsulada em `AguardarV2.Processar` para exibir um indicador de progresso, lidando com transações e fechamento da conexão em caso de erros ou conclusão.

**Exemplo:**
```csharp
DBTransacao trans = (dcParams["trans"].ToString() == "S" ? new DBTransacao() : null);

AguardarV2.Processar(Aplicacao.FormAtivo.ActiveMdiChild, "Importação de dados", true, true, 0, true, true, (ag) =>
{
    // Configuração de Conexão com Sistema Origem
    ag.Descricao = "Inicializando conexão";
    ImportaUtils.sStringConexaoBanco = ImportaUtils.sStringConexaoBanco.Replace("[arquivo_database]", dcParams["database"].ToString());

    if (!ImportaUtils.ConectarBanco())
        throw new DevValidaException("Não foi possível conectar na base de dados de origem!");

    // Chamadas para Importar Módulos Específicos
    if (ImportaUtils.MarcadoParaImportar(dcParams, "dmaam"))
    {
        if (dcParams["limpar"].ToString() == "S")
        {
            ImportaUtils.LimparDados(trans, $"delete from {Aplicacao.getTabSQL("dmaam")}");
            // Limpezas adicionais...
        }
        
        if (trans != null) trans.Iniciar();
        ImportarClientes(ag, trans); // Rotina de preenchimento
        
        ag.Descricao = "Confirmando dados...";
        if (trans != null && trans.Ativa) trans.Confirmar();
    }
    
    FormMensagem.Show("Importação de dados", "Processo Concluído!");
}, (ex) => 
{
    if (trans != null && trans.Ativa) trans.Cancelar();
    FormErro.Show("Importação de dados", ex);
});
```

## Padrão de Inserção por Entidade

Na função específica de cada entidade (ex: `ImportarClientes`), consulta-se o banco de origem e itera sobre o `DataTable`, inserindo ou atualizando na tabela de destino (`DBTabela`).

```csharp
private static void ImportarClientes(AguardarV2 ag, DBTransacao trans)
{
    ag.Descricao = "Importando Clientes...";
    DBTabela dbAAM = new DBTabela("dmaam", trans);

    // Consulta banco legado (via ImportaUtils)
    DataTable dtDados = ImportaUtils.ConsultarSQL("SELECT * FROM clientes ORDER BY id");
    ag.QtdProcessos = dtDados.Rows.Count;

    foreach (DataRow dr in dtDados.Rows)
    {
        if (ag.Cancelado) throw new DevValidaException("Processo cancelado");
        
        ag.SetaHistorico();
        string sCodigo = ImportaUtils.NormalizarString(dr["ID"]).PadLeft(6, '0');
        
        // Log individual do registro no AguardarV2
        int iLog = ag.NovoLog($"Cliente > {sCodigo}");

        if (dbAAM.Localizar("01", sCodigo))
        {
            // Opcionalmente atualiza
            ag.SetaStatusLog(iLog, "Atualizado / Existente");
        }
        else
        {
            // Insere novo
            dbAAM.Inserir();
            dbAAM["aam_codigo"].Valor = sCodigo;
            dbAAM["aam_nome"].Valor = ImportaUtils.NormalizarString(dr["NOME"]);
            dbAAM["aam_cnpj"].Valor = ImportaUtils.SomenteNumeros(dr["CNPJ"]);
            // ... Mapear outros campos ...

            dbAAM.Salvar();
            ag.SetaStatusLog(iLog, "Importado");
        }

        ag.IncrementaProgresso();
    }
}
```

## Tratamento e Validação de Dados (ImportaUtils)

O utilitário `ImportaUtils` contém métodos auxiliares essenciais para conversão, sanitização e formatação de dados antes da inserção no banco DevMaster.

*   `ImportaUtils.NormalizarString(object value)`: Remove espaços excessivos, corrige encodings e garante que nulos tornem-se strings vazias.
*   `ImportaUtils.SomenteNumeros(object value)`: Exclui qualquer caractere não numérico, útil para CPF, CNPJ, CEP e telefones.
*   `ImportaUtils.NormalizarTelefones(object ddd, object numero)`: Combina DDD e número no formato padrão.
*   `ImportaUtils.MarcadoParaImportar(Dictionary<string, object> dcParams, string key)`: Verifica de forma padronizada se o usuário escolheu exportar o módulo desejado (compara com `S`).
*   `ImportaUtils.ConsultarSQL(string sql)`: Roda um SQL na base de origem configurada anteriormente.
*   `ImportaUtils.LimparDados(DBTransacao trans, string sql)`: Realiza a exclusão segura na base do DevMaster (usando SQL). Extremo cuidado!

## Melhores Práticas de Importação

1. **Log de Execução Individual**: Use `ag.NovoLog(msg)` e `ag.SetaStatusLog(iLog, msg)` no `AguardarV2` para que problemas pontuais não percam a rastreabilidade e o usuário entenda linha a linha.
2. **Uso Correto de PadLeft**: Chaves e campos no DevMaster frequentemente necessitam formatação com zeros à esquerda: `sCodigo.PadLeft(6, '0')`.
3. **Conversões Seguras**: Use os métodos de extensão do Framework para validação de tipo, como `.ToInt32(false)`, `.ToDecimal(false)`, `.ToDateTime(false)` nos `DataRows`.
4. **Verificação de Duplidade**: Sempre use `dbTabela.Localizar()` pela chave de origem para evitar a reinserção dos mesmos dados ao rodar o processo duas vezes.
