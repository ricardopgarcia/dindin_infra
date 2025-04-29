import json
import boto3
import os
import urllib.parse

def handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ.get('INVESTMENTS_BUCKET', 'dindin-ofx-files')
    
    # Extrai o investmentId do path e decodifica
    path_params = event.get('pathParameters') or {}
    investment_id = path_params.get('investmentId')
    if not investment_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'investmentId é obrigatório'})
        }
    
    # Decodifica o ID da URL
    investment_id = urllib.parse.unquote(investment_id)
    key = f'investment_details/{investment_id}.json'
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(data)
        }
    except s3.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Investimento não encontrado'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Erro interno', 'details': str(e)})
        } 