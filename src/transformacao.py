import json
from pathlib import Path

import pandas as pd

PASTA_RAW = Path("data/raw")
PASTA_REFINED = Path("data/refined")


def converter_serie(registros):
    """Transforma a lista do JSON em tabela com data e valor nos tipos certos."""
    df = pd.DataFrame(registros)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = df["valor"].astype(float)
    return df


def ipca_por_mes(df_ipca):
    df = df_ipca.copy()
    df["mes"] = df["data"].dt.strftime("%Y-%m")
    return df[["mes", "valor"]].rename(columns={"valor": "ipca"})


def dolar_medio_por_mes(df_dolar):
    df = df_dolar.copy()
    df["mes"] = df["data"].dt.strftime("%Y-%m")
    media = df.groupby("mes", as_index=False)["valor"].mean()
    media["valor"] = media["valor"].round(4)
    return media.rename(columns={"valor": "dolar_medio"})


def juntar_por_mes(ipca_mes, dolar_mes):
    """JOIN entre IPCA e dólar médio pela chave 'mes'."""
    return ipca_mes.merge(dolar_mes, on="mes", how="inner")


def ler_raw(nome):
    texto = (PASTA_RAW / f"{nome}.json").read_text(encoding="utf-8")
    return json.loads(texto)


def main():
    PASTA_REFINED.mkdir(parents=True, exist_ok=True)

    ipca = converter_serie(ler_raw("ipca"))
    dolar = converter_serie(ler_raw("dolar"))

    dolar.to_csv(PASTA_REFINED / "dolar_diario.csv", index=False)

    economia = juntar_por_mes(ipca_por_mes(ipca), dolar_medio_por_mes(dolar))
    economia.to_csv(PASTA_REFINED / "economia_mensal.csv", index=False)

    print(f"dolar_diario: {len(dolar)} linhas")
    print(f"economia_mensal: {len(economia)} linhas")


if __name__ == "__main__":
    main()