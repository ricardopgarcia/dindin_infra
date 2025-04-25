import json

def handler(event, context):
    accounts = [
    {
        "icon": "wallet.pass",
        "name": "Dinheiro em Espécie",
        "balance": 1000.0,
        "category": "Espécie",
        "type": "investimento"
    },
    {
        "icon": "banknote",
        "name": "Conta Corrente",
        "balance": 2500.0,
        "category": "Contas",
        "type": "conta"
    },
    {
        "icon": "briefcase",
        "name": "Conta PJ",
        "balance": 3202.8,
        "category": "Contas",
        "type": "conta"
    },
    {
        "icon": "creditcard",
        "name": "Cartão Nubank",
        "balance": 750.0,
        "category": "Cartões",
        "type": "cartao"
    },
    {
        "icon": "chart.line.uptrend.xyaxis",
        "name": "CDB C6 Pré 14%",
        "balance": 4000.0,
        "category": "CDBs",
        "type": "investimento"
    },
    {
        "icon": "chart.line.uptrend.xyaxis",
        "name": "CDB Inter Pós 100% CDI",
        "balance": 1500.0,
        "category": "CDBs",
        "type": "investimento"
    },
    {
        "icon": "chart.line.uptrend.xyaxis",
        "name": "LCA Banco do Brasil 97% CDI",
        "balance": 1000.0,
        "category": "LCAs",
        "type": "investimento"
    },
    {
        "icon": "chart.line.uptrend.xyaxis",
        "name": "LCI Santander 96% CDI",
        "balance": 800.0,
        "category": "LCIs",
        "type": "investimento"
    },
    {
        "icon": "rectangle.stack",
        "name": "XP RF Crédito Privado",
        "balance": 5000.0,
        "category": "Fundos de Renda Fixa",
        "type": "investimento"
    },
    {
        "icon": "rectangle.stack",
        "name": "Itaú RF Simples",
        "balance": 4200.0,
        "category": "Fundos de Renda Fixa",
        "type": "investimento"
    },
    {
        "icon": "rectangle.stack.fill.badge.plus",
        "name": "XP Selection Multimercado",
        "balance": 3800.0,
        "category": "Fundos de Renda Variável",
        "type": "investimento"
    },
    {
        "icon": "rectangle.stack.fill.badge.plus",
        "name": "Itaú Multiestratégia",
        "balance": 2700.0,
        "category": "Fundos de Renda Variável",
        "type": "investimento"
    },
    {
        "icon": "chart.bar",
        "name": "PETR4",
        "balance": 2100.0,
        "category": "Ações",
        "type": "investimento"
    },
    {
        "icon": "chart.bar",
        "name": "ITUB4",
        "balance": 1300.0,
        "category": "Ações",
        "type": "investimento"
    },
    {
        "icon": "chart.bar",
        "name": "WEGE3",
        "balance": 1900.0,
        "category": "Ações",
        "type": "investimento"
    },
    {
        "icon": "building.2",
        "name": "HGLG11",
        "balance": 3500.0,
        "category": "FIIs",
        "type": "investimento"
    },
    {
        "icon": "building.2",
        "name": "KNRI11",
        "balance": 2800.0,
        "category": "FIIs",
        "type": "investimento"
    },
    {
        "icon": "bitcoinsign.circle",
        "name": "Criptomoedas",
        "balance": 0.0,
        "category": "Criptomoedas",
        "type": "investimento"
    }
]




    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(accounts)
    } 