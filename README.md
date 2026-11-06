# HomeWise

> **Our home, our responsibilities.**

Sistema AI-first de controle de gastos do lar. Transforma fotos de notas fiscais em dados estruturados, acompanha o histórico de preços, avisa sobre aumentos e compras fora do padrão e ajuda a economizar e reduzir desperdício.

Projeto pessoal, com dois objetivos: resolver um problema real de orçamento doméstico e aprender desenvolvimento AI-first na prática.

## Status

Em fundação. Ainda não há código de aplicação. Veja o [roadmap](docs/03-roadmap.md).

## Documentação

- [Visão](docs/00-visao.md): problema, objetivos e escopo
- [Arquitetura](docs/01-arquitetura.md): componentes e responsabilidades
- [Roadmap](docs/03-roadmap.md): fases do projeto
- [ADRs](docs/adr/): decisões de arquitetura

## Stack

Python 3.11+, FastAPI, SQLite (depois PostgreSQL + pgvector), Streamlit, API da Claude (visão + tool use), APScheduler. Detalhes no [ADR 0001](docs/adr/0001-stack-inicial.md).

## Como preparar o ambiente (Windows / PowerShell)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env   # depois preencha as chaves no .env
```

## Segurança

Dados financeiros, bancos locais (`data/`, `*.db`), notas reais (`evals/notas_reais/`) e chaves (`.env`) **nunca** vão para o Git.

## Licença

MIT. Veja [LICENSE](LICENSE).
