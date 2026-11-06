# Dependências do HomeWise

Guia do que cada biblioteca instalada faz e onde ela entra no projeto. Atualizado a cada nova dependência.

Versões instaladas em 2026-11-06, no `.venv` com Python 3.13.14.

---

## Dependências de execução

Declaradas em `[project].dependencies` do `pyproject.toml`.

### anthropic 2.6.0
**O que é:** SDK oficial para chamar a API da Claude pelo Python.
**Para que serve aqui:** é o cérebro do sistema. Lê a foto da nota (visão), extrai os itens, sugere categorias e escreve os pareceres. Também é onde implementamos o loop de tool use: a Claude pede para executar uma função (por exemplo, "some os gastos do mês em Carnes"), nosso código executa no banco e devolve o resultado.
**Exemplo prático:**
```python
import anthropic
client = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do ambiente
resposta = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extraia os itens desta nota: ..."}],
)
```
**Onde entra:** `ingestion/` (Fase 1), `agents/` (Fases 2 a 5).

### pydantic 2.14.3
**O que é:** biblioteca que define a forma dos dados com classes Python e valida automaticamente.
**Para que serve aqui:** o JSON que a Claude devolve da nota é texto. O pydantic transforma esse texto em objetos validados (data é data, preço é número, quantidade não é negativa). Se a Claude devolver lixo, o erro aparece na hora e não no banco.
**Exemplo prático:**
```python
from decimal import Decimal
from pydantic import BaseModel

class Item(BaseModel):
    descricao: str
    quantidade: Decimal
    preco_total: Decimal

Item(descricao="Leite 1L", quantidade="2", preco_total="9.80")  # converte e valida
Item(descricao="Leite 1L", quantidade="abc", preco_total="9.80")  # levanta ValidationError
```
**Onde entra:** `ingestion/` (schema da nota), `api/` (entrada e saída), `db/`.

### pydantic-settings 2.16.2
**O que é:** extensão do pydantic para ler configurações de variáveis de ambiente e do arquivo `.env`.
**Para que serve aqui:** é a base do `config.py`. Em vez de espalhar `os.environ["ANTHROPIC_API_KEY"]` pelo código, existe uma classe `Settings` única, tipada e validada. Se faltar uma chave obrigatória, o programa avisa ao iniciar.
**Exemplo prático:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    anthropic_api_key: str
    homewise_model: str = "claude-sonnet-5-5"
```
**Onde entra:** `config.py`.

### fastapi 0.162.0
**O que é:** framework para criar APIs web em Python.
**Para que serve aqui:** é a camada entre a interface e o resto. O Streamlit não fala direto com o banco nem com a Claude: ele chama endpoints da API ("enviar nota", "listar compras", "confirmar itens"). Isso mantém a regra de negócio fora da tela e permite trocar a interface depois, ou receber mensagens do Telegram pelo mesmo caminho. Gera também uma página de documentação interativa em `/docs`.
**Exemplo prático:**
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/compras")
def listar_compras():
    return [{"loja": "Mercado X", "total": "54.30"}]
```
**Onde entra:** `api/`.

### uvicorn[standard] 0.54.0
**O que é:** servidor que roda a aplicação FastAPI. O `[standard]` inclui extras de desempenho e o recarregamento automático em desenvolvimento.
**Para que serve aqui:** o FastAPI define a API, mas não "liga" sozinho. O uvicorn é quem abre a porta e recebe as requisições.
**Exemplo prático (terminal):**
```powershell
uvicorn homewise.api.main:app --reload   # reinicia ao salvar o arquivo
```
**Onde entra:** execução da `api/`.

### streamlit 1.67.0
**O que é:** biblioteca para montar telas web só com Python, sem HTML, CSS ou JavaScript.
**Para que serve aqui:** é a interface: upload da foto da nota, tela de revisão dos itens antes de salvar, tabela de compras, dashboard, central de alertas e chat.
**Exemplo prático:**
```python
import streamlit as st
foto = st.file_uploader("Foto da nota", type=["jpg", "png"])
if foto:
    st.image(foto)
    st.button("Extrair itens")
```
**Onde entra:** `app/`.

### apscheduler 3.11.3
**O que é:** agendador de tarefas dentro do próprio programa Python (algo como um "cron" interno).
**Para que serve aqui:** dispara rotinas sem você pedir: o parecer diário às 20h, o semanal no domingo, o mensal no dia 1º, verificações periódicas de preço.
**Exemplo prático:**
```python
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
sched.add_job(gerar_parecer_diario, "cron", hour=20)
sched.start()
```
**Onde entra:** Fase 4 (relatórios agendados). Está instalado, mas ainda sem uso.

### python-multipart 0.0.33
**O que é:** biblioteca que o FastAPI usa por baixo para receber formulários e **upload de arquivos**.
**Para que serve aqui:** sem ela, o endpoint que recebe a foto da nota não funciona (o FastAPI recusa subir sem ela). Você quase nunca a importa diretamente.
**Exemplo prático:**
```python
from fastapi import UploadFile

@app.post("/notas")
async def enviar_nota(arquivo: UploadFile):  # só funciona com python-multipart instalado
    conteudo = await arquivo.read()
```
**Onde entra:** `api/` (endpoint de upload).

---

## Dependências de desenvolvimento

Declaradas em `[project.optional-dependencies].dev`. Servem para construir e testar o projeto, não para rodá-lo em uso normal.

### pytest 9.2.0
**O que é:** framework de testes.
**Para que serve aqui:** garante que a lógica de números continua correta. Principal uso: testar que a soma dos itens bate com o total, que o cálculo de variação de preço está certo e que a categorização não regride. Rodar os evals também pode usar pytest.
**Exemplo prático:**
```python
def test_variacao_percentual():
    assert variacao_percentual(antigo=Decimal("10"), novo=Decimal("12")) == Decimal("20")
```
```powershell
pytest            # roda tudo em tests/
```
**Onde entra:** `tests/`.

### ruff 0.17.4
**O que é:** verificador de estilo e erros comuns (linter) e formatador de código, muito rápido.
**Para que serve aqui:** acha import não usado, variável inexistente, linhas fora do padrão de 100 caracteres, e organiza os imports. Pega erros bobos antes de rodar.
**Exemplo prático (terminal):**
```powershell
ruff check .          # aponta problemas
ruff check . --fix    # corrige os que são seguros
ruff format .         # formata o código
```
**Onde entra:** todo o código em `src/`, `app/` e `tests/`.

### httpx 0.28.1
**O que é:** cliente HTTP (faz requisições a APIs).
**Para que serve aqui:** o `TestClient` do FastAPI usa o httpx por baixo para testar os endpoints sem subir um servidor. Também será útil quando o Streamlit precisar chamar a API.
**Exemplo prático:**
```python
from fastapi.testclient import TestClient
client = TestClient(app)
assert client.get("/compras").status_code == 200
```
**Onde entra:** `tests/` (e possivelmente `app/`).

---

## Pacote do próprio projeto

### homewise 0.1.0
É o código em `src/homewise/`, instalado em **modo editável** (`pip install -e`). Isso faz `import homewise` funcionar em qualquer lugar do ambiente, e as mudanças no código valem na hora, sem reinstalar.

---

## Previstas para as próximas fases (ainda não instaladas)

| Biblioteca | Fase | Para quê |
|---|---|---|
| PostgreSQL driver (psycopg) | 2 | Conectar ao PostgreSQL |
| pgvector (Python) | 2 | Guardar e buscar embeddings |
| Biblioteca de embeddings | 2 | Gerar os vetores dos produtos |
| Leitor de QR code | 1 (a avaliar) | Ler o QR code da NFC-e |
| python-telegram-bot ou similar | 4 | Notificações por Telegram |

---

## Como manter este arquivo

Ao instalar qualquer dependência nova: adicionar a entrada acima (o que é, para que serve aqui, exemplo, onde entra), mover da tabela "previstas" se estiver lá, e atualizar a data das versões.
