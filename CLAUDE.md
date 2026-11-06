# CLAUDE.md: HomeWise

Slogan: **"Our home, our responsibilities"**

## O que é

Sistema AI-first de controle de gastos do lar. Projeto pessoal com dois objetivos: resolver um problema real (economizar e reduzir desperdício) e aprender AI-first na prática. O dono do projeto está aprendendo, então **ensinar faz parte da entrega**.

## O que o sistema faz

- Lê foto de nota fiscal ou texto descritivo de compras e extrai os itens em JSON estruturado
- Normaliza e categoriza produtos (RAG com embeddings onde agrega)
- Guarda tudo em banco de dados e mantém histórico de preços
- Detecta aumento de preço de alimentos e compras fora do padrão (calculado por código, com estatística simples; o LLM só interpreta e explica)
- Planeja orçamento por categoria
- Agentes: Ingestão, Categorização, Analista de Preços, Guardião de Orçamento, Relator (pareceres diário, semanal e mensal)
- Interface: dashboard, upload com revisão antes de salvar, chat sobre os gastos, central de alertas

## Stack

Python 3.11+ (venv com 3.13), FastAPI, SQLite na Fase 1 (PostgreSQL + pgvector na Fase 2), Streamlit, API da Claude (visão + tool use), loop de tool use próprio (sem frameworks pesados no começo), APScheduler, Telegram na Fase 4.

## Roadmap

1. Foto → JSON → SQLite → tabela no Streamlit
2. Categorização com embeddings, Postgres/pgvector, histórico de preços
3. Orçamentos e alertas
4. Relatórios agendados e Telegram
5. Chat com tool use, planejamento, sugestões de economia, avaliação de qualidade

## Princípios (inegociáveis)

- **Números vêm de SQL/código, nunca do LLM fazendo conta.** O LLM interpreta e explica.
- **RAG só onde agrega:** normalização de produtos, base de conhecimento, memória do lar.
- **Confirmação humana antes de gravar** dados extraídos.
- **Evals desde cedo:** notas reais com gabarito em `evals/`.
- **Dados financeiros e chaves nunca vão para o Git.**
- NFC-e brasileira tem QR code com itens estruturados: avaliar como alternativa ao OCR.

## Convenções

- **Idioma:** documentação em português; código, nomes técnicos, commits de código e identificadores em inglês.
- **Layout:** pacote em `src/homewise/` (ingestion, db, agents, rag, api, config.py); UI em `app/`; testes em `tests/`; evals em `evals/`; dados locais em `data/`.
- **Configuração:** toda leitura de variáveis de ambiente passa por `src/homewise/config.py`. Nunca chamar `os.environ` espalhado pelo código.
- **Estilo:** ruff (line-length 100), type hints, pydantic para schemas de dados.
- **Testes:** pytest. Lógica de cálculo (preços, estatística, orçamento) sempre com teste.
- **Windows:** o dono usa Windows 11 + PowerShell. Comandos de exemplo devem funcionar nele.

## Como trabalhar comigo

- **Explique o porquê** de cada decisão. O dono está aqui para aprender.
- **Um passo por vez.** Termine o passo, resuma e **espere confirmação** antes do próximo.
- **NÃO faça `git commit`, `git push` nem crie repositório no GitHub** sem pedido explícito.
- **Nunca escreva segredos** em arquivos versionados (`.env.example` só com nomes de variáveis).
- **Toda decisão relevante vira um ADR** em `docs/adr/` (formato: Contexto, Decisão, Consequências, Alternativas).
- **Ao final de cada sessão**, sugira uma entrada para `docs/diario/` (pasta só local, ignorada pelo Git; o que foi feito, decisões, aprendizados, próximos passos).
- **Ao instalar qualquer dependência nova**, atualize `docs/dependencias.md` (arquivo versionado): o que é, para que serve aqui, exemplo prático e onde entra.
- **Ao criar ou alterar testes**, atualize o arquivo correspondente em `tests/docs/` (um `.md` com o mesmo nome de cada `test_*.py`, por exemplo `tests/docs/test_schemas.md`): o que cada teste prova, entrada e resultado esperado, e a linha "Última execução".
- Não adicione código de aplicação além do que o passo atual pede.
