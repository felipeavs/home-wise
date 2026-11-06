# 03. Roadmap

Cada fase entrega algo utilizável. Só começamos a fase seguinte quando a atual funciona e tem evals.

## Fase 1: foto → JSON → SQLite → tabela

**Objetivo:** provar o fluxo ponta a ponta com o mínimo de peças.

- Extrair itens de foto de nota ou texto com a API da Claude (visão), saída em JSON validado.
- Avaliar o QR code da NFC-e como alternativa ao OCR.
- Gravar em SQLite.
- Streamlit: upload, **revisão antes de salvar** e tabela das compras.
- Primeiras evals: poucas notas reais com gabarito.

**Pronto quando:** uma nota fotografada vira linhas no banco após a sua confirmação, e as evals mostram a taxa de acerto.

## Fase 2: categorização e histórico de preços

- Normalização e categorização de produtos com embeddings (RAG).
- Migração para PostgreSQL + pgvector.
- Histórico de preços por produto.

**Pronto quando:** o mesmo produto escrito de formas diferentes na nota cai no mesmo produto normalizado, e dá para ver a evolução do preço.

## Fase 3: orçamentos e alertas

- Orçamento por categoria.
- Detecção de aumento de preço e de compras fora do padrão (código + estatística simples).
- Central de alertas na interface.
- Agentes Analista de Preços e Guardião de Orçamento explicando os alertas.

**Pronto quando:** estourar um orçamento ou subir o preço de um item recorrente gera alerta com explicação, e os números batem com o SQL.

## Fase 4: relatórios agendados e Telegram

- APScheduler para pareceres diário, semanal e mensal (agente Relator).
- Notificações e alertas por Telegram.

**Pronto quando:** os relatórios chegam sozinhos no horário certo.

## Fase 5: chat, planejamento e qualidade

- Chat sobre os gastos com tool use.
- Planejamento e sugestões de economia.
- Avaliação de qualidade do sistema todo (evals de extração, categorização, alertas e respostas do chat).

**Pronto quando:** dá para perguntar "quanto gastei com carne este mês comparado ao anterior?" e receber a resposta correta, vinda de SQL.

## Em todas as fases

- Toda decisão relevante vira um ADR.
- Ao final de cada sessão, uma entrada em `docs/diario/`.
- Nada de dados financeiros ou chaves no Git.
