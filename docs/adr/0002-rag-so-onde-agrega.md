# ADR 0002: RAG só onde agrega

- **Status:** Aceito
- **Data:** 2026-11-06

## Contexto

RAG (busca por embeddings para dar contexto ao LLM) é uma técnica popular, e há a tentação de aplicá-lo em tudo. Mas a maior parte dos dados deste sistema é estruturada (compras, itens, preços, orçamentos), e para dados estruturados SQL é mais preciso, mais barato e verificável. Busca por similaridade devolve resultados aproximados, e erro aproximado em número de dinheiro não é aceitável.

## Decisão

Usar RAG apenas onde a busca por significado resolve algo que SQL não resolve:

1. **Normalização de produtos:** "LEITE INT PIRACANJUBA 1L", "Leite Integral 1 litro" e "LT UHT INTEGRAL" devem ser reconhecidos como o mesmo produto.
2. **Base de conhecimento:** textos de apoio (dicas de economia, validade e conservação, substituições).
3. **Memória do lar:** preferências e fatos do lar descritos em texto (marcas preferidas, restrições alimentares).

Não usar RAG para: somas, médias, variações de preço, comparação com orçamento, histórico de compras e qualquer número. Isso vem de SQL ou código, e o LLM só recebe o resultado pronto.

## Consequências

- A busca vetorial entra na Fase 2, quando os produtos precisam ser normalizados. Antes disso não há necessidade.
- pgvector só será necessário a partir da Fase 2 (ver [ADR 0001](0001-stack-inicial.md)).
- Os números dos relatórios e alertas são verificáveis, pois vêm de consultas.
- Cada novo uso de RAG precisa justificar por que SQL não basta. Se não houver justificativa, não se usa.
- A normalização por embeddings pode errar. Por isso entra nos evals, e casos de baixa confiança vão para revisão humana.

## Alternativas consideradas

- **RAG sobre todo o histórico de compras (para o chat):** descartado. Perguntas como "quanto gastei com carne?" são consultas SQL expostas ao LLM como tools, o que dá resposta exata.
- **Normalização só com regras e dicionários:** simples e determinística, mas frágil diante da variedade de abreviações nas notas. Pode ser usada como primeira passada antes dos embeddings.
- **Pedir ao LLM para normalizar sem busca:** inconsistente entre chamadas, pois o mesmo produto pode receber nomes diferentes.
