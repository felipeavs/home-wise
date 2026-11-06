# Documentação de tests/test_schemas.py

Guia do que este arquivo de teste valida. Para cada teste: o que ele prova, com um exemplo de entrada e do resultado esperado. Atualizado sempre que um teste é criado ou alterado.

Como rodar (com o venv ativado):

```powershell
pytest                    # resumo
pytest -v                 # lista cada teste
pytest tests/test_schemas.py   # só um arquivo
pytest -k discount        # só testes cujo nome contém "discount"
```

**Última execução:** 2026-11-06, 12 testes, 12 passaram.

---

## Visão geral

Testa `src/homewise/ingestion/schemas.py`: o contrato dos dados extraídos da nota. Garante que o dinheiro é exato (`Decimal`, 2 casas) e que notas duvidosas são marcadas para revisão. Decisão registrada no [ADR 0003](../../docs/adr/0003-dinheiro-em-decimal.md).

### Dinheiro e números

| Teste | O que prova | Entrada | Resultado esperado |
|---|---|---|---|
| `test_money_is_rounded_to_two_places_half_up` | Arredonda para 2 casas com meio para cima (regra do comércio) | `1.005` e `2.675` | `1.01` e `2.68` |
| `test_money_always_has_two_decimals` | Sempre exibe 2 casas, mesmo para número inteiro | `10` | `"10.00"` |
| `test_brazilian_comma_and_currency_symbol` | Aceita formato brasileiro e o símbolo de real | `"R$ 4,90"` | `4.90` |
| `test_float_input_has_no_binary_noise` | `float` não traz erro binário para dentro do sistema | `0.1`, `0.3` | `0.10`, `0.30` |
| `test_weighed_quantity_keeps_three_decimals` | Item pesado mantém 3 casas na quantidade | `0.345 kg × 39.90` | quantidade `0.345`, linha consistente com `13.77` |

### Regras de validação

| Teste | O que prova | Entrada | Resultado esperado |
|---|---|---|---|
| `test_negative_price_and_zero_quantity_are_rejected` | Valores impossíveis são recusados | preço `-1`; quantidade `0` | erro de validação nos dois casos |
| `test_purchase_requires_at_least_one_item` | Nota sem itens não existe | lista de itens vazia | erro de validação |

### Conferência de totais (a nota vai para revisão ou não)

| Teste | O que prova | Entrada | Resultado esperado |
|---|---|---|---|
| `test_purchase_total_matches` | Soma dos itens igual ao total declarado passa | itens `9.80 + 6.20`, total `16.00` | divergência `0.00`, sem revisão |
| `test_purchase_with_discount` | Desconto entra na conta | itens `16.00`, desconto `1.00`, total `15.00` | bate |
| `test_total_mismatch_flags_review_instead_of_raising` | Total errado não derruba o sistema, só pede revisão | itens `16.00`, total `20.00` | divergência `-4.00`, `needs_review = True` |
| `test_inconsistent_line_flags_review` | Linha em que quantidade × preço não bate pede revisão | `2 × 4.90` mas total da linha `12.00` | `needs_review = True` |

### Serialização

| Teste | O que prova | Entrada | Resultado esperado |
|---|---|---|---|
| `test_json_roundtrip_keeps_two_decimals` | Gravar em JSON e reler não perde nem altera valores | uma compra qualquer | compra relida igual à original; total sai como `"16.00"` |

---

## Como manter este arquivo

Ao criar ou alterar um teste em `tests/test_schemas.py`: atualizar as tabelas deste arquivo e a linha "Última execução". Cada novo `tests/test_xxx.py` ganha o seu `tests/docs/test_xxx.md`.
