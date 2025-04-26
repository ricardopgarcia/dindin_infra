import json
import boto3
from datetime import datetime
from ofx_parser import handler as ofx_parser

def get_latest_ofx_content():
    """
    Busca o conteúdo OFX mais recente do S3.
    No futuro, isso pode ser parametrizado por conta/banco.
    """
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(
            Bucket='dindin-ofx-files',
            Key='latest.ofx'
        )
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Erro ao buscar arquivo OFX: {str(e)}")
        return None

def format_transaction_response(transactions, period, balance, statistics):
    """
    Formata a resposta da API com transações e informações adicionais.
    """
    # Agrupa transações por mês
    transactions_by_month = {}
    for transaction in transactions:
        month = transaction['date_posted'][:7]  # YYYY-MM
        if month not in transactions_by_month:
            transactions_by_month[month] = []
        transactions_by_month[month].append(transaction)

    return {
        'summary': {
            'period': period,
            'balance': balance,
            'total_transactions': len(transactions),
            'total_credit': statistics['total_creditos'],
            'total_debit': statistics['total_debitos'],
            'net_balance': statistics['total_creditos'] - statistics['total_debitos']
        },
        'transactions_by_month': transactions_by_month,
        'statistics': {
            'by_category': statistics['por_categoria'],
            'by_month': statistics['por_mes'],
            'largest_transactions': {
                'credit': statistics['maior_credito'],
                'debit': statistics['maior_debito']
            },
            'averages': {
                'credit': statistics['media_creditos'],
                'debit': statistics['media_debitos']
            }
        }
    }

def handler(event, context):
    """
    Handler principal da API de transações.
    Parâmetros suportados via query string:
    - month: Filtra por mês específico (YYYY-MM)
    - category: Filtra por categoria
    - type: Filtra por tipo (CREDIT/DEBIT)
    """
    try:
        # Obtém parâmetros da query string
        params = event.get('queryStringParameters', {}) or {}
        month_filter = params.get('month')
        category_filter = params.get('category')
        type_filter = params.get('type')

        # Busca dados OFX
        ofx_content = get_latest_ofx_content()
        if not ofx_content:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Erro ao buscar dados OFX',
                    'message': 'Não foi possível obter os dados das transações'
                })
            }

        # Processa o arquivo OFX
        ofx_response = ofx_parser({'body': ofx_content}, None)
        if ofx_response['statusCode'] != 200:
            return ofx_response

        # Obtém os dados processados
        ofx_data = json.loads(ofx_response['body'])
        transactions = ofx_data['transactions']
        
        # Aplica filtros
        if month_filter:
            transactions = [t for t in transactions if t['date_posted'].startswith(month_filter)]
        if category_filter:
            transactions = [t for t in transactions if t['suggested_category'] == category_filter]
        if type_filter:
            transactions = [t for t in transactions if t['type'] == type_filter]

        # Formata a resposta
        response_data = format_transaction_response(
            transactions=transactions,
            period=ofx_data['period'],
            balance=ofx_data['balance'],
            statistics=ofx_data['statistics']
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data)
        }

    except Exception as e:
        print(f"Erro ao processar transações: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Erro interno',
                'message': str(e)
            })
        } 