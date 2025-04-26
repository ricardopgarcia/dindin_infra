import json
import re
from datetime import datetime

def parse_amount(amount_str):
    """
    Converte string de valor OFX para float.
    Retorna None se amount_str for None ou inválido.
    """
    if not amount_str:
        return None
    try:
        return float(amount_str.replace(',', ''))
    except (ValueError, AttributeError):
        return None

def parse_date(date_str):
    """
    Converte string de data OFX para formato ISO.
    Datas OFX são tipicamente no formato YYYYMMDDHHMMSS.
    Retorna None se date_str for None ou inválido.
    """
    if not date_str:
        return None
    try:
        # Remove informação de timezone se presente
        date_str = date_str.split('[')[0]
        # Lida com datas com ou sem componente de tempo
        if len(date_str) >= 14:
            return datetime.strptime(date_str[:14], '%Y%m%d%H%M%S').isoformat()
        elif len(date_str) >= 8:
            return datetime.strptime(date_str[:8], '%Y%m%d').isoformat()
        return None
    except (ValueError, AttributeError):
        return None

def parse_ofx_date(date_str):
    """
    Remove informação de timezone e converte para YYYY-MM-DD
    """
    date_str = date_str.split('[')[0]
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

def parse_ofx_amount(amount_str):
    """
    Converte string de valor para float
    """
    return float(amount_str)

def extract_parent_tag_content(content, tag_name):
    """
    Extrai conteúdo entre tags pai de abertura e fechamento.
    """
    try:
        if not content or not tag_name:
            return None

        # Tenta encontrar conteúdo entre tags de abertura e fechamento
        pattern = f'<{tag_name}>(.*?)</{tag_name}>'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # Tenta encontrar conteúdo após uma tag auto-fechada
        pattern = f'<{tag_name}>(.*?)(?=<|$)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        return match.group(1).strip() if match else None
    except Exception as e:
        print(f"Erro ao extrair tag pai {tag_name}: {str(e)}")
        return None

def extract_tag_content(content, tag_name):
    """
    Extrai conteúdo para uma tag específica, lidando com tags auto-fechadas e tags pai.
    """
    try:
        if not content or not tag_name:
            return None

        # Tenta encontrar conteúdo entre tags de abertura e fechamento
        pattern = f'<{tag_name}>(.*?)</{tag_name}>'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # Tenta encontrar conteúdo após uma tag auto-fechada
        pattern = f'<{tag_name}>(.*?)(?=<|$)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # Se não encontrado, tenta procurar em tags pai específicas
        parent_tags = ['BANKACCTFROM', 'LEDGERBAL', 'BANKTRANLIST']
        for parent_tag in parent_tags:
            parent_content = extract_parent_tag_content(content, parent_tag)
            if parent_content:
                # Tenta encontrar a tag dentro do conteúdo pai
                pattern = f'<{tag_name}>(.*?)(?=<|$)'
                match = re.search(pattern, parent_content, re.DOTALL | re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return None
    except Exception as e:
        print(f"Erro ao extrair tag {tag_name}: {str(e)}")
        return None

def extract_transactions(content):
    """
    Extrai transações da seção BANKTRANLIST.
    """
    try:
        transactions = []
        
        if not content:
            print("Conteúdo vazio ao extrair transações")
            return transactions

        # Obtém conteúdo do BANKTRANLIST
        banktranlist = extract_parent_tag_content(content, 'BANKTRANLIST')
        if not banktranlist:
            print("BANKTRANLIST não encontrado")
            return transactions

        # Encontra todas as seções STMTTRN
        pattern = '<STMTTRN>(.*?)</STMTTRN>'
        matches = re.finditer(pattern, banktranlist, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            try:
                trn_content = match.group(1)
                
                # Extrai detalhes da transação
                transaction = {
                    'type': extract_tag_content(trn_content, 'TRNTYPE'),
                    'date_posted': extract_tag_content(trn_content, 'DTPOSTED'),
                    'amount': extract_tag_content(trn_content, 'TRNAMT'),
                    'fitid': extract_tag_content(trn_content, 'FITID'),
                    'name': extract_tag_content(trn_content, 'NAME'),
                    'memo': extract_tag_content(trn_content, 'MEMO'),
                    'check_number': extract_tag_content(trn_content, 'CHECKNUM')
                }
                
                # Converte o valor para float apenas se existir
                if transaction['amount']:
                    transaction['amount'] = parse_ofx_amount(transaction['amount'])
                
                # Remove valores None
                transaction = {k: v for k, v in transaction.items() if v is not None}
                
                # Formata a data para ISO
                if 'date_posted' in transaction:
                    transaction['date_posted'] = parse_date(transaction['date_posted'])
                
                transactions.append(transaction)
            except Exception as e:
                print(f"Erro ao processar transação individual: {str(e)}")
                continue
        
        return transactions
    except Exception as e:
        print(f"Erro ao extrair transações: {str(e)}")
        return []

def suggest_category(transaction):
    """
    Sugere uma categoria com base no memo e tipo da transação.
    """
    memo = transaction.get('memo', '').upper()
    trntype = transaction.get('type', '').upper()
    amount = transaction.get('amount', 0)

    # Categorias de receita
    if trntype == 'CREDIT':
        if 'FOLHA PAGAMENTO' in memo:
            return 'Salário'
        elif 'FERIAS' in memo:
            return 'Férias'
        elif 'PARTICIPACAO' in memo:
            return 'Participação nos Lucros'
        elif 'JUROS POUPANCA' in memo or 'REMUNER BAS POUP' in memo:
            return 'Rendimentos'
        elif 'PIX' in memo or 'TED' in memo or 'DOC' in memo:
            return 'Transferência Recebida'
        else:
            return 'Outras Receitas'
    
    # Categorias de despesa
    else:
        if 'CARTAO' in memo:
            return 'Cartão de Crédito'
        elif 'TELEFONICA' in memo or 'VIVO' in memo:
            return 'Telefonia'
        elif 'DDA' in memo or 'TITULO' in memo or 'BOLETO' in memo:
            return 'Contas e Boletos'
        elif 'PIX' in memo or 'TED' in memo or 'DOC' in memo:
            return 'Transferência Enviada'
        elif 'COMPRA' in memo:
            return 'Compras'
        else:
            return 'Outras Despesas'

def analyze_transactions(transactions):
    """
    Realiza análise estatística das transações.
    """
    # Inicializa contadores
    stats = {
        'total_creditos': 0,
        'total_debitos': 0,
        'count_creditos': 0,
        'count_debitos': 0,
        'maior_credito': 0,
        'maior_debito': 0,
        'por_categoria': {},
        'por_mes': {}
    }
    
    for transaction in transactions:
        amount = transaction.get('amount', 0)
        category = transaction.get('suggested_category', 'Não Categorizado')
        date = transaction.get('date_posted', '')[:7]  # Pega só ano e mês
        
        # Atualiza totais por categoria
        if category not in stats['por_categoria']:
            stats['por_categoria'][category] = {
                'total': 0,
                'count': 0,
                'media': 0,
                'maior': 0,
                'menor': float('inf')
            }
        
        cat_stats = stats['por_categoria'][category]
        cat_stats['total'] += amount
        cat_stats['count'] += 1
        cat_stats['maior'] = max(cat_stats['maior'], amount)
        cat_stats['menor'] = min(cat_stats['menor'], amount)
        cat_stats['media'] = cat_stats['total'] / cat_stats['count']
        
        # Atualiza totais por mês
        if date not in stats['por_mes']:
            stats['por_mes'][date] = {
                'creditos': 0,
                'debitos': 0,
                'saldo': 0
            }
        
        if amount > 0:
            stats['total_creditos'] += amount
            stats['count_creditos'] += 1
            stats['maior_credito'] = max(stats['maior_credito'], amount)
            stats['por_mes'][date]['creditos'] += amount
        else:
            stats['total_debitos'] += abs(amount)
            stats['count_debitos'] += 1
            stats['maior_debito'] = max(stats['maior_debito'], abs(amount))
            stats['por_mes'][date]['debitos'] += abs(amount)
        
        stats['por_mes'][date]['saldo'] = stats['por_mes'][date]['creditos'] - stats['por_mes'][date]['debitos']
    
    # Calcula médias
    stats['media_creditos'] = stats['total_creditos'] / stats['count_creditos'] if stats['count_creditos'] > 0 else 0
    stats['media_debitos'] = stats['total_debitos'] / stats['count_debitos'] if stats['count_debitos'] > 0 else 0
    
    return stats

def handler(event, context):
    """
    Função principal do Lambda que processa arquivos OFX.
    """
    try:
        # Obtém o conteúdo OFX do corpo da requisição
        if not event:
            raise ValueError("Evento vazio")

        # Debug do evento recebido
        print(f"Evento recebido: {json.dumps(event)[:200]}")

        # Se o evento for uma string, use-o diretamente
        if isinstance(event, str):
            ofx_content = event
        # Se for um dict, procure pelo corpo
        elif isinstance(event, dict):
            if 'body' in event:
                ofx_content = event['body']
            else:
                raise ValueError("Corpo da requisição não encontrado no evento")
        else:
            raise ValueError(f"Formato de evento não suportado: {type(event)}")

        if not ofx_content:
            raise ValueError("Nenhum conteúdo OFX fornecido")

        # Debug do conteúdo OFX
        print(f"Primeiros 100 caracteres do conteúdo OFX: {ofx_content[:100]}")

        # Lida com quebras de linha escapadas substituindo-as por quebras de linha reais
        ofx_content = ofx_content.replace('\\n', '\n')

        # Extrai informações da conta da seção BANKACCTFROM
        bank_id = extract_tag_content(ofx_content, 'BANKID')
        account_id = extract_tag_content(ofx_content, 'ACCTID')
        account_type = extract_tag_content(ofx_content, 'ACCTTYPE')

        if not all([bank_id, account_id, account_type]):
            print(f"Informações da conta incompletas: bank_id={bank_id}, account_id={account_id}, account_type={account_type}")
            raise ValueError("Informações da conta não encontradas no arquivo OFX")

        # Debug: Imprime informações da conta extraídas
        print(f"ID do Banco: {bank_id}")
        print(f"ID da Conta: {account_id}")
        print(f"Tipo da Conta: {account_type}")

        # Extrai informações do período da seção BANKTRANLIST
        banktranlist = extract_parent_tag_content(ofx_content, 'BANKTRANLIST')
        if not banktranlist:
            raise ValueError("Seção BANKTRANLIST não encontrada no arquivo OFX")

        start_date = extract_tag_content(banktranlist, 'DTSTART')
        end_date = extract_tag_content(banktranlist, 'DTEND')

        # Debug: Imprime informações do período extraídas
        print(f"Data Inicial: {start_date}")
        print(f"Data Final: {end_date}")

        # Extrai informações do saldo da seção LEDGERBAL
        ledgerbal = extract_parent_tag_content(ofx_content, 'LEDGERBAL')
        if not ledgerbal:
            raise ValueError("Seção LEDGERBAL não encontrada no arquivo OFX")

        balance_amount = extract_tag_content(ledgerbal, 'BALAMT')
        balance_date = extract_tag_content(ledgerbal, 'DTASOF')

        # Debug: Imprime informações do saldo extraídas
        print(f"Valor do Saldo: {balance_amount}")
        print(f"Data do Saldo: {balance_date}")

        # Extrai todas as transações
        transactions = extract_transactions(ofx_content)
        if not transactions:
            raise ValueError("Nenhuma transação encontrada no arquivo OFX")
        
        # Debug: Imprime número de transações encontradas
        print(f"Número de transações encontradas: {len(transactions)}")

        # Adiciona categoria sugerida
        for transaction in transactions:
            transaction['suggested_category'] = suggest_category(transaction)

        # Realiza análise estatística
        stats = analyze_transactions(transactions)

        # Constrói a resposta
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
            },
            'statistics': stats,
            'debug': {
                'transaction_count': len(transactions),
                'bank_id_found': bank_id is not None,
                'account_id_found': account_id is not None,
                'balance_amount_found': balance_amount is not None,
                'content_length': len(ofx_content),
                'first_chars': ofx_content[:100]
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
        error_response = {
            'error': str(e),
            'debug': {
                'event_type': type(event).__name__,
                'error_type': type(e).__name__,
                'error_details': str(e)
            }
        }
        
        # Adiciona informações de debug se disponíveis
        if 'ofx_content' in locals():
            error_response['debug'].update({
                'content_length': len(ofx_content),
                'first_chars': ofx_content[:100]
            })
        
        print(f"Erro: {json.dumps(error_response)}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(error_response)
        } 