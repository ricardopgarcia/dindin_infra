# DinDin Infra

Este repositório contém as funções Lambda para o aplicativo DinDin.

## Estrutura do Projeto

```
.
├── lambda/
│   ├── accounts.py
│   ├── transactions.py
│   └── requirements.txt
└── README.md
```

## Funções Lambda

### Accounts Lambda
- Endpoint: `/accounts`
- Método: GET
- Descrição: Retorna a lista de contas do usuário

### Transactions Lambda
- Endpoint: `/transactions`
- Método: GET
- Parâmetros:
  - `account`: Nome da conta para filtrar as transações
- Descrição: Retorna as transações de uma conta específica

## Deploy na AWS

1. Instale o AWS CLI e configure suas credenciais:
```bash
aws configure
```

2. Crie um arquivo ZIP com as funções Lambda:
```bash
cd lambda
zip -r ../function.zip .
```

3. Crie a função Lambda na AWS:
```bash
aws lambda create-function \
  --function-name dindin-transactions \
  --runtime python3.9 \
  --handler transactions.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-role
```

4. Configure o API Gateway:
   - Crie uma nova API REST
   - Crie um recurso `/transactions`
   - Configure o método GET
   - Integre com a função Lambda
   - Implante a API

## Desenvolvimento Local

Para testar localmente, você pode usar o AWS SAM CLI:

```bash
sam local invoke TransactionsFunction --event events/event.json
``` 