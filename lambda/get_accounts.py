import json
import boto3

def get_accounts(event, context):
    try:
        # Lê o arquivo de contas do S3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket='dindin-ofx-files', Key='accounts.json')
        accounts_data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Filtra por titular se especificado
        titular = event.get('queryStringParameters', {}).get('titular')
        if titular:
            if titular not in ['ricardo', 'priscila']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Campo titular deve ser "ricardo" ou "priscila"'
                    })
                }
            accounts_data['accounts'] = [
                account for account in accounts_data['accounts']
                if account.get('titular') == titular
            ]
        
        return {
            'statusCode': 200,
            'body': json.dumps(accounts_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 