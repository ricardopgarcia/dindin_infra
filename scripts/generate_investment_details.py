import json
import boto3
from datetime import datetime, timedelta
import random
import uuid

def get_random_date(start_year=2020):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def generate_cdb_details(account):
    purchase_date = get_random_date()
    maturity_date = purchase_date + timedelta(days=random.choice([180, 360, 720, 1080]))
    rate = random.uniform(100, 130)
    
    return {
        "account_name": account["name"],
        "account_id": account["id"],
        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
        "maturity_date": maturity_date.strftime("%Y-%m-%d"),
        "rate": f"{rate:.2f}% do CDI",
        "initial_investment": round(account["balance"] * 0.9, 2),
        "current_balance": account["balance"],
        "risk_level": "Baixo",
        "liquidity": "D+1" if "Liquidez" in account["name"] else "Vencimento",
        "institution": next((bank for bank in ["Daycoval", "C6", "Fibra", "Agibank"] if bank.upper() in account["name"].upper()), "Outros")
    }

def generate_stock_details(account):
    purchase_date = get_random_date()
    quantity = round(account["balance"] / random.uniform(10, 30))
    avg_price = round(account["balance"] / quantity, 2)
    
    return {
        "account_name": account["name"],
        "account_id": account["id"],
        "ticker": account["name"],
        "sector": random.choice(["Energia", "Tecnologia", "Financeiro", "Consumo", "Infraestrutura"]),
        "quantity": quantity,
        "average_price": avg_price,
        "current_price": round(account["balance"] / quantity, 2),
        "total_balance": account["balance"],
        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
        "dividend_yield": f"{random.uniform(3, 12):.2f}%"
    }

def generate_fii_details(account):
    purchase_date = get_random_date()
    quantity = round(account["balance"] / random.uniform(50, 100))
    avg_price = round(account["balance"] / quantity, 2)
    
    return {
        "account_name": account["name"],
        "account_id": account["id"],
        "ticker": account["name"],
        "segment": random.choice(["Logística", "Shoppings", "Lajes Corporativas", "Recebíveis", "Fundo de Fundos"]),
        "quantity": quantity,
        "average_price": avg_price,
        "current_price": round(account["balance"] / quantity, 2),
        "total_balance": account["balance"],
        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
        "dividend_yield": f"{random.uniform(6, 14):.2f}%",
        "vacancy_rate": f"{random.uniform(0, 15):.1f}%"
    }

def generate_crypto_details(account):
    purchase_date = get_random_date(2021)
    quantity = round(account["balance"] / random.uniform(1000, 50000), 8)
    avg_price = round(account["balance"] / quantity, 2)
    
    return {
        "account_name": account["name"],
        "account_id": account["id"],
        "token": account["name"],
        "quantity": quantity,
        "average_price": avg_price,
        "current_price": round(account["balance"] / quantity, 2),
        "total_balance": account["balance"],
        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
        "wallet": random.choice(["Binance", "Coinbase", "MetaMask", "Trust Wallet"]),
        "network": random.choice(["BTC", "ETH", "BSC", "Polygon"])
    }

def generate_pension_details(account):
    start_date = get_random_date(2015)
    
    return {
        "account_name": account["name"],
        "account_id": account["id"],
        "plan_type": random.choice(["PGBL", "VGBL"]),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "total_balance": account["balance"],
        "monthly_contribution": round(account["balance"] * 0.02, 2),
        "tax_regime": random.choice(["Progressivo", "Regressivo"]),
        "portfolio_composition": {
            "Renda Fixa": f"{random.uniform(40, 80):.1f}%",
            "Renda Variável": f"{random.uniform(20, 60):.1f}%"
        },
        "institution": random.choice(["Icatu", "Brasilprev", "XP Vida e Previdência"])
    }

def generate_fgts_details(account):
    return {
        "account_name": account["name"],
        "account_id": account["id"],
        "total_balance": account["balance"],
        "birthday_withdrawal": round(account["balance"] * 0.05, 2),
        "annual_yield": "TR + 3% a.a.",
        "next_withdrawal_date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
        "employer": "Atual Empregador",
        "available_for_withdrawal": round(account["balance"] * random.uniform(0.1, 0.3), 2)
    }

def main():
    # Configurar cliente S3
    s3 = boto3.client('s3')
    bucket_name = 'dindin-ofx-files'
    
    # Ler arquivo de contas
    response = s3.get_object(Bucket=bucket_name, Key='accounts.json')
    accounts_data = json.loads(response['Body'].read().decode('utf-8'))
    
    # Adicionar IDs para contas que não têm
    updated = False
    for account in accounts_data['accounts']:
        if 'id' not in account:
            account['id'] = str(uuid.uuid4())
            updated = True
    
    # Se houve atualização, salvar o arquivo accounts.json atualizado
    if updated:
        s3.put_object(
            Bucket=bucket_name,
            Key='accounts.json',
            Body=json.dumps(accounts_data, indent=2, ensure_ascii=False),
            ContentType='application/json'
        )
        print("Updated accounts.json with new IDs")
    
    # Limpar diretório investment_details
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='investment_details/')
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print("Cleaned up old investment details")
    except Exception as e:
        print(f"Warning: Could not clean up old files: {e}")
    
    # Gerar detalhes para cada conta de investimento
    for account in accounts_data['accounts']:
        if account['type'] != 'investimento':
            continue
            
        details = None
        if account['category'] == 'CDBs':
            details = generate_cdb_details(account)
        elif account['category'] == 'Ações':
            details = generate_stock_details(account)
        elif account['category'] == 'FIIs':
            details = generate_fii_details(account)
        elif account['category'] == 'Criptomoedas':
            details = generate_crypto_details(account)
        elif account['category'] == 'Previdência':
            details = generate_pension_details(account)
        elif account['category'] == 'FGTS':
            details = generate_fgts_details(account)
            
        if details:
            # Salvar detalhes no S3 usando o ID como nome do arquivo
            file_name = f"investment_details/{account['id']}.json"
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json.dumps(details, indent=2, ensure_ascii=False),
                ContentType='application/json'
            )
            print(f"Generated details for: {account['name']} (ID: {account['id']})")

if __name__ == "__main__":
    main() 