---
name: Domínio ERP
description: Padrões de lógica de negócio para módulos específicos do ERP na solução DevMaster.
---

# Domínio ERP

Esta habilidade cobre a lógica específica de domínio para vários módulos do ERP dentro do DevMaster.

## Módulos Principais

- **Comercial**: Pedidos de venda, precificação e gestão de clientes.
- **Financeiro**: Contas a pagar/receber, fluxo de caixa e integração bancária.
- **Fiscal**: Geração de NFe/NFCe, cálculos de impostos (ICMS, IPI, PIS, COFINS).
- **Estoque**: Gestão de estoque, operações de armazém e movimentações.
- **PDV (Ponto de Venda)**: Operações de frente de caixa, cupons e vendas rápidas.

## Padrões de Lógica Comuns

### Cálculo (Precificação)
Os cálculos de preço geralmente envolvem múltiplos fatores:
- Preço Base.
- Desconto específico do cliente.
- Impostos regionais.
- Regras de Promoção/Campanha.

### Fiscal (NFe)
- Sempre use as classes de `Faturamento` para geração de XML.
- Garanta que o TLS 1.2 esteja habilitado para comunicação com a SEFAZ: `Faturamento.NFe_4_00.GeradorXML.HabilitarTLSv12()`.

### Estoque (Baixa de Estoque)
- As movimentações devem ser registradas nas tabelas de prefixo `MOV` (ex: `dmmov`).
- Sempre verifique o saldo disponível antes de confirmar uma venda.

## Melhores Práticas
1. **Segregação de Módulos**: Mantenha a lógica de negócio dentro do prefixo/pasta do módulo correspondente.
2. **Regras Fiscais**: Consulte o módulo `Fiscal` para lógica centralizada de cálculo de impostos.
3. **Trilhas de Auditoria**: Todas as alterações em registros financeiros ou de estoque devem ser rastreáveis.
