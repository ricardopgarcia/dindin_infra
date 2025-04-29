import json
import boto3
import os
import uuid

def handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ.get('ACCOUNTS_BUCKET', 'dindin-ofx-files')
    key = 'accounts.json'
    
    try:
        # Lê o corpo da requisição
        body = json.loads(event.get('body', '{}'))
        
        # Valida os campos obrigatórios
        required_fields = ['name', 'balance', 'category', 'type']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': f'Campo obrigatório ausente: {field}'
                    })
                }
        
        # Lê o arquivo atual de contas
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        accounts = data.get('accounts', [])
        
        # Cria a nova conta
        new_account = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'balance': float(body['balance']),
            'category': body['category'],
            'type': body['type'],
            'icon': body.get('icon', 'banknote')  # Ícone padrão se não fornecido
        }
        
        # Adiciona a nova conta à lista
        accounts.append(new_account)
        
        # Atualiza o arquivo no S3
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps({'accounts': accounts}, indent=2),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(new_account)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Erro ao criar conta',
                'details': str(e)
            })
        } 