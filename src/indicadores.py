from pathlib import Path

import pandas as pd

PASTA_REFINED = Path("data/refined")
PASTA_MARTS = Path("data/marts")

TETO_META_2026 = 4.5  # meta de 3% + 1,5 ponto de tolerância


def inflacao_acumulada(economia):
    """Pergunta 1: a inflação acumulada de 2026 já estourou o teto da meta?"""
    fatores = 1 + economia["ipca"] / 100
    acumulada = round((fatores.prod() - 1) * 100, 2)
    return pd.DataFrame([{
        "primeiro_mes": economia["mes"].min(),
        "ultimo_mes": economia["mes"].max(),
        "inflacao_acumulada": acumulada,
        "teto_meta": TETO_META_2026,
        "estourou_teto": acumulada > TETO_META_2026,
    }])


def ranking_inflacao(economia):
    """Pergunta 2: qual foi o mês de maior inflação (e o dólar naquele mês)?"""
    ranking = economia.sort_values("ipca", ascending=False).reset_index(drop=True)
    ranking.insert(0, "posicao", range(1, len(ranking) + 1))
    return ranking


def variacao_dolar(dolar):
    """Pergunta 3: quanto o dólar variou em 2026?"""
    dolar = dolar.sort_values("data")
    primeiro = dolar.iloc[0]
    ultimo = dolar.iloc[-1]
    variacao = round((ultimo["valor"] / primeiro["valor"] - 1) * 100, 2)
    return pd.DataFrame([{
        "data_inicial": primeiro["data"],
        "dolar_inicial": primeiro["valor"],
        "data_final": ultimo["data"],
        "dolar_final": ultimo["valor"],
        "variacao_pct": variacao,
    }])


def mudancas_selic(selic):
    """Pergunta 4: quantas vezes o BC mudou a Selic, e para que lado?"""
    df = selic.sort_values("data").copy()
    df["selic_anterior"] = df["valor"].shift(1)
    mudou = df[df["selic_anterior"].notna() & (df["valor"] != df["selic_anterior"])].copy()
    mudou["direcao"] = (mudou["valor"] > mudou["selic_anterior"]).map({True: "subiu", False: "desceu"})
    mudou = mudou.rename(columns={"valor": "selic_nova"})
    return mudou[["data", "selic_anterior", "selic_nova", "direcao"]].reset_index(drop=True)


def main():
    PASTA_MARTS.mkdir(parents=True, exist_ok=True)

    economia = pd.read_csv(PASTA_REFINED / "economia_mensal.csv")
    dolar = pd.read_csv(PASTA_REFINED / "dolar_diario.csv", parse_dates=["data"])
    selic = pd.read_csv(PASTA_REFINED / "selic_diaria.csv", parse_dates=["data"])

    resultados = {
        "inflacao_vs_meta": inflacao_acumulada(economia),
        "ranking_inflacao_mensal": ranking_inflacao(economia),
        "variacao_dolar": variacao_dolar(dolar),
        "mudancas_selic": mudancas_selic(selic),
    }

    for nome, tabela in resultados.items():
        tabela.to_csv(PASTA_MARTS / f"{nome}.csv", index=False)
        print(f"\n== {nome} ==")
        print(tabela.to_string(index=False))


if __name__ == "__main__":
    main()