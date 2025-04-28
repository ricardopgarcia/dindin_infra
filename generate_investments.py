import json
import random
from datetime import datetime, timedelta
import os
import re

def slugify(text):
    # Remove caracteres especiais e converte para minúsculas
    text = text.lower()
    text = re.sub(r'[áàãâä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòõôö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def generate_chart_data(start_date, end_date, initial_value, volatility=0.02):
    data = []
    current_date = start_date
    current_value = initial_value
    
    while current_date <= end_date:
        data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "value": round(current_value, 2)
        })
        # Simula variação de preço
        change = random.uniform(-volatility, volatility)
        current_value *= (1 + change)
        current_date += timedelta(days=30)
    
    return data

def generate_transactions(chart_data):
    transactions = []
    for i, data_point in enumerate(chart_data):
        if i == 0:
            transactions.append({
                "id": str(i + 1),
                "description": "Aplicação Inicial",
                "date": data_point["date"],
                "value": data_point["value"]
            })
        else:
            transactions.append({
                "id": str(i + 1),
                "description": "Rendimento Mensal",
                "date": data_point["date"],
                "value": round(data_point["value"] - chart_data[i-1]["value"], 2)
            })
    return transactions

def create_investment_data(name, category, initial_balance, annual_return, liquidity, maturity_date=None):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 4, 1)
    
    chart_data = generate_chart_data(start_date, end_date, initial_balance)
    transactions = generate_transactions(chart_data)
    
    current_balance = chart_data[-1]["value"]
    total_profitability = round((current_balance - initial_balance) / initial_balance * 100, 1)
    
    investment_data = {
        "id": slugify(name),
        "name": name,
        "type": "investimento",
        "category": category,
        "currentBalance": round(current_balance, 2),
        "initialInvestment": initial_balance,
        "totalProfitability": total_profitability,
        "annualProfitability": annual_return,
        "liquidity": liquidity,
        "chartData": chart_data,
        "transactions": transactions
    }
    
    if maturity_date:
        investment_data["maturityDate"] = maturity_date
    
    return investment_data

# Lista de investimentos para gerar
investments = [
    {
        "name": "CDB C6 Pre 14",
        "category": "CDBs",
        "initial_balance": 4000.0,
        "annual_return": 14.0,
        "liquidity": "D+0",
        "maturity_date": "2025-04-25"
    },
    {
        "name": "CDB Inter Pos 100 CDI",
        "category": "CDBs",
        "initial_balance": 1500.0,
        "annual_return": 11.5,
        "liquidity": "D+0",
        "maturity_date": "2025-04-25"
    },
    {
        "name": "LCA BB 97 CDI",
        "category": "LCAs",
        "initial_balance": 1000.0,
        "annual_return": 11.2,
        "liquidity": "D+0",
        "maturity_date": "2025-04-25"
    },
    {
        "name": "LCI Santander 96 CDI",
        "category": "LCIs",
        "initial_balance": 800.0,
        "annual_return": 11.0,
        "liquidity": "D+0",
        "maturity_date": "2025-04-25"
    },
    {
        "name": "XP RF Credito Privado",
        "category": "Fundos de Renda Fixa",
        "initial_balance": 5000.0,
        "annual_return": 12.0,
        "liquidity": "D+1"
    },
    {
        "name": "Itau RF Simples",
        "category": "Fundos de Renda Fixa",
        "initial_balance": 4200.0,
        "annual_return": 11.8,
        "liquidity": "D+1"
    },
    {
        "name": "XP Selection Multimercado",
        "category": "Fundos de Renda Variável",
        "initial_balance": 3800.0,
        "annual_return": 15.0,
        "liquidity": "D+2"
    },
    {
        "name": "Itau Multiestrategia",
        "category": "Fundos de Renda Variável",
        "initial_balance": 2700.0,
        "annual_return": 14.5,
        "liquidity": "D+2"
    },
    {
        "name": "PETR4",
        "category": "Ações",
        "initial_balance": 2100.0,
        "annual_return": 13.0,
        "liquidity": "D+2"
    },
    {
        "name": "WEGE3",
        "category": "Ações",
        "initial_balance": 1900.0,
        "annual_return": 12.8,
        "liquidity": "D+2"
    },
    {
        "name": "HGLG11",
        "category": "FIIs",
        "initial_balance": 3500.0,
        "annual_return": 10.5,
        "liquidity": "D+2"
    },
    {
        "name": "KNRI11",
        "category": "FIIs",
        "initial_balance": 2800.0,
        "annual_return": 10.2,
        "liquidity": "D+2"
    }
]

# Criar diretório temporário para os arquivos
os.makedirs("temp_investments", exist_ok=True)

# Gerar arquivos JSON para cada investimento
for investment in investments:
    data = create_investment_data(**investment)
    filename = f"temp_investments/{data['id']}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Arquivo gerado: {filename}")

print("\nArquivos gerados com sucesso! Agora você pode fazer upload para o S3.") 