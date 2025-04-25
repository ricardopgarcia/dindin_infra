import json
from datetime import datetime

def handler(event, context):
    # Nome da conta enviada via query string (GET /transactions?account=Conta Corrente)
    account_name = event.get("queryStringParameters", {}).get("account", "")

    # Base fictícia de lançamentos
    lancamentos_db = {
        "Conta Corrente": [
            {"descricao": "Salário", "valor": 5000.0, "data": "2025-04-01"},
            {"descricao": "Supermercado", "valor": -320.0, "data": "2025-04-03"},
            {"descricao": "Farmácia", "valor": -80.0, "data": "2025-04-04"},
            {"descricao": "Transferência Recebida", "valor": 1200.0, "data": "2025-04-15"},
            {"descricao": "Cinema", "valor": -50.0, "data": "2025-04-20"},
            {"descricao": "Conta de Luz", "valor": -180.0, "data": "2025-03-15"},
            {"descricao": "Água", "valor": -90.0, "data": "2025-03-20"},
            {"descricao": "Internet", "valor": -100.0, "data": "2025-02-10"},
            {"descricao": "Seguro Saúde Futuro", "valor": -500.0, "data": "2025-06-01"},
            {"descricao": "Viagem Futuro", "valor": -2000.0, "data": "2025-06-15"}
        ],
        "Cartão Nubank": [
            {"descricao": "Compra Supermercado", "valor": -400.0, "data": "2025-04-05"},
            {"descricao": "Posto de Gasolina", "valor": -150.0, "data": "2025-04-10"},
            {"descricao": "Cinema", "valor": -70.0, "data": "2025-04-15"}
        ]
    }

    # Busca os lançamentos para a conta
    lancamentos = lancamentos_db.get(account_name, [])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(lancamentos)
    } 