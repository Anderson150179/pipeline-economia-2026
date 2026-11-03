# Pipeline Economia 2026

Pipeline de dados com indicadores da economia brasileira em 2026 (inflação, juros e dólar), usando a API pública do Banco Central. Projeto do desafio final do módulo de pipeline de dados da pós-graduação.

## Perguntas que o projeto responde

1. A inflação acumulada de 2026 já estourou o teto da meta (4,5%)?
2. Qual foi o mês de maior inflação do ano, e como estava o dólar naquele mês?
3. Quanto o dólar variou em 2026?
4. Quantas vezes o Banco Central mudou a Selic em 2026, e para que lado?

## Fonte dos dados

Banco Central do Brasil, SGS: séries 433 (IPCA), 432 (Selic meta) e 1 (dólar PTAX). Extraídos em 03/11/2026. Licença ODbL.

## Camadas

| Camada | Pasta | O que tem |
|---|---|---|
| Raw | `data/raw` | JSON exatamente como veio da API, sem alteração |
| Refined | `data/refined` | Datas e valores convertidos, dólar médio por mês e JOIN entre IPCA e dólar pela chave `mes` |
| Marts | `data/marts` | Um indicador por pergunta |

O IPCA é divulgado com cerca de um mês de atraso, então os indicadores de inflação vão até setembro de 2026. O JOIN mantém só os meses que têm IPCA.

## Como rodar

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python src/ingestao.py
python src/transformacao.py
python src/indicadores.py
pytest -v
```

## Resultados (dados até 03/11/2026)

| Pergunta | Resposta |
|---|---|
| Inflação acumulada vs. teto | 3,95% de janeiro a setembro, abaixo do teto de 4,5% |
| Mês de maior inflação | Março (0,88%), com dólar médio de R$ 5,23 |
| Variação do dólar | +1,04% (R$ 5,44 em 02/01 para R$ 5,49 em 03/11) |
| Mudanças na Selic | 5 cortes de 0,25 ponto, de 15% para 13,75% |

## O que eu concluí

Até setembro, a inflação acumulada ficou em 3,95%, abaixo do teto da meta, mas com pouca folga: se o último trimestre somar mais de 0,5 ponto, o teto estoura. Março foi o mês mais pesado, e agosto chegou a ter deflação. O dólar quase não se mexeu no ano, então não parece ter sido ele que puxou a inflação. Com a inflação sob controle, o Banco Central teve espaço para cortar a Selic cinco vezes, de 15% para 13,75%.
