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
        print("Tentando buscar arquivo OFX do S3...")
        s3 = boto3.client('s3')
        
        # Lista os objetos para verificar se o arquivo existe
        try:
            s3.head_object(Bucket='dindin-ofx-files', Key='latest.ofx')
        except Exception as e:
            print(f"Arquivo latest.ofx não encontrado: {str(e)}")
            return None
            
        response = s3.get_object(
            Bucket='dindin-ofx-files',
            Key='latest.ofx'
        )
        content = response['Body'].read().decode('utf-8')
        print(f"Arquivo OFX obtido com sucesso. Tamanho: {len(content)} bytes")
        return content
    except Exception as e:
        print(f"Erro ao buscar arquivo OFX: {str(e)}")
        return None

def format_transaction_response(transactions, period, balance, statistics):
    """
    Formata a resposta da API com transações e informações adicionais.
    """
    try:
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
    except Exception as e:
        print(f"Erro ao formatar resposta: {str(e)}")
        raise

def handler(event, context):
    """
    Handler principal da API de transações.
    Parâmetros suportados via query string:
    - month: Filtra por mês específico (YYYY-MM)
    - category: Filtra por categoria
    - type: Filtra por tipo (CREDIT/DEBIT)
    """
    try:
        print("Iniciando processamento da requisição...")
        
        # Obtém parâmetros da query string
        params = event.get('queryStringParameters', {}) or {}
        month_filter = params.get('month')
        category_filter = params.get('category')
        type_filter = params.get('type')
        
        print(f"Filtros recebidos: month={month_filter}, category={category_filter}, type={type_filter}")

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
                    'message': 'Arquivo OFX não encontrado ou inacessível no S3',
                    'details': 'Verifique se o arquivo latest.ofx existe no bucket dindin-ofx-files'
                })
            }

        # Processa o arquivo OFX
        print("Processando arquivo OFX...")
        ofx_response = ofx_parser({'body': ofx_content}, None)
        if ofx_response['statusCode'] != 200:
            print(f"Erro ao processar OFX: {ofx_response['body']}")
            return ofx_response

        # Obtém os dados processados
        ofx_data = json.loads(ofx_response['body'])
        transactions = ofx_data['transactions']
        print(f"Total de transações encontradas: {len(transactions)}")
        
        # Aplica filtros
        if month_filter:
            transactions = [t for t in transactions if t['date_posted'].startswith(month_filter)]
            print(f"Após filtro de mês: {len(transactions)} transações")
            
        if category_filter:
            transactions = [t for t in transactions if t['suggested_category'] == category_filter]
            print(f"Após filtro de categoria: {len(transactions)} transações")
            
        if type_filter:
            transactions = [t for t in transactions if t['type'] == type_filter]
            print(f"Após filtro de tipo: {len(transactions)} transações")

        # Formata a resposta
        response_data = format_transaction_response(
            transactions=transactions,
            period=ofx_data['period'],
            balance=ofx_data['balance'],
            statistics=ofx_data['statistics']
        )

        print("Processamento concluído com sucesso")
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
                'message': 'Erro ao processar as transações',
                'details': str(e)
            })
        } 