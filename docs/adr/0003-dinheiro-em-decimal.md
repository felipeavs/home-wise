# ADR 0003: Dinheiro em Decimal com 2 casas

- **Status:** Aceito
- **Data:** 2026-11-06

## Contexto

O sistema soma, compara e confere valores em reais. Um dos controles centrais é conferir se a soma dos itens bate com o total da nota. Isso exige aritmética exata. Números de ponto flutuante (`float`) guardam aproximações binárias: `0.1 + 0.2` dá `0.30000000000000004`, e erros assim fariam notas corretas parecerem divergentes.

## Decisão

- Todo valor monetário usa `Decimal` do Python, nunca `float`.
- Todo valor monetário é **arredondado para 2 casas decimais**, com `ROUND_HALF_UP` (0,005 vira 0,01, a regra comum no comércio). O padrão do Python é arredondar para o par mais próximo, que não usamos.
- O arredondamento acontece na entrada, no validador do pydantic (`Money` em `ingestion/schemas.py`). Depois disso, nenhum valor com mais de 2 casas circula no sistema.
- Entradas aceitas: número, texto com ponto ("12.90"), com vírgula ("12,90") ou com "R$". Floats são convertidos via texto para não carregar ruído binário.
- No JSON o valor sai como texto com 2 casas (`"12.90"`), preservando a exatidão.
- A conferência usa tolerância de 1 centavo, porque cupons arredondam linha a linha.
- **Exceção: quantidade.** Itens pesados vêm com 3 casas (0,345 kg). Arredondar para 2 casas distorceria o cálculo `quantidade × preço`. A quantidade usa 3 casas; só dinheiro usa 2.
- Divergência de total **não gera erro**: o item é marcado `needs_review` e vai para a revisão humana.

## Consequências

- Somas e comparações são exatas.
- No banco, o SQLite não tem tipo decimal nativo. Na Fase 1 vamos guardar como texto ou inteiro em centavos internamente, com conversão na camada `db`. A decisão será detalhada ao desenhar o esquema, e some quando migrarmos para PostgreSQL (`NUMERIC(12,2)`).
- Qualquer cálculo novo com dinheiro deve usar `Decimal` e passar por arredondamento antes de ser gravado ou exibido.

## Alternativas consideradas

- **`float`:** simples, mas inexato. Descartado.
- **Inteiro em centavos:** também exato e comum, mas obriga a converter na entrada e na saída em todo lugar, e é mais fácil errar uma conversão. Descartado a favor de `Decimal` por ser mais legível.
