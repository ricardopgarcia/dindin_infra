import json
from datetime import datetime

def handler(event, context):
    transactions = [
        {
            "id": "1",
            "description": "Salário",
            "amount": 5000.00,
            "date": "2024-04-25",
            "type": "income",
            "category": "Salário",
            "account": "Conta Corrente"
        },
        {
            "id": "2",
            "description": "Aluguel",
            "amount": -1500.00,
            "date": "2024-04-20",
            "type": "expense",
            "category": "Moradia",
            "account": "Conta Corrente"
        },
        {
            "id": "3",
            "description": "Supermercado",
            "amount": -350.00,
            "date": "2024-04-22",
            "type": "expense",
            "category": "Alimentação",
            "account": "Cartão Nubank"
        },
        {
            "id": "4",
            "description": "Freelance",
            "amount": 1200.00,
            "date": "2024-04-23",
            "type": "income",
            "category": "Trabalho",
            "account": "Conta PJ"
        }
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(transactions)
    } 