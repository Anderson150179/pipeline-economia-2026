import pandas as pd

from indicadores import inflacao_acumulada, mudancas_selic, ranking_inflacao, variacao_dolar


def test_inflacao_acumulada_e_composta_e_nao_soma():
    economia = pd.DataFrame({"mes": ["2026-01", "2026-02"], "ipca": [1.0, 1.0]})
    resultado = inflacao_acumulada(economia)
    assert resultado["inflacao_acumulada"].iloc[0] == 2.01
    assert not resultado["estourou_teto"].iloc[0]


def test_inflacao_acumulada_detecta_estouro_do_teto():
    economia = pd.DataFrame({"mes": ["2026-01", "2026-02"], "ipca": [3.0, 3.0]})
    resultado = inflacao_acumulada(economia)
    assert resultado["estourou_teto"].iloc[0]


def test_ranking_coloca_maior_inflacao_em_primeiro():
    economia = pd.DataFrame({
        "mes": ["2026-01", "2026-02", "2026-03"],
        "ipca": [0.2, 0.9, -0.1],
        "dolar_medio": [5.0, 5.1, 5.2],
    })
    resultado = ranking_inflacao(economia)
    assert resultado["mes"].iloc[0] == "2026-02"
    assert resultado["posicao"].tolist() == [1, 2, 3]


def test_variacao_dolar_compara_primeiro_e_ultimo_dia():
    dolar = pd.DataFrame({
        "data": pd.to_datetime(["2026-03-01", "2026-01-01", "2026-02-01"]),
        "valor": [5.5, 5.0, 4.0],
    })
    resultado = variacao_dolar(dolar)
    assert resultado["variacao_pct"].iloc[0] == 10.0


def test_mudancas_selic_identifica_subida_e_descida():
    selic = pd.DataFrame({
        "data": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]),
        "valor": [15.0, 15.0, 14.75, 14.75, 15.0],
    })
    resultado = mudancas_selic(selic)
    assert len(resultado) == 2
    assert resultado["direcao"].tolist() == ["desceu", "subiu"]