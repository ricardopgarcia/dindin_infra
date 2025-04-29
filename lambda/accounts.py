import json
import boto3
import os

def handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ.get('ACCOUNTS_BUCKET', 'dindin-ofx-files')
    key = 'accounts.json'
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        accounts = data.get('accounts', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(accounts)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro ao carregar contas', 'details': str(e)})
        } 