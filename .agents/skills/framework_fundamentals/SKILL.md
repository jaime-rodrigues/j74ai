---
name: Fundamentos do Framework
description: Padrões arquiteturais principais, pontos de entrada e estado global da aplicação para a solução DevMaster.
---

# Fundamentos do Framework

Esta habilidade cobre a arquitetura básica da solução DevMaster e como usar corretamente as classes principais do framework.

## Padrões Principais

### Pontos de Entrada (Ponto de Entrada)
As customizações devem sempre ser implementadas através do padrão "Ponto de Entrada" usando a classe `CustomizacoesV2`. Isso permite a modificação do comportamento padrão do sistema sem alterar o código base.

**Exemplo de Uso**:
```csharp
new CustomizacoesV2<string>("pe_NomeDaClasse").PontoDeEntrada("NomeDoMetodo", argumentos);
```

Pontos de entrada comuns:
- `pe_DevMaster`: Inicialização da aplicação.
- `pe_Aplicacao`: Conexão e autenticação.
- `pe_PainelPagamentoV2`: Lógica de processamento de pagamentos.

### Estado da Aplicação (Aplicacao)
A classe estática `Aplicacao` contém o estado global da aplicação. Consulte-a para obter informações sobre o usuário atual, empresa, filial e estado da conexão.

**Propriedades Chave**:
- `Aplicacao.devEmpresa`: Código da empresa atual.
- `Aplicacao.devFilial`: Código da filial atual.
- `Aplicacao.devUsuario`: Nome do usuário atual.
- `Aplicacao.iIdUsuario`: ID único do usuário logado.
- `Aplicacao.BancoAtivo`: Nome do banco de dados atual (geralmente "devmaster").

### Manipulação de Mensagens
Evite usar o `MessageBox.Show` padrão. Em vez disso, use as classes de mensagem do framework:
- `FormMensagemV2.Show(titulo, mensagem, botoes, icone)`: Mensagens padrão.
- `FormErro.Show(mensagem, exp)`: Para exibir e logar exceções.

## Melhores Práticas
1. **Nunca reinvente a roda**: Verifique `Aplicacao` e `DBTabela` para métodos utilitários existentes antes de implementar nova lógica.
2. **Trate Exceções**: Use `FormErro.Show` para garantir que os erros sejam devidamente registrados no sistema.
3. **Verifique a Conexão**: Use `Aplicacao.bConectadoServidor` para verificar o estado da conexão antes de realizar operações dependentes de rede.
