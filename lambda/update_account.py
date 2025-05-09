import json
import boto3
import os

def handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ.get('ACCOUNTS_BUCKET', 'dindin-ofx-files')
    key = 'accounts.json'
    
    try:
        # Obtém o ID da conta da URL
        account_id = event.get('pathParameters', {}).get('id')
        if not account_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'ID da conta não fornecido'
                })
            }
        
        # Lê o corpo da requisição
        body = json.loads(event.get('body', '{}'))
        
        # Valida o campo titular
        if 'titular' in body:
            titular = body['titular'].lower()
            if titular not in ['ricardo', 'priscila']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Campo titular deve ser "ricardo" ou "priscila"'
                    })
                }
            body['titular'] = titular
        
        # Lê o arquivo atual de contas
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        accounts = data.get('accounts', [])
        
        # Procura a conta pelo ID
        account_index = next((i for i, acc in enumerate(accounts) if acc['id'] == account_id), None)
        if account_index is None:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Conta não encontrada'
                })
            }
        
        # Atualiza os campos da conta
        current_account = accounts[account_index]
        updated_account = {
            'id': current_account['id'],  # Mantém o ID original
            'name': body.get('name', current_account['name']),
            'balance': float(body.get('balance', current_account['balance'])),
            'category': body.get('category', current_account['category']),
            'type': body.get('type', current_account['type']),
            'icon': body.get('icon', current_account['icon']),
            'titular': body.get('titular', current_account['titular'])
        }
        
        # Atualiza a conta na lista
        accounts[account_index] = updated_account
        
        # Atualiza o arquivo no S3
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps({'accounts': accounts}, indent=2),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(updated_account)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Erro ao atualizar conta',
                'details': str(e)
            })
        } 