import json
from datetime import date
from pathlib import Path

import requests

SERIES = {
    "ipca": 433,        # IPCA, variação mensal (%)
    "selic_meta": 432,  # Selic meta (% ao ano)
    "dolar": 1,         # Dólar PTAX, diário
}

PASTA_RAW = Path("data/raw")


def baixar_serie(codigo, inicio, fim):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    params = {"formato": "json", "dataInicial": inicio, "dataFinal": fim}
    resposta = requests.get(url, params=params, timeout=30)
    resposta.raise_for_status()
    return resposta.json()


def main():
    PASTA_RAW.mkdir(parents=True, exist_ok=True)
    hoje = date.today().strftime("%d/%m/%Y")
    for nome, codigo in SERIES.items():
        dados = baixar_serie(codigo, "01/01/2026", hoje)
        arquivo = PASTA_RAW / f"{nome}.json"
        arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{nome}: {len(dados)} registros salvos em {arquivo}")


if __name__ == "__main__":
    main()