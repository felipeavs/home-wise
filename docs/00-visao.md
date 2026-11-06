# 00. Visão

## Problema

Gastar com o lar (mercado, farmácia, contas, casa) sem enxergar para onde o dinheiro vai. Os sintomas:

- Notas fiscais em papel ou foto que ninguém analisa.
- Preços de alimentos que sobem aos poucos e passam despercebidos.
- Compras fora do padrão que só aparecem no fim do mês, quando já não dá para corrigir.
- Desperdício (comprar o que já tem, comprar demais) sem registro que permita perceber o padrão.
- Planilhas manuais que dão trabalho e são abandonadas.

## Objetivos

1. **Economizar e reduzir desperdício** no lar, com dados reais de compras.
2. **Reduzir o esforço de registro:** foto da nota ou texto livre vira dado estruturado, sem digitação manual.
3. **Avisar cedo:** detectar aumento de preço e compras fora do padrão perto de quando acontecem.
4. **Dar controle de orçamento** por categoria, com alertas antes de estourar.
5. **Aprender AI-first na prática:** uso de visão, tool use, RAG, agentes e evals em um problema concreto, com decisões documentadas.

## Escopo

- Entrada de compras por foto de nota fiscal ou texto descritivo, com extração em JSON estruturado.
- Avaliar o QR code da NFC-e como alternativa ao OCR.
- Normalização e categorização de produtos.
- Banco de dados com histórico de preços.
- Detecção de aumento de preço e de anomalias, calculada por código com estatística simples.
- Orçamento por categoria e alertas.
- Agentes: Ingestão, Categorização, Analista de Preços, Guardião de Orçamento, Relator.
- Pareceres diário, semanal e mensal.
- Interface em Streamlit: dashboard, upload com revisão antes de salvar, chat sobre os gastos, central de alertas.
- Notificações por Telegram (Fase 4).
- Avaliação de qualidade (evals) com notas reais e gabarito.

## Fora de escopo

- Integração bancária (Open Finance, extratos automáticos).
- Multiusuário, contas de usuário e permissões. O sistema é de um lar, rodando localmente.
- Aplicativo mobile nativo.
- Investimentos, impostos, empréstimos e finanças pessoais além do gasto doméstico.
- LLM fazendo contas. Todo número vem de SQL ou código.
- Frameworks pesados de agentes no início. Começamos com um loop de tool use próprio.
- Hospedagem em nuvem pública na fase inicial.

## Princípios

- Números vêm de SQL/código; o LLM interpreta e explica.
- RAG só onde agrega (ver [ADR 0002](adr/0002-rag-so-onde-agrega.md)).
- Confirmação humana antes de gravar dados extraídos.
- Evals desde cedo.
- Dados financeiros e chaves nunca vão para o Git.

## Critérios de sucesso

- Registrar uma compra leva menos de um minuto, incluindo a revisão.
- A extração acerta os itens e valores de notas reais, medido por evals e não por impressão.
- Um aumento de preço relevante em um item recorrente gera alerta.
- O relatório mensal bate com o SQL, sem nenhum número inventado.
