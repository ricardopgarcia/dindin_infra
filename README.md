# DinDin Infra

Este repositório contém a infraestrutura como código (Terraform) e as funções Lambda para o aplicativo DinDin, incluindo integração com AWS API Gateway e S3 para processamento de extratos bancários em formato OFX.

## Estrutura do Projeto

```
.
├── lambda/
│   ├── accounts.py
│   ├── transactions.py
│   ├── ofx_parser.py
│   ├── requirements.txt
│   └── events/
│       ├── event.json
│       └── sample.ofx
├── main.tf
├── variables.tf
├── README.md
└── ...
```

## Infraestrutura (Terraform)
- **Lambda Functions:**
  - `accounts_api`, `transactions_api`, `ofx_parser_api`, `dindin_api`
- **API Gateway:**
  - Rotas: `/accounts`, `/transactions`, `/ofx-parser`, `/`
- **S3:**
  - Bucket: `dindin-ofx-files` (armazenamento dos arquivos OFX)
- **Variáveis:**
  - `aws_region`, `environment`, `api_stage`

## Funções Lambda e Endpoints

### `/accounts`
- **Método:** GET
- **Descrição:** Retorna a lista de contas do usuário.
- **Exemplo:**
  ```bash
  curl https://<api-url>/accounts
  ```

### `/transactions`
- **Método:** GET
- **Descrição:** Retorna as transações do extrato OFX mais recente do S3, agrupadas por mês, com estatísticas e filtros.
- **Parâmetros de filtro:**
  - `month` (ex: 2025-03)
  - `category` (ex: Salário, Rendimentos, etc)
  - `type` (CREDIT ou DEBIT)
- **Exemplo:**
  ```bash
  curl "https://<api-url>/transactions?type=DEBIT&month=2025-03"
  ```
- **Exemplo de resposta:**
  ```json
  {
    "summary": {
      "period": {"startDate": "2025-01-27", "endDate": "2025-04-25"},
      "balance": {"amount": 17140.7, "date": "2025-04-25"},
      "total_transactions": 60,
      "total_credit": 97307.67,
      "total_debit": 118624.48,
      "net_balance": -21316.81
    },
    "transactions_by_month": { ... },
    "statistics": { ... }
  }
  ```

### `/ofx-parser`
- **Método:** POST
- **Descrição:** Recebe um arquivo OFX (via body) e retorna os dados estruturados (conta, período, saldo, transações detalhadas).

## Integração com S3
- O arquivo OFX mais recente deve ser enviado para o bucket S3 `dindin-ofx-files` com o nome `latest.ofx`:
  ```bash
  aws s3 cp caminho/para/arquivo.ofx s3://dindin-ofx-files/latest.ofx
  ```

## Deploy

### Usando Terraform
1. Configure suas credenciais AWS:
   ```bash
   aws configure
   ```
2. Inicialize e aplique o Terraform:
   ```bash
   terraform init
   terraform apply -auto-approve
   ```

### Atualizando código das Lambdas
1. Instale dependências e compacte:
   ```bash
   cd lambda
   pip install -r requirements.txt -t .
   zip -r ../transactions.zip .
   ```
2. Atualize a função Lambda:
   ```bash
   aws lambda update-function-code --function-name transactions_api --zip-file fileb://../transactions.zip
   ```

## Desenvolvimento Local e Testes
- Teste funções Lambda localmente com AWS SAM:
  ```bash
  sam local invoke TransactionsFunction --event events/event.json
  ```
- Teste endpoints com `curl` ou Postman.

## Contribuição
- Faça um fork do projeto
- Crie uma branch para sua feature/fix
- Envie um Pull Request

---

**Dúvidas ou sugestões?** Abra uma issue ou entre em contato! 