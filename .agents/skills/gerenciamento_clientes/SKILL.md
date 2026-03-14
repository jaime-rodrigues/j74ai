---
name: Gerenciamento de Projetos de Clientes
description: Habilidade para criar novos projetos de clientes baseados no modelo "Cliente Base" e integrá-los corretamente à solução.
---

# Gerenciamento de Projetos de Clientes

Esta habilidade descreve o processo padrão para criar uma nova customização de cliente (`src\Clientes`) na solução DevMaster.

## Passos para Criar um Novo Projeto de Cliente

### 1. Preparação da Estrutura
- Localize a pasta modelo: `src\Clientes\Cliente Base`.
- Crie uma nova pasta em `src\Clientes\<NomeCliente>`.
- Copie todo o conteúdo de `Cliente Base` para a nova pasta.
- Renomeie o arquivo `ClienteBase.csproj` para `<NomeCliente>.csproj`.
- Remova as pastas `bin` e `obj`, caso tenham sido copiadas.

### 2. Configuração Interna do Projeto
No arquivo `Properties\Resources.Designer.cs`:
- Atualize o `namespace` para `<NomeCliente>.Properties`.
- No método `ResourceManager`, atualize a string para `"<NomeCliente>.Properties.Resources"`.

### 3. Integração na Solução (DevMaster.sln)
Ao adicionar o projeto ao arquivo `.sln`, siga o padrão de organização por pastas de solução.

**Estrutura Requerida no .sln**:
1. **Pasta de Solução**: Crie uma entrada de projeto com o GUID de pasta (`{2150E333-8FDC-42A3-9474-1A3956D46DE8}`) usando o nome do cliente.
2. **Projeto CSharp**: Adicione a referência ao `.csproj` do cliente.

**Exemplo de Bloco de Projeto**:
```sln
Project("{2150E333-8FDC-42A3-9474-1A3956D46DE8}") = "<NomeCliente>", "<NomeCliente>", "{GUID_PASTA_NOVO}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "<NomeCliente>", "Clientes\<NomeCliente>\<NomeCliente>.csproj", "{GUID_PROJETO_NOVO}"
EndProject
```

3. **Aninhamento (NestedProjects)**:
Sempre coloque o novo projeto e sua pasta de solução dentro da pasta principal de "Clientes".
- A pasta do cliente deve ser filha de `Clientes` (`{4BE54250-1FA2-47AC-ADF9-A4E5318A584D}`).
- O projeto do cliente deve ser filho da pasta do cliente criada no passo anterior.

**Exemplo de NestedProjects**:
```sln
	GlobalSection(NestedProjects) = preSolution
		{GUID_PASTA_NOVO} = {4BE54250-1FA2-47AC-ADF9-A4E5318A584D}
		{GUID_PROJETO_NOVO} = {GUID_PASTA_NOVO}
	EndGlobalSection
```

## Resumo de GUIDs Importantes
- **Tipo Pasta de Solução**: `{2150E333-8FDC-42A3-9474-1A3956D46DE8}`
- **Tipo Projeto C#**: `{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}`
- **GUID da Pasta "Clientes"**: `{4BE54250-1FA2-47AC-ADF9-A4E5318A584D}`

> [!IMPORTANT]
> Ao criar GUIDs novos para a pasta de solução, utilize o comando PowerShell `[Guid]::NewGuid().ToString("B").ToUpper()`.
