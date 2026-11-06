# ADR 0001: Stack inicial

- **Status:** Aceito
- **Data:** 2026-11-06

## Contexto

Projeto pessoal, usado por uma pessoa em um lar, rodando localmente em Windows. Dois objetivos: resolver um problema real e aprender AI-first. Precisamos de uma stack que seja simples de começar, que permita evoluir (busca vetorial, agendamento) e que deixe visível o funcionamento de agentes e tool use.

## Decisão

- **Linguagem:** Python 3.11+ (ambiente virtual criado com 3.13).
- **API:** FastAPI.
- **Banco:** SQLite na Fase 1; PostgreSQL + pgvector na Fase 2.
- **Interface:** Streamlit.
- **LLM:** API da Claude, com visão (leitura de notas) e tool use.
- **Agentes:** loop de tool use próprio, sem frameworks pesados no começo.
- **Agendamento:** APScheduler.
- **Notificações:** Telegram, na Fase 4.

## Consequências

- Python tem o ecossistema mais maduro para IA e dados.
- SQLite não exige servidor, o que reduz atrito na Fase 1. A troca para PostgreSQL na Fase 2 exige que a camada `db` isole o acesso a dados, para a migração não vazar para o resto do código.
- Streamlit permite uma interface útil rápido, ao custo de pouca flexibilidade visual. Aceitável para uso pessoal.
- O loop próprio de tool use dá mais trabalho que um framework, mas ensina o mecanismo e evita abstrações que escondem o que acontece. Se a complexidade crescer, reavaliamos em um novo ADR.
- O Python 3.14 foi evitado no `.venv` porque bibliotecas com extensões nativas costumam demorar a publicar pacotes para versões novas.
- O sistema depende de um serviço externo (API da Claude) e tem custo por uso.

## Alternativas consideradas

- **PostgreSQL desde o início:** mais próximo do alvo, mas adiciona instalação e administração antes de termos algo funcionando.
- **LangChain/LlamaIndex:** aceleram o início, mas escondem o loop de tool use, que é justamente o que queremos aprender.
- **Interface web própria (React etc.):** mais flexível, mas muito mais trabalho para um projeto pessoal.
- **Flask ou Django no lugar de FastAPI:** FastAPI tem validação com pydantic e documentação automática, que combinam com saídas estruturadas de LLM.
