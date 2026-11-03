import pandas as pd

from transformacao import converter_serie, dolar_medio_por_mes, ipca_por_mes, juntar_por_mes


def test_converter_serie_arruma_tipos():
    registros = [{"data": "01/02/2026", "valor": "1.50"}]
    df = converter_serie(registros)
    assert df["data"].iloc[0] == pd.Timestamp("2026-02-01")
    assert df["valor"].iloc[0] == 1.5


def test_dolar_medio_por_mes_calcula_media():
    dolar = pd.DataFrame({
        "data": pd.to_datetime(["2026-01-02", "2026-01-03", "2026-02-02"]),
        "valor": [5.0, 6.0, 4.0],
    })
    resultado = dolar_medio_por_mes(dolar)
    assert resultado["mes"].tolist() == ["2026-01", "2026-02"]
    assert resultado["dolar_medio"].tolist() == [5.5, 4.0]


def test_juntar_por_mes_mantem_so_meses_em_comum():
    ipca = pd.DataFrame({
        "data": pd.to_datetime(["2026-01-01", "2026-02-01"]),
        "valor": [0.5, 0.3],
    })
    dolar = pd.DataFrame({
        "data": pd.to_datetime(["2026-01-05", "2026-03-05"]),
        "valor": [5.0, 5.2],
    })
    resultado = juntar_por_mes(ipca_por_mes(ipca), dolar_medio_por_mes(dolar))
    assert resultado["mes"].tolist() == ["2026-01"]