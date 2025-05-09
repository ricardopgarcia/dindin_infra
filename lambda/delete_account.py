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
        
        # Remove a conta
        deleted_account = accounts.pop(account_index)
        
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
            'body': json.dumps(deleted_account)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Erro ao deletar conta',
                'details': str(e)
            })
        } 