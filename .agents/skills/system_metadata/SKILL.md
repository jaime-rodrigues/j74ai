---
name: Metadados e Estrutura (dmz)
description: Uso de tabelas de sistema (prefixo dmz) para descobrir a estrutura do banco de dados (tabelas, campos, relações e tipos).
---

# Metadados e Estrutura (dmz)

Esta habilidade descreve como utilizar as tabelas de sistema do DevMaster para entender o dicionário de dados da aplicação. Essas tabelas iniciam com o prefixo `dmz` e são essenciais para construir queries e classes precisas.

## 1. Dicionário de Tabelas (`dmzag`)
Contém o cadastro de todas as tabelas do sistema.
- `zag_nome`: Nome/Prefixo da tabela (ex: `dmaaa`).
- `zag_texto`: Descrição ou título da tabela.
- `zag_modulo`: Módulo ao qual a tabela pertence.

## 2. Dicionário de Campos (`dmzae`)
Contém a definição detalhada de cada coluna.
- `zae_tabela`: Nome da tabela pai.
- `zae_nome`: Nome técnico do campo.
- `zae_tipo`: Tipo de dado (ND=Número, TV=Texto, TM=Memorando, DT=Data, DR=DataHora, HR=Hora, IM=Imagem, BL=Blob).
- `zae_tamanho`: Comprimento total do campo.
- `zae_precisao`: Casas decimais (para tipo ND).
- `zae_contexto`: `R` para campos reais (no banco) e `V` para virtuais (calculados).
- `zae_listaopcoes`: Lista de valores para Combo/Lookup (valor=descrição;(...) ou sub-query `<tabela,valor,descrição,filtro,ordem>`).

## 3. Relações e Chaves Estrangeiras (`dmzaf` e `dmzaa`)
Mapeia como as tabelas se conectam.
- **dmzaf**: Define o nome da relação e as tabelas envolvidas (`zaf_tabela` -> `zaf_reftabela`).
- **dmzaa**: Define o mapeamento de campos individuais entre a tabela filha e a pai (`zaa_campo` -> `zaa_refcampo`).

## 4. Relações Mestre-Detalhe (`dmzac` e `dmzap`)
Define as dependências automáticas entre formulários e tabelas.
- **dmzac**: Relação de tabelas filhas (`zac_tabela` é o mestre, `zac_reftabela` é o detalhe).
- **dmzap**: Campos usados no vínculo entre mestre e detalhe.

## 5. Índices (`dmzak`)
Define as chaves primárias e índices de busca.
- `zak_tabela`: Tabela do índice.
- `zak_codigo`: Código do índice (ex: `01` costuma ser a PK conceitual).
- `zak_unico`: `S` para único, `N` para não único.
- `zak_chave`: Campos que compõem o índice (separados por vírgula).

## Consultas de Metadados via PostgreSQL
Sempre que precisar descobrir a estrutura de uma tabela desconhecida, o agente pode utilizar consultas a estas tabelas para obter informações precisas em vez de tentar adivinhar campos.

**Exemplo: Listar campos reais de uma tabela**:
```sql
SELECT zae_nome, zae_tipo, zae_tamanho, zae_precisao
FROM dmzae
WHERE dm_deletado = 0
AND zae_tabela = 'dmaaa'
AND zae_contexto = 'R'
ORDER BY zae_ordem;
```

**Exemplo: Descobrir relação entre duas tabelas**:
```sql
SELECT zaf_nome, zaf_reftabela, zaa_campo, zaa_refcampo
FROM dmzaf
INNER JOIN dmzaa ON (zaa_tabela = zaf_tabela AND zaa_nome = zaf_nome)
WHERE zaf_tabela = 'dmaaa' AND zaf_dm_deletado = 0;
```
