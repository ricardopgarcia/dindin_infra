import json
import re
from datetime import datetime

def parse_ofx_date(date_str):
    # Remove timezone information and convert to YYYY-MM-DD
    date_str = date_str.split('[')[0]
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

def parse_ofx_amount(amount_str):
    # Convert string amount to float
    return float(amount_str)

def extract_tag_content(content, tag):
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None

def handler(event, context):
    try:
        # Get the OFX content from the request body
        ofx_content = event.get('body', '')
        
        if not ofx_content:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'No OFX content provided'})
            }

        # Extract account information
        bank_id = extract_tag_content(ofx_content, 'BANKID')
        account_id = extract_tag_content(ofx_content, 'ACCTID')
        account_type = extract_tag_content(ofx_content, 'ACCTTYPE')

        # Extract period information
        start_date = extract_tag_content(ofx_content, 'DTSTART')
        end_date = extract_tag_content(ofx_content, 'DTEND')

        # Extract balance information
        balance_amount = extract_tag_content(ofx_content, 'BALAMT')
        balance_date = extract_tag_content(ofx_content, 'DTASOF')

        # Extract all transactions
        transactions = []
        # Modified pattern to handle multiline content
        transaction_blocks = re.findall(r'<STMTTRN>[\s\S]*?</STMTTRN>', ofx_content)
        
        for block in transaction_blocks:
            trn_type = extract_tag_content(block, 'TRNTYPE')
            dt_posted = extract_tag_content(block, 'DTPOSTED')
            trn_amt = extract_tag_content(block, 'TRNAMT')
            fit_id = extract_tag_content(block, 'FITID')
            check_num = extract_tag_content(block, 'CHECKNUM')
            memo = extract_tag_content(block, 'MEMO')

            if all([trn_type, dt_posted, trn_amt, fit_id, check_num, memo]):
                transactions.append({
                    'id': fit_id,
                    'type': trn_type,
                    'date': parse_ofx_date(dt_posted),
                    'amount': parse_ofx_amount(trn_amt),
                    'description': memo.strip(),
                    'documentNumber': check_num
                })

        # Build the response structure
        response = {
            'account': {
                'bank': bank_id,
                'accountNumber': account_id,
                'type': account_type
            },
            'period': {
                'startDate': parse_ofx_date(start_date) if start_date else None,
                'endDate': parse_ofx_date(end_date) if end_date else None
            },
            'transactions': transactions,
            'balance': {
                'amount': parse_ofx_amount(balance_amount) if balance_amount else None,
                'date': parse_ofx_date(balance_date) if balance_date else None
            }
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        } 