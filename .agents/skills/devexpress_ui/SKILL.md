---
name: DevExpress UI
description: Melhores práticas para usar controles DevExpress e layouts WinForms na solução DevMaster.
---

# DevExpress UI

Esta habilidade cobre a integração de controles DevExpress dentro da aplicação Windows Forms do DevMaster.

## Controles Comuns

### XtraGrid
O controle principal para exibição de dados.
- **Customização**: Use os eventos do GridView (ex: `CustomDrawCell`, `RowStyle`) para ajustes visuais.
- **Binding de Dados**: Sempre vincule o `GridControl.DataSource` a um `DataTable` ou `DataView` da camada de acesso a dados do framework.

### XtraBars & Ribbon
Usado para menus e barras de ferramentas.
- **BarAndDockingController**: Use `BarAndDockingController.Default` para gerenciar skins e aparência global.
- **Tamanho de Glyphs**: O tamanho padrão de glyph é 20x20 (`BarAndDockingController.Default.PropertiesBar.DefaultGlyphSize`).

### Editores (XtraEditors)
- **Uso de Editores Avançados**: Quando solicitado, habilite a edição de texto avançada: `WindowsFormsSettings.UseAdvancedTextEdit = DevExpress.Utils.DefaultBoolean.True`.
- **MessageBox**: Use `XtraMessageBox.Show` ou o wrapper `FormMensagemV2` do framework.

## Padrões de UI

### Indicador de Aguarde (AguardarV2)
Para operações de longa duração, use o método estático `Processar`. Ele gerencia o ciclo de vida do diálogo de carregamento e blocos try/finally.

**Exemplo Progressivo**:
```csharp
AguardarV2.Processar(this.Form, "Título do Processo", false, true, totalRegistros, true, true, (ag) => {
    // Caso bPermiteCancelar seja true, verifique ag.Cancelado
    if (ag.Cancelado) return; 

    ag.Descricao = "Atualizando...";
    ag.IncrementaProgresso();
});
```

### Manipuladores de Eventos
Ao adicionar lógica customizada a formulários existentes via Pontos de Entrada, você pode precisar limpar ou modificar manipuladores de eventos de controles DevExpress. Use reflexão se os manipuladores forem privados, ou a API específica do controle se forem públicos.

## Melhores Práticas
1. **Consistência de Skin**: Sempre respeite a skin do sistema. Use `WindowsFormsSettings` para configurar comportamentos globais do DevExpress.
2. **Performance**: Para grids com grandes conjuntos de dados, habilite `OptimizeRemoteConnectionPerformance` se estiver rodando em Terminal Server.
3. **Acessibilidade**: Forneça tooltips claros e descrições acessíveis para botões e itens de menu.
4. **Validação**: Use `DXErrorProvider` para validação complexa de formulários.
